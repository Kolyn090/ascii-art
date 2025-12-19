import math
import os
import sys
from typing import Callable
from static import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shade')))
from gradient_writer import GradientWriter  # type: ignore

def blend_ascii_with_color(ascii_img: np.ndarray,
                           color_img: np.ndarray,
                           strength: float) -> np.ndarray:
    ascii_f = ascii_img.astype(np.float32)
    color_f = color_img.astype(np.float32)

    blended = strength * color_f + (1-strength) * ascii_f

    # Add alpha channel if needed
    if blended.shape[2] == 3:
        alpha = np.full((blended.shape[0], blended.shape[1], 1), 255, dtype=np.float32)
        blended = np.concatenate([blended, alpha], axis=2)

    return np.round(blended).astype(np.uint8)

def copy_black_pixels(source_img: np.ndarray,
                      target_img: np.ndarray) -> np.ndarray:
    assert source_img.shape[:2] == target_img.shape[:2], \
        "Images must have the same dimensions."

    result = target_img.copy()
    mask = np.all(source_img[..., :3] == 0, axis=2)
    result[mask, :3] = [0, 0, 0]
    return result

def process_image_blocks(img: np.ndarray,
                         cell_size: tuple[int, int],
                         block_func: Callable[[np.ndarray], np.ndarray]) -> np.ndarray:
    h, w = img.shape[:2]
    cell_w, cell_h = cell_size
    output = img.copy()

    for y in range(0, h, cell_h):
        for x in range(0, w, cell_w):
            block = img[y:y + cell_h, x:x + cell_w]
            processed_block = block_func(block)

            # Ensure processed block has the same size
            output[y:y + cell_h, x:x + cell_w] = processed_block
    output = output[0:math.floor(h / cell_size[1]) * cell_size[1],
                    0:math.floor(w / cell_size[0]) * cell_size[0]]
    return output

def average_color_block(block: np.ndarray) -> np.ndarray:
    avg_color = block.mean(axis=(0, 1), keepdims=True)
    return np.tile(avg_color, (block.shape[0], block.shape[1], 1)).astype(block.dtype)
