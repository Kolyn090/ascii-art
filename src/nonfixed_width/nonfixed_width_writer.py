import os
import sys

import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../util')))
from palette_template import PaletteTemplate  # type: ignore
from static import (to_binary_strong, to_grayscale, increase_contrast,  # type: ignore
                    resize_nearest_neighbor, to_binary_middle, smooth_colors,  # type: ignore
                    invert_image)  # type: ignore

class NonFixedWidthWriter:
    def __init__(self,
                 palettes: list[PaletteTemplate],
                 gradient_imgs: list[np.ndarray],
                 max_workers=16):
        self.palettes = palettes
        self.max_workers = max_workers
        self.gradient_imgs = gradient_imgs
        self.layers = self._get_layers()

    def _get_layers(self):
        layers = []
        for i in range(len(self.palettes)):
            palette = self.palettes[i]
            gradient_img = self.gradient_imgs[i]
            flow_writer = palette.create_flow_writer(self.max_workers)
            final_img, p_cts = flow_writer.match(gradient_img)
            layers.append(p_cts)
        return layers

    def _get_char_weight(self) -> dict[str, int]:
        pass
