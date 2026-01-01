import math
from typing import Callable

from static import *
from char_template import PositionalCharTemplate

class PositionalColor:
    def __init__(self, color: np.ndarray, position: tuple[int, int]):
        self.color = color
        self.top_left = position

    def __str__(self):
        return f"{{{self.color}{self.top_left}}}"

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

def blend_pixels(source_img: np.ndarray,
                 target_img: np.ndarray) -> np.ndarray:
    assert source_img.shape[:2] == target_img.shape[:2], \
        "Images must have the same dimensions."

    # Compute grayscale intensity
    gray = source_img[..., :3].mean(axis=2)  # shape (H, W)

    # Step 1: mask of pixels greater than 0
    mask = (gray > 0)  # True where we want to blend

    # Step 2: convert to strength (0-1)
    strength = np.zeros_like(gray, dtype=np.float32)
    strength[mask] = gray[mask] / 255.0  # only for masked pixels

    # Step 3: expand grayscale to 3 channels
    gray3 = np.repeat(gray[..., None], 3, axis=2).astype(np.float32)

    # Ensure target is float
    result = target_img.copy().astype(np.float32)

    # Expand strength to 3 channels
    strength3 = np.repeat(strength[..., None], 3, axis=2)

    # Blend: result = (1 - strength) * target + strength * gray
    result[..., :3] = strength3 * result[..., :3] + (1 - strength3) * 0.3 * gray3

    # Preserve alpha if present
    if target_img.shape[2] > 3:
        result[..., 3:] = target_img[..., 3:]

    # Convert back to uint8
    result = np.clip(result, 0, 255).astype(np.uint8)

    return result.astype(np.uint8)

def process_image_blocks(img: np.ndarray,
                         cell_size: tuple[int, int],
                         block_func: Callable[[np.ndarray], np.ndarray]) \
        -> tuple[np.ndarray, list[PositionalColor]]:
    h, w = img.shape[:2]
    cell_w, cell_h = cell_size
    output = img.copy()
    p_cs: list[PositionalColor] = []

    for y in range(0, math.floor(h / cell_size[1]) * cell_size[1], cell_h):
        for x in range(0, math.floor(w / cell_size[0]) * cell_size[0], cell_w):
            block = img[y:y + cell_h, x:x + cell_w]
            processed_block = block_func(block)
            color = processed_block[0, 0]
            p_cs.append(PositionalColor(color, (x, y)))
            # Ensure processed block has the same size
            output[y:y + cell_h, x:x + cell_w] = processed_block

    output = output[0:math.floor(h / cell_size[1]) * cell_size[1],
                    0:math.floor(w / cell_size[0]) * cell_size[0]]
    return output, p_cs

def process_image_blocks_nonfixed_width(img: np.ndarray,
                                        p_cts: list[PositionalCharTemplate],
                                        block_func: Callable[[np.ndarray], np.ndarray]) \
        -> tuple[np.ndarray, list[PositionalColor]]:
    p_cs: list[PositionalColor] = []
    output = img.copy()

    for p_ct in p_cts:
        top_left = p_ct.top_left
        x, y = top_left
        cell_w, cell_h = p_ct.char_template.char_bound
        block = img[y:y + cell_h, x:x + cell_w]
        processed_block = block_func(block)
        color = processed_block[0, 0]
        p_cs.append(PositionalColor(color, (x, y)))
        # Ensure processed block has the same size
        output[y:y + cell_h, x:x + cell_w] = processed_block

    return output, p_cs

def average_color_block(block: np.ndarray) -> np.ndarray:
    avg_color = block.mean(axis=(0, 1), keepdims=True)
    return np.tile(avg_color, (block.shape[0], block.shape[1], 1)).astype(block.dtype)

def reassign_positional_colors(p_cs: list[PositionalColor], img: np.ndarray):
    p_cs.sort(key=lambda positional_color: positional_color.top_left)
    for p_c in p_cs:
        x = p_c.top_left[0]
        y = p_c.top_left[1]
        p_c.color = img[y, x]
