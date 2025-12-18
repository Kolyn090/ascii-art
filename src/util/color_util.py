import os
import cv2
import numpy as np
from typing import Callable
from static import resize_nearest_neighbor

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

    return output

def average_color_block(block: np.ndarray) -> np.ndarray:
    avg_color = block.mean(axis=(0, 1), keepdims=True)
    return np.tile(avg_color, (block.shape[0], block.shape[1], 1)).astype(block.dtype)

def test():
    resize_factor = 4
    img = cv2.imread('../../resource/imgs/tsunami.jpg')
    img = resize_nearest_neighbor(img, resize_factor)
    cell_size = (13, 22)  # width x height
    processed = process_image_blocks(img, cell_size, average_color_block)
    os.makedirs('test', exist_ok=True)
    cv2.imwrite("test/test.png", processed)

if __name__ == '__main__':
    test()
