from einops.layers.torch import Rearrange
from torch import nn
from torch.nn.modules.utils import _pair

from .layers import SwinTransformerBlock, DeformableAttentionTransformerBlock

__all__ = ['DATT', 'DATS', 'DATB']


class BasicLayer1(nn.Module):
    def __init__(self, dim, input_resolution, depth, num_head, window_size, mlp_ratio=4., drop=0., attn_drop=0.,
                 patch_merging=False):
        super().__init__()
        self.blocks = nn.ModuleList([
            SwinTransformerBlock(dim=dim, input_resolution=input_resolution,
                                 num_heads=num_head, window_size=window_size,
                                 shift_size=0 if (i % 2 == 0) else window_size // 2,
                                 mlp_dim=dim * mlp_ratio,
                                 drop=drop, attn_drop=attn_drop)
            for i in range(depth)])

        if patch_merging:
            self.patch_merging = nn.Sequential(
                Rearrange('b (h hs w ws) c -> b (h w) (ws hs c)', hs=2, ws=2, h=input_resolution[0] // 2),
                nn.LayerNorm(4 * dim),
                nn.Linear(4 * dim, 2 * dim, bias=False))
        else:
            self.patch_merging = None

    def forward(self, x):
        for blk in self.blocks:
            x = blk(x)
        if self.patch_merging is not None:
            x = self.patch_merging(x)
        return x


class BasicLayer2(nn.Module):
    def __init__(self, dim, input_resolution, depth, num_head, window_size, offset_kernel_size, offset_range_factor,
                 mlp_ratio=4., drop=0., attn_drop=0., patch_merging=False):
        super().__init__()
        self.blocks = nn.ModuleList()
        for _ in range(depth // 2):
            self.blocks.append(
                SwinTransformerBlock(dim=dim, input_resolution=input_resolution,
                                     num_heads=num_head, window_size=window_size,
                                     shift_size=0,
                                     mlp_dim=dim * mlp_ratio,
                                     drop=drop, attn_drop=attn_drop))
            self.blocks.append(
                DeformableAttentionTransformerBlock(dim=dim, input_resolution=input_resolution,
                                                    num_heads=num_head,
                                                    mlp_dim=dim * mlp_ratio,
                                                    drop=drop, attn_drop=attn_drop,
                                                    offset_kernel_size=offset_kernel_size,
                                                    offset_range_factor=offset_range_factor))

        if patch_merging:
            self.patch_merging = nn.Sequential(
                Rearrange('b (h hs w ws) c -> b (h w) (ws hs c)', hs=2, ws=2, h=input_resolution[0] // 2),
                nn.LayerNorm(4 * dim),
                nn.Linear(4 * dim, 2 * dim, bias=False))
        else:
            self.patch_merging = None

    def forward(self, x):
        for blk in self.blocks:
            x = blk(x)
        if self.patch_merging is not None:
            x = self.patch_merging(x)
        return x


class DeformableAttentionTransformer(nn.Module):
    """Deformable Attention Transformer.
    A PyTorch implement of : `Vision Transformer with Deformable Attention
    <https://arxiv.org/abs/2201.00520>`_"""

    def __init__(self, *, image_size=224, channels=3, patch_size=4, dim=96, depths=(2, 2, 6, 2),
                 num_heads=(3, 6, 12, 24), mlp_ratio=4, drop=0., attn_drop=0., num_classes=1000, window_size=7,
                 offset_kernel_sizes=(9, 7, 5, 3), offset_range_factor=2, **kwargs):
        super().__init__()
        image_height, image_width = _pair(image_size)
        patch_height, patch_width = _pair(patch_size)

        assert image_height % patch_height == 0 and image_width % patch_width == 0, \
            'Image size must be divisible by patch size!'

        patches_resolution = (image_height // patch_height, image_width // patch_width)
        patch_dim = channels * patch_height * patch_width

        self.patch_embedding = nn.Sequential(
            Rearrange('b c (h p1) (w p2) -> b (h w) (p1 p2 c)', p1=patch_height, p2=patch_width),
            nn.Linear(patch_dim, dim))

        self.dropout = nn.Dropout(drop)

        num_layers = len(depths)
        dims = [dim * 2 ** i for i in range(num_layers)]
        input_resolutions = [(patches_resolution[0] // 2 ** i, patches_resolution[1] // 2 ** i) for i in
                             range(num_layers)]
        patch_mergings = [True if i < num_layers - 1 else False for i in range(num_layers)]

        # build layers
        self.layers = nn.ModuleList()
        for i, (dim, input_resolution, depth, num_head, patch_merging) in \
                enumerate(zip(dims, input_resolutions, depths, num_heads, patch_mergings)):
            # first two stages not use deformable attention
            if i < 2:
                self.layers.append(
                    BasicLayer1(dim=dim, input_resolution=input_resolution, depth=depth, num_head=num_head,
                                window_size=window_size, mlp_ratio=mlp_ratio, drop=drop,
                                attn_drop=attn_drop, patch_merging=patch_merging))
            else:
                self.layers.append(
                    BasicLayer2(dim=dim, input_resolution=input_resolution, depth=depth, num_head=num_head,
                                window_size=window_size, offset_kernel_size=offset_kernel_sizes[i],
                                offset_range_factor=offset_range_factor, mlp_ratio=mlp_ratio, drop=drop,
                                attn_drop=attn_drop, patch_merging=patch_merging))
        self.mlp_head = nn.Sequential(nn.LayerNorm(dims[-1]), nn.Linear(dims[-1], num_classes))

    def forward(self, x):
        x = self.patch_embedding(x)
        x = self.dropout(x)

        for layer in self.layers:
            x = layer(x)

        x = x.mean(dim=1)
        return self.mlp_head(x)


def dat_params(model_name):
    params_dict = {
        'dat-t': {'dim': 96, 'depths': (2, 2, 6, 2), 'num_heads': (3, 6, 12, 24)},
        'dat-s': {'dim': 96, 'depths': (2, 2, 18, 2), 'num_heads': (3, 6, 12, 24)},
        'dat-b': {'dim': 128, 'depths': (2, 2, 18, 2), 'num_heads': (4, 8, 16, 32)},
    }
    return params_dict[model_name]


class DATT(DeformableAttentionTransformer):
    def __init__(self, **kwargs):
        super().__init__(**{**dat_params('dat-t'), **kwargs})


class DATS(DeformableAttentionTransformer):
    def __init__(self, **kwargs):
        super().__init__(**{**dat_params('dat-s'), **kwargs})


class DATB(DeformableAttentionTransformer):
    def __init__(self, **kwargs):
        super().__init__(**{**dat_params('dat-b'), **kwargs})
