import os
import sys
from arg_util import ShadeArgUtil
from color_util import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../depth_shade')))
from gradient_writer import GradientWriter  # type: ignore

def test_color():
    resize_factor = 4
    thresholds_gamma = 0.3
    img = cv2.imread('../../resource/imgs/monalisa.jpg')

    color_img = img.copy()
    color_img = resize_nearest_neighbor(color_img, resize_factor)
    cell_size = (13, 22)
    color_converted = process_image_blocks(color_img, cell_size, average_color_block)[0]

    ascii_img = img.copy()
    ascii_img = resize_bilinear(ascii_img, resize_factor)
    ascii_img = smooth_colors(ascii_img, sigma_s=1, sigma_r=0.6)
    ascii_img = to_grayscale(ascii_img)
    h, w = ascii_img.shape[:2]

    templates = ShadeArgUtil.get_palette_json('../../resource/palette_files/palette_default.json')
    gradient_writer = GradientWriter(templates, max_workers=16)
    gradient_writer.assign_gradient_imgs(ascii_img, thresholds_gamma)

    ascii_img = gradient_writer.match()
    converted = blend_ascii_with_color(ascii_img, color_converted, 0.5)
    converted = copy_black_pixels(ascii_img, converted)
    os.makedirs('test', exist_ok=True)
    cv2.imwrite("test/test.png", converted)

def test_average_color_block():
    resize_factor = 4
    img = cv2.imread('../../resource/imgs/tsunami.jpg')
    img = resize_nearest_neighbor(img, resize_factor)
    cell_size = (13, 22)
    processed = process_image_blocks(img, cell_size, average_color_block)[0]
    os.makedirs('test', exist_ok=True)
    cv2.imwrite("test/test.png", processed)

def test():
    test_color()

if __name__ == '__main__':
    test()
