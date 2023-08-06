import torch.nn as nn
from einops.layers.torch import Rearrange
from torch.nn.modules.utils import _pair

from .layers import SwinTransformerBlockV2

__all__ = ['SwinV2T', 'SwinV2S', 'SwinV2B', 'SwinV2L', 'SwinV2H', 'SwinV2G']


class BasicLayer(nn.Module):
    def __init__(self, dim, input_resolution, depth, num_head, window_size, mlp_ratio=4., drop=0., attn_drop=0.,
                 patch_merging=False, extra_norm_period=0):
        super().__init__()

        self.blocks = nn.ModuleList([
            SwinTransformerBlockV2(dim=dim, input_resolution=input_resolution,
                                   num_heads=num_head, window_size=window_size,
                                   shift_size=0 if (i % 2 == 0) else window_size // 2,
                                   mlp_dim=dim * mlp_ratio, drop=drop, attn_drop=attn_drop,
                                   extra_norm=True if extra_norm_period and (i + 1) % extra_norm_period == 0 else False)
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


class SwinTransformerV2(nn.Module):
    """Swin Transformer V2.
    A PyTorch implement of : `Swin Transformer V2: Scaling Up Capacity and Resolution
    <https://arxiv.org/abs/2111.09883>`_"""

    def __init__(self, *, image_size, channels=3, patch_size=4, dim=96, depths=(2, 2, 6, 2), num_heads=(3, 6, 12, 24),
                 mlp_ratio=4, drop=0., attn_drop=0., num_classes=1000, window_size=None, image_window_ratio=32,
                 extra_norm_period=0):
        super(SwinTransformerV2, self).__init__()
        image_height, image_width = _pair(image_size)
        patch_height, patch_width = _pair(patch_size)
        if window_size is None:
            window_size = max(image_height, image_width) // image_window_ratio  # for simplification
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
        for dim, input_resolution, depth, num_head, patch_merging in \
                zip(dims, input_resolutions, depths, num_heads, patch_mergings):
            self.layers.append(BasicLayer(dim=dim, input_resolution=input_resolution, depth=depth, num_head=num_head,
                                          window_size=window_size, mlp_ratio=mlp_ratio, drop=drop, attn_drop=attn_drop,
                                          patch_merging=patch_merging, extra_norm_period=extra_norm_period))

        self.mlp_head = nn.Sequential(nn.LayerNorm(dims[-1]), nn.Linear(dims[-1], num_classes))

    def forward(self, x):
        x = self.patch_embedding(x)
        x = self.dropout(x)

        for layer in self.layers:
            x = layer(x)

        x = x.mean(dim=1)

        return self.mlp_head(x)


def swinv2_params(model_name):
    params_dict = {
        'swinv2-t': {'dim': 96, 'depths': (2, 2, 6, 2), 'num_heads': (3, 6, 12, 24)},
        'swinv2-s': {'dim': 96, 'depths': (2, 2, 18, 2), 'num_heads': (3, 6, 12, 24)},
        'swinv2-b': {'dim': 128, 'depths': (2, 2, 18, 2), 'num_heads': (4, 8, 16, 32)},
        'swinv2-l': {'dim': 192, 'depths': (2, 2, 18, 2), 'num_heads': (6, 12, 24, 48)},
        'swinv2-h': {'dim': 352, 'depths': (2, 2, 18, 2), 'num_heads': (8, 16, 32, 64), 'extra_norm_period': 6},
        'swinv2-g': {'dim': 512, 'depths': (2, 2, 42, 2), 'num_heads': (16, 32, 64, 128), 'extra_norm_period': 6},
    }
    return params_dict[model_name]


class SwinV2T(SwinTransformerV2):
    def __init__(self, **kwargs):
        super().__init__(**{**swinv2_params('swinv2-t'), **kwargs})


class SwinV2S(SwinTransformerV2):
    def __init__(self, **kwargs):
        super().__init__(**{**swinv2_params('swinv2-s'), **kwargs})


class SwinV2B(SwinTransformerV2):
    def __init__(self, **kwargs):
        super().__init__(**{**swinv2_params('swinv2-b'), **kwargs})


class SwinV2L(SwinTransformerV2):
    def __init__(self, **kwargs):
        super().__init__(**{**swinv2_params('swinv2-l'), **kwargs})


class SwinV2H(SwinTransformerV2):
    def __init__(self, **kwargs):
        super().__init__(**{**swinv2_params('swinv2-h'), **kwargs})


class SwinV2G(SwinTransformerV2):
    def __init__(self, **kwargs):
        super().__init__(**{**swinv2_params('swinv2-g'), **kwargs})
