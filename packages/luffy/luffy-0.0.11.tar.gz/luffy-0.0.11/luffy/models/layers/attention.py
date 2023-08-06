import torch
import torch.nn.functional as F
from einops import rearrange, repeat
from einops.layers.torch import Rearrange
from torch import nn, einsum
from torch.nn.modules.utils import _pair

from .mlp import MLP

__all__ = ['Attention', 'WindowAttention', 'WindowAttentionV2', 'DeformableAttention', 'MultiQueryAttention']


class Attention(nn.Module):
    def __init__(self, dim, num_heads=8, dim_head=None, drop=0.):
        super().__init__()
        dim_head = dim_head or dim // num_heads

        self.num_heads = num_heads
        self.scale = dim_head ** -0.5
        inner_dim = dim_head * num_heads
        self.to_qkv = nn.Linear(dim, inner_dim * 3, bias=False)
        self.drop = nn.Dropout(drop)
        self.to_out = nn.Sequential(nn.Linear(inner_dim, dim), nn.Dropout(drop))

    def forward(self, x, mask=None):
        q, k, v = self.to_qkv(x).chunk(3, dim=-1)
        q, k, v = map(lambda t: rearrange(t, 'b n (nh d) -> b nh n d', nh=self.num_heads), (q, k, v))
        q = q * self.scale
        sim = einsum('b h i d, b h j d -> b h i j', q, k)  # h means nh
        # TODO: other mask types?
        if mask is not None:
            b, _, n, n = sim.shape
            assert mask.shape == (b, n, n), 'mask has incorrect dimensions'
            sim.masked_fill_(~mask, -torch.finfo(sim.dtype).max)
        attn = sim.softmax(dim=-1)
        attn = self.drop(attn)

        out = einsum('b h i j, b h j d -> b h i d', attn, v)
        out = rearrange(out, 'b nh n d -> b n (nh d)')
        return self.to_out(out)


class WindowAttention(nn.Module):
    @staticmethod
    def double_step_seq(step1, len1, step2, len2):
        seq1 = torch.arange(0, step1 * len1, step1)
        seq2 = torch.arange(0, step2 * len2, step2)
        return (seq1[:, None] + seq2[None, :]).reshape(1, -1)

    def __init__(self, dim, window_size, num_heads, dim_head=None, drop=0.):
        super().__init__()
        dim_head = dim_head or dim // num_heads

        self.num_heads = num_heads
        self.scale = dim_head ** -0.5
        inner_dim = dim_head * num_heads
        self.to_qkv = nn.Linear(dim, inner_dim * 3, bias=False)
        self.drop = nn.Dropout(drop)
        self.to_out = nn.Sequential(nn.Linear(inner_dim, dim), nn.Dropout(drop))

        wh, ww = _pair(window_size)
        self.ws = wh * ww
        self.relative_position_bias_table = nn.Parameter(torch.zeros((2 * wh - 1) * (2 * ww - 1), num_heads))
        rel_index_coords = self.double_step_seq(2 * ww - 1, wh, 1, ww)
        relative_position_index = rel_index_coords + rel_index_coords.T
        relative_position_index = relative_position_index.flip(1)
        relative_position_index = rearrange(relative_position_index, 'ws1 ws2-> (ws1 ws2)')
        self.register_buffer("relative_position_index", relative_position_index)

    def forward(self, x, mask=None):
        """
        Args:
            x: input features with shape of (num_windows*B, N, C)
            mask: (0/-inf) mask with shape of (num_windows, Wh*Ww, Wh*Ww) or None
        """
        q, k, v = self.to_qkv(x).chunk(3, dim=-1)
        q, k, v = map(lambda t: rearrange(t, 'b n (nh d) -> b nh n d', nh=self.num_heads), (q, k, v))
        q = q * self.scale
        sim = einsum('b h i d, b h j d -> b h i j', q, k)

        relative_position_bias = self.relative_position_bias_table[self.relative_position_index]
        relative_position_bias = rearrange(relative_position_bias, '(ws1 ws2) n-> 1 n ws1 ws2', ws1=self.ws)
        sim = sim + relative_position_bias
        if mask is not None:
            sim = rearrange(sim, '(b nw) nh n1 n2 -> b nw nh n1 n2', nw=mask.shape[0])
            mask = rearrange(mask, 'nw ws1 ws2 -> 1 nw 1 ws1 ws2')
            sim = sim + mask
            sim = rearrange(sim, 'b nw nh n1 n2 -> (b nw) nh n1 n2')

        attn = sim.softmax(dim=-1)
        attn = self.drop(attn)

        out = einsum('b h i j, b h j d -> b h i d', attn, v)
        out = rearrange(out, 'b nh n d -> b n (nh d)')
        return self.to_out(out)


class WindowAttentionV2(nn.Module):
    def __init__(self, dim, window_size, num_heads, dim_head=None, drop=0., meta_hidden_dim=384):
        super().__init__()
        super().__init__()
        dim_head = dim_head or dim // num_heads
        wh, ww = _pair(window_size)
        self.num_heads = num_heads
        self.scale = dim_head ** -0.5
        inner_dim = dim_head * num_heads
        self.to_qkv = nn.Linear(dim, inner_dim * 3, bias=False)
        self.drop = nn.Dropout(drop)
        self.to_out = nn.Sequential(nn.Linear(inner_dim, dim), nn.Dropout(drop))

        # meta network for positional encodings
        self.meta_mlp = MLP(2, meta_hidden_dim, num_heads)
        self.register_parameter("tau", torch.nn.Parameter(torch.ones((1, num_heads, 1, 1))))
        coordinates = torch.cartesian_prod(torch.arange(wh), torch.arange(ww))
        relative_coordinates = coordinates[:, None, :] - coordinates[None, :, :]
        relative_coordinates_log = torch.sign(relative_coordinates) * torch.log(1.0 + relative_coordinates.abs())
        self.register_buffer("relative_coordinates_log", relative_coordinates_log, persistent=False)

    def forward(self, x, mask=None):
        q, k, v = self.to_qkv(x).chunk(3, dim=-1)
        q, k, v = map(lambda t: rearrange(t, 'b n (nh d) -> b nh n d', nh=self.num_heads), (q, k, v))
        # compute attention map with scaled cosine attention
        q, k = F.normalize(q, dim=-1), F.normalize(k, dim=-1)
        sim = einsum('b h i d, b h j d -> b h i j', q, k)
        sim = sim * self.tau
        relative_position_bias = self.meta_mlp(self.relative_coordinates_log)
        relative_position_bias = rearrange(relative_position_bias, 'ws1 ws2 nh->1 nh ws1 ws2')
        sim = sim + relative_position_bias
        if mask is not None:
            sim = rearrange(sim, '(b nw) nh n1 n2 -> b nw nh n1 n2', nw=mask.shape[0])
            mask = rearrange(mask, 'nw ws1 ws2 -> 1 nw 1 ws1 ws2')
            sim = sim + mask
            sim = rearrange(sim, 'b nw nh n1 n2 -> (b nw) nh n1 n2')

        attn = sim.softmax(dim=-1)
        attn = self.drop(attn)

        out = einsum('b h i j, b h j d -> b h i d', attn, v)
        out = rearrange(out, 'b nh n d -> b n (nh d)')
        return self.to_out(out)


class DeformableAttention(nn.Module):
    def __init__(self, dim, input_resolution, offset_kernel_size, offset_range_factor=2, num_heads=8, dim_head=None,
                 drop=0., dim_group=128):
        super().__init__()
        dim_head = dim_head or dim // num_heads

        self.num_heads = num_heads
        self.scale = dim_head ** -0.5
        inner_dim = dim_head * num_heads
        self.h, self.w = input_resolution
        self.dim_group = dim_group
        self.num_groups = dim // dim_group
        self.offset_range_factor = offset_range_factor

        self.conv_offset = nn.Sequential(
            nn.Conv2d(dim_group, dim_group, offset_kernel_size, 1, offset_kernel_size // 2, groups=dim_group),
            Rearrange('B dg h w -> B h w dg'),
            nn.LayerNorm(dim_group),
            nn.GELU(),
            nn.Linear(dim_group, 2, bias=False)
        )

        self.to_q = nn.Linear(dim, inner_dim, bias=False)
        self.to_kv = nn.Linear(dim, inner_dim * 2, bias=False)

        self.drop = nn.Dropout(drop)
        self.to_out = nn.Sequential(nn.Linear(inner_dim, dim), nn.Dropout(drop))

        self.rpe_table = nn.Parameter(torch.zeros(self.num_heads, self.h * 2 - 1, self.w * 2 - 1))
        reference = self.get_reference(self.h, self.w)
        self.register_buffer('reference', reference)

    @staticmethod
    def get_reference(h, w):
        ref_y, ref_x = torch.meshgrid(
            torch.linspace(0.5, h - 0.5, h),
            torch.linspace(0.5, w - 0.5, w))

        ref = torch.stack((ref_y, ref_x), -1)
        ref[..., 1].div_(w).mul_(2).sub_(1)
        ref[..., 0].div_(h).mul_(2).sub_(1)

        return ref

    def resample(self, x):
        x = rearrange(x, 'b (h w) (ng dg) -> (b ng) dg h w', dg=self.dim_group, h=self.h)
        offset = self.conv_offset(x)
        if self.offset_range_factor > 0:
            offset_range = torch.tensor([1.0 / self.h, 1.0 / self.w]).reshape(1, 1, 1, 2)
            offset = offset.tanh().mul(offset_range).mul(self.offset_range_factor)

        if self.offset_range_factor >= 0:
            pos = offset + self.reference
        else:
            pos = (offset + self.reference).tanh()

        x_sampled = F.grid_sample(
            input=x,
            grid=pos[..., (1, 0)],  # y, x -> x, y
            mode='bilinear', align_corners=True)  # B, dg, h, w

        x_sampled = rearrange(x_sampled, '(b ng) dg h w -> b (h w) (ng dg)', ng=self.num_groups)

        rpe_bias = repeat(self.rpe_table, '(ng nhg) H W -> (b ng) nhg H W', b=x.shape[0] // self.num_groups,
                          ng=self.num_groups)

        q_grid = repeat(self.reference, 'h w p -> B (h w) 1 p', B=x.shape[0])
        pos = rearrange(pos, 'B h w p -> B 1 (h w) p')
        displacement = (q_grid - pos).mul(0.5)

        attn_bias = F.grid_sample(
            input=rpe_bias,
            grid=displacement[..., (1, 0)],
            mode='bilinear', align_corners=True
        )  # B, nhg, L, L # L = h * w

        attn_bias = rearrange(attn_bias, '(b ng) nhg L1 L2 -> b (ng nhg) L1 L2', ng=self.num_groups)
        return x_sampled, attn_bias

    def forward(self, x):
        q = self.to_q(x)
        x_sampled, attn_bias = self.resample(q)
        k, v = self.to_kv(x_sampled).chunk(2, dim=-1)
        q, k, v = map(lambda t: rearrange(t, 'b n (nh d) -> b nh n d', nh=self.num_heads), (q, k, v))
        q = q * self.scale
        sim = einsum('b h i d, b h j d -> b h i j', q, k)  # h means nh
        sim = sim + attn_bias
        attn = sim.softmax(dim=-1)
        attn = self.drop(attn)

        out = einsum('b h i j, b h j d -> b h i d', attn, v)
        out = rearrange(out, 'b nh n d -> b n (nh d)')
        return self.to_out(out)


class RotaryEmbedding(nn.Module):
    """rotary positional embedding.
    `RoFormer: Enhanced Transformer with Rotary Position Embedding
    <https://arxiv.org/abs/2104.09864>`_"""

    def __init__(self, dim):
        super().__init__()
        inv_freq = 1.0 / (10000 ** (torch.arange(0, dim, 2).float() / dim))
        self.register_buffer("inv_freq", inv_freq)

    def forward(self, max_seq_len):
        seq = torch.arange(max_seq_len, dtype=self.inv_freq.dtype)
        freqs = einsum("i , j -> i j", seq, self.inv_freq)
        return torch.cat((freqs, freqs), dim=-1)


class MultiQueryAttention(nn.Module):
    def __init__(self, dim, dim_head=None, num_heads=8, drop=0.):
        super().__init__()
        dim_head = dim_head or dim // num_heads
        self.num_heads = num_heads
        self.scale = dim_head ** -0.5
        inner_dim = dim_head * num_heads
        self.to_q = nn.Linear(dim, inner_dim, bias=False)
        self.to_kv = nn.Linear(dim, dim_head * 2, bias=False)
        self.drop = nn.Dropout(drop)
        self.to_out = nn.Sequential(nn.Linear(inner_dim, dim), nn.Dropout(drop))

        self.rotary_emb = RotaryEmbedding(dim_head)

        # for caching causal mask and rotary embeddings
        self.register_buffer("mask", None, persistent=False)
        self.register_buffer("pos_emb", None, persistent=False)

    def get_rotary_embedding(self, n):
        if self.pos_emb is not None and self.pos_emb.shape[-2] >= n:
            return self.pos_emb[:n]

        pos_emb = self.rotary_emb(n)
        self.register_buffer("pos_emb", pos_emb, persistent=False)
        return pos_emb

    @staticmethod
    def rotate_half(x):
        x = rearrange(x, "... (j d) -> ... j d", j=2)
        x1, x2 = x.unbind(dim=-2)
        return torch.cat((-x2, x1), dim=-1)

    def apply_rotary_pos_emb(self, pos, t):
        return (t * pos.cos()) + (self.rotate_half(t) * pos.sin())

    def get_mask(self, n):
        if self.mask is not None and self.mask.shape[-1] >= n:
            return self.mask[:n, :n]

        mask = torch.ones((n, n), dtype=torch.bool).triu(1)
        self.register_buffer("mask", mask, persistent=False)
        return mask

    def forward(self, x):
        q = self.to_q(x)
        k, v = self.to_kv(x).chunk(2, dim=-1)
        q = rearrange(q, "b n (nh d) -> b nh n d", nh=self.num_heads)

        positions = self.get_rotary_embedding(x.shape[1])
        q, k = map(lambda t: self.apply_rotary_pos_emb(positions, t), (q, k))

        q = q * self.scale
        sim = einsum('b h i d, b j d -> b h i j', q, k)  # h means nh
        causal_mask = self.get_mask(x.shape[1])
        sim = sim.masked_fill(causal_mask, -torch.finfo(sim.dtype).max)
        sim = sim - sim.amax(dim=-1, keepdim=True)
        attn = sim.softmax(dim=-1)
        attn = self.drop(attn)

        out = einsum('b h i j, b j d -> b h i d', attn, v)
        out = rearrange(out, 'b nh n d -> b n (nh d)')
        return self.to_out(out)
