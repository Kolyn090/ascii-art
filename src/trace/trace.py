import os
import sys
import cv2
import argparse

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../util')))
from slicer import Slicer  # type: ignore
from writer import Writer  # type: ignore
from arg_util import TraceArgUtil  # type: ignore
from static import resize_nearest_neighbor, resize_bilinear  # type: ignore

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_path', type=str)
    parser.add_argument('--save_path', type=str, default='ascii_art.png')
    parser.add_argument('--factor', type=float, default=1)
    parser.add_argument('--chars', type=str, default='ascii')
    parser.add_argument('--font', type=str, default='C:/Windows/Fonts/consolab.ttf')
    parser.add_argument('--font_size', type=int, default=24)
    parser.add_argument('--char_bound_width', type=int, default=13)
    parser.add_argument('--char_bound_height', type=int, default=22)
    parser.add_argument('--resize_method', type=str, default='nearest_neighbor')
    args = parser.parse_args()

    factor = args.factor
    chars = TraceArgUtil.get_chars(args.chars)
    font_size = args.font_size
    img_path = args.image_path
    save_path = args.save_path
    img = cv2.imread(img_path)
    img = TraceArgUtil.resize(args.resize_method, img, factor)
    h, w = img.shape[:2]

    slicer = Slicer()
    cells = slicer.slice(img, (args.char_bound_width, args.char_bound_height))
    writer = Writer()
    writer.font = args.font
    writer.font_size = font_size
    writer.assign_char_templates(chars)
    converted = writer.match_cells(cells, w, h)[0]
    cv2.imwrite(save_path, converted)

if __name__ == '__main__':
    main()
