import os
import sys
import cv2

from nonfixed_width_writer import NonFixedWidthWriter

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../util')))
from static import (to_binary_strong, to_grayscale, increase_contrast,  # type: ignore
                    resize_nearest_neighbor, to_binary_middle, smooth_colors,  # type: ignore
                    invert_image)  # type: ignore
from arg_util import ShadeArgUtil  # type: ignore

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../depth_shade')))
from gradient_divide import divide  # type: ignore

def test():
    os.makedirs("jx_files", exist_ok=True)
    max_workers = 16
    resize_factor = 8
    contrast_factor = 1
    thresholds_gamma = 0.17
    sigma_s = 1
    sigma_r = 0.6

    image = cv2.imread("../../resource/f_input/ultraman-nexus.png")
    image = resize_nearest_neighbor(image, resize_factor)
    image = increase_contrast(image, contrast_factor)
    image = smooth_colors(image, sigma_s, sigma_r)
    image = to_grayscale(image)

    palettes = ShadeArgUtil.get_palette_json('../../resource/palette_files/jx_files/palette_test.json')
    gradient_imgs = divide(image, len(palettes), thresholds_gamma)
    nfww = NonFixedWidthWriter(palettes, gradient_imgs, max_workers)

    print(nfww.char_weights)

    # count = 1
    # for img in nfww.transitional_imgs:
    #     cv2.imwrite(f"jx_files/transition_{count}.png", img)
    #     count += 1

    width = resize_factor * image.shape[:2][1]

    # converted = nfww.stack(width)
    # cv2.imwrite(f"jx_files/final_img.png", converted)

    converted_so = nfww.stack_overlay(width)
    count = 1
    for img in converted_so:
        cv2.imwrite(f"jx_files/final_img_so_{count}.png", img)
        count += 1

if __name__ == '__main__':
    test()
