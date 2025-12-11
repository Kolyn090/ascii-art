import cv2
import numpy as np
import os.path
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

def write_character(input_path: str, char: str):
    text = char
    font_size = 24
    # Load a bold monospace font
    font = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", font_size)

    # Create image
    img = Image.new("RGB", (13, 22), "white")
    draw = ImageDraw.Draw(img)

    draw.text((0, 0), text, font=font, fill="black")

    img.save(os.path.join(input_path, f"char_{ord(text)}.png"))

def make_char_templates():
    input_path = "chars"
    os.makedirs(input_path, exist_ok=True)

    chars = [chr(i) for i in range(128)]

    for char in chars:
        write_character(input_path, char)

def match_slice(sliced_folder: str, char_template_folder: str, w: int, h: int, save_path: str):
    def find_top_left(slice_name: str) -> tuple[int, int]:
        slice_name = slice_name.replace("slice_", "")
        slice_name = slice_name.replace(".png", "")
        split_str = slice_name.split("_")
        return int(split_str[0]), int(split_str[1])

    empty_img = np.zeros((h, w, 3), dtype=np.uint8)
    slices = [str(f) for f in Path(sliced_folder).iterdir() if f.is_file() and f.suffix.lower() == ".png"]
    char_templates = [str(f) for f in Path(char_template_folder).iterdir() if f.is_file() and f.suffix.lower() == ".png"]
    for s in slices:
        top_left = find_top_left(os.path.basename(s))
        most_similar_template_path = find_most_similar(s, char_templates)
        small_img = cv2.imread(most_similar_template_path)
        bottom_right_y = top_left[1] + small_img.shape[0]
        bottom_right_x = top_left[0] + small_img.shape[1]
        print(top_left)
        empty_img[top_left[1]:bottom_right_y, top_left[0]:bottom_right_x] = small_img
    cv2.imwrite(save_path, empty_img)

def find_most_similar(img_path: str, template_paths: list[str]) -> str:
    best_score = -1
    best_template = None

    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    h, w = img.shape

    for tpl_path in template_paths:
        tpl = cv2.imread(tpl_path, cv2.IMREAD_GRAYSCALE)
        if tpl is None:
            continue

        # Resize template to match target image
        tpl_resized = cv2.resize(tpl, (w, h), interpolation=cv2.INTER_NEAREST)

        score = np.sum(img == tpl_resized) / (w * h)

        if score > best_score:
            best_score = score
            best_template = tpl_path
    return best_template

def main():
    # make_char_templates()
    match_slice('./sliced', './chars', 1200, 1200, 'ascii_art.png')

if __name__ == '__main__':
    main()
