import torch
from einops import rearrange
from torch import nn

from .activation import SwiGLU
from .attention import Attention, WindowAttention, WindowAttentionV2, MultiQueryAttention
from .mlp import MLP

__all__ = ['TransformerBlock', 'ParallelTransformerBlock', 'SwinTransformerBlock', 'SwinTransformerBlockV2']


class TransformerBlock(nn.Module):
    def __init__(self, dim, num_heads, mlp_dim, drop=0., attn_drop=0.):
        super().__init__()
        self.attn = nn.Sequential(
            nn.LayerNorm(dim),
            Attention(dim, num_heads=num_heads, drop=attn_drop))
        self.mlp = nn.Sequential(
            nn.LayerNorm(dim),
            MLP(dim, mlp_dim, drop=drop))

    def forward(self, x):
        x = self.attn(x) + x
        x = self.mlp(x) + x

        return x


class ParallelTransformerBlock(nn.Module):
    def __init__(self, dim, num_heads, mlp_dim, drop=0., attn_drop=0., act_layer=SwiGLU):
        super().__init__()
        self.attn = nn.Sequential(
            nn.LayerNorm(dim),
            MultiQueryAttention(dim, num_heads=num_heads, drop=attn_drop))
        self.mlp = nn.Sequential(
            nn.LayerNorm(dim),
            MLP(dim, mlp_dim, drop=drop))

    def forward(self, x):
        x = self.mlp(x) + self.attn(x) + x

        return x


class SwinTransformerBlock(nn.Module):
    def __init__(self, *, dim, input_resolution, num_heads, window_size=7, shift_size=0, mlp_dim, drop=0.,
                 attn_drop=0.):
        super().__init__()
        self.dim = dim
        self.input_resolution = input_resolution
        self.num_heads = num_heads
        self.window_size = window_size
        self.shift_size = shift_size
        self.attn_drop = attn_drop
        if min(self.input_resolution) <= self.window_size:
            # if window size is larger than input resolution, we don't partition windows
            self.shift_size = 0
            self.window_size = min(self.input_resolution)
        assert 0 <= self.shift_size < self.window_size, "shift_size must in 0-window_size"

        self.norm1 = nn.LayerNorm(dim)
        self.norm2 = nn.LayerNorm(dim)
        self.attn = WindowAttention(self.dim, window_size=self.window_size, num_heads=self.num_heads,
                                    drop=self.attn_drop)

        attn_mask = self.get_attn_mask(self.input_resolution, self.window_size, self.shift_size)
        self.register_buffer("attn_mask", attn_mask)

        self.mlp = MLP(dim, mlp_dim, drop=drop)

    @staticmethod
    def get_attn_mask(input_resolution, window_size, shift_size):
        if shift_size > 0:
            # calculate attention mask for SW-MSA
            img_mask = torch.zeros((1, *input_resolution, 1))  # 1 H W 1
            h_slices = (slice(0, -window_size),
                        slice(-window_size, -shift_size),
                        slice(-shift_size, None))
            w_slices = (slice(0, -window_size),
                        slice(-window_size, -shift_size),
                        slice(-shift_size, None))
            cnt = 0
            for h in h_slices:
                for w in w_slices:
                    img_mask[:, h, w, :] = cnt
                    cnt += 1

            mask_windows = rearrange(img_mask, 'b (h hws) (w wws) 1 -> (b h w) (hws wws 1)', hws=window_size,
                                     wws=window_size)

            attn_mask = mask_windows.unsqueeze(1) - mask_windows.unsqueeze(2)
            attn_mask = attn_mask.masked_fill(attn_mask != 0, float(-100.0)).masked_fill(attn_mask == 0, float(0.0))
        else:
            attn_mask = None
        return attn_mask

    def shift_window_attn(self, x):
        H, W = self.input_resolution
        x = rearrange(x, 'b (h w) c -> b h w c', h=H)
        # cyclic shift
        if self.shift_size > 0:
            shifted_x = torch.roll(x, shifts=(-self.shift_size, -self.shift_size), dims=(1, 2))
        else:
            shifted_x = x
        # partition windows
        x_windows = rearrange(shifted_x, 'b (h hws) (w wws) c -> (b h w) (hws wws) c', hws=self.window_size,
                              wws=self.window_size)
        # W-MSA/SW-MSA
        attn_windows = self.attn(x_windows, mask=self.attn_mask)  # nW*B, window_size*window_size, C
        # merge windows
        shifted_x = rearrange(attn_windows, '(b h w) (hws wws) c -> b (h hws) (w wws) c', h=H // self.window_size,
                              w=W // self.window_size, hws=self.window_size)
        # reverse cyclic shift
        if self.shift_size > 0:
            attn_x = torch.roll(shifted_x, shifts=(self.shift_size, self.shift_size), dims=(1, 2))
        else:
            attn_x = shifted_x
        attn_x = rearrange(attn_x, 'b h w c -> b (h w) c')
        return attn_x

    def forward(self, x):
        x = self.shift_window_attn(self.norm1(x)) + x
        x = self.mlp(self.norm2(x)) + x

        return x


class SwinTransformerBlockV2(SwinTransformerBlock):
    def __init__(self, extra_norm=False, **kwargs):
        super().__init__(**kwargs)
        self.attn = WindowAttentionV2(dim=self.dim, window_size=self.window_size, num_heads=self.num_heads,
                                      drop=self.attn_drop)

        self.norm3 = nn.LayerNorm(self.dim) if extra_norm else nn.Identity()

    def forward(self, x):
        x = self.norm1(self.shift_window_attn(x)) + x
        x = self.norm2(self.mlp(x)) + x
        x = self.norm3(x)  # main-branch norm enabled for some blocks / stages (every 6 for Huge/Giant)
        return x
