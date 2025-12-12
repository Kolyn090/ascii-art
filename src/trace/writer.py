import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from concurrent.futures import ThreadPoolExecutor

from slicer import Cell, Slicer

class CharTemplate:
    def __init__(self):
        self.char: str | None = None
        self.template: np.ndarray | None = None

class Writer:
    def __init__(self):
        self.font_size = 24
        self.font = 'C:/Windows/Fonts/consolab.ttf'
        self.char_templates: list[CharTemplate] = []

    def match_cells(self, cells: list[Cell],
                    w: int, h: int) -> np.ndarray:
        result_img = np.zeros((h, w, 3), dtype=np.uint8)
        with ThreadPoolExecutor(max_workers=8) as executor:
            list(executor.map(lambda cell: self.paste_to_img(cell, result_img), cells))
        return result_img

    def paste_to_img(self, cell: Cell, result_img: np.ndarray):
        most_similar = self.get_most_similar(cell)
        template = most_similar.template
        top_left = cell.top_left
        bottom_right_y = top_left[1] + template.shape[0]
        bottom_right_x = top_left[0] + template.shape[1]
        result_img[top_left[1]:bottom_right_y, top_left[0]:bottom_right_x] = template

    def get_most_similar(self, cell: Cell) -> CharTemplate:
        if len(self.char_templates) == 0:
            raise Exception("You have not assigned any template yet.")

        best_score = -1
        best_template = None

        img = cell.img
        h, w = img.shape[:2]

        for char_template in self.char_templates:
            template = char_template.template
            template_resized = cv2.resize(template, (w, h), interpolation=cv2.INTER_NEAREST)
            score = np.sum(img == template_resized) / (w * h)
            if score > best_score:
                best_score = score
                best_template = char_template
        return best_template

    def assign_char_templates(self, chars: list[str]) -> list[CharTemplate]:
        font = ImageFont.truetype(self.font, self.font_size)
        result = []
        for char in chars:
            img = Image.new("RGB", (13, 22), "white")
            draw = ImageDraw.Draw(img)
            draw.text((0, 0), char, font=font, fill="black")
            char_template = CharTemplate()
            char_template.char = char
            char_template.template = np.array(img)
            result.append(char_template)
        self.char_templates = result
        return result

def test_char_templates():
    save_to_folder = False
    save_folder = 'chars'
    chars = [chr(i) for i in range(128)]
    if save_to_folder:
        os.makedirs(save_folder, exist_ok=True)

    writer = Writer()
    char_templates = writer.assign_char_templates(chars)
    for char_template in char_templates:
        char = char_template.char
        template = char_template.template
        print(char)
        save_path = os.path.join(save_folder, f"char_{ord(char)}.png")
        if save_to_folder:
            cv2.imwrite(save_path, template)

def test_match_cells():
    img_path = '../binary/bin_85.png'
    save_folder = 'test'
    save_to_folder = True
    img = cv2.imread(img_path)
    h, w = img.shape[:2]
    chars = [chr(i) for i in range(128)]

    if save_to_folder:
        os.makedirs(save_folder)

    slicer = Slicer()
    cells = slicer.slice(img, (13, 22))
    writer = Writer()
    writer.assign_char_templates(chars)
    converted = writer.match_cells(cells, w, h)
    cv2.imwrite(os.path.join(save_folder, 'converted.png'), converted)

if __name__ == '__main__':
    test_match_cells()
