import os

import cv2
import numpy as np
from PIL import Image, ImageFont, ImageDraw

from slicer import Cell

def pil_pad_columns(img: Image.Image, num: int, color="white") -> Image.Image:
    num = max(num, 0)
    w, h = img.size
    new_img = Image.new(img.mode, (w + 2 * num, h), color)
    new_img.paste(img, (num, 0))
    return new_img

def pil_pad_rows(img: Image.Image, num: int, color="white") -> Image.Image:
    num = max(num, 0)
    w, h = img.size
    new_img = Image.new(img.mode, (w, h + 2 * num), color)
    new_img.paste(img, (num, 0))
    return new_img

def np_pad_columns(img: np.ndarray, num: int, color=255) -> np.ndarray:
    return np_pad(img, top=num, bottom=num, color=color)

def np_pad_rows(img: np.ndarray, num: int, color=255) -> np.ndarray:
    return np_pad(img, left=num, right=num, color=color)

def np_pad(
        img: np.ndarray,
        *,
        top: int = 0,
        bottom: int = 0,
        left: int = 0,
        right: int = 0,
        color=255
    ) -> np.ndarray:
    h, w = img.shape[:2]

    # --- Crop first (negative values) ---
    y0 = max(-top, 0)
    y1 = h - max(-bottom, 0)
    x0 = max(-left, 0)
    x1 = w - max(-right, 0)

    if y0 >= y1 or x0 >= x1:
        raise ValueError("Cropping removed entire image")

    img = img[y0:y1, x0:x1]

    # --- Pad second (positive values) ---
    top = max(top, 0)
    bottom = max(bottom, 0)
    left = max(left, 0)
    right = max(right, 0)

    h, w = img.shape[:2]

    if img.ndim == 2:  # grayscale
        out = np.full(
            (h + top + bottom, w + left + right),
            color,
            dtype=img.dtype,
        )
        out[top:top + h, left:left + w] = img

    else:  # color
        c = img.shape[2]
        if np.isscalar(color):
            color = (color,) * c

        out = np.full(
            (h + top + bottom, w + left + right, c),
            color,
            dtype=img.dtype,
        )
        out[top:top + h, left:left + w, :] = img

    return out

# This is outer padding
# Unused
def pad_cells(cells: list[Cell], pad: tuple[int, int], pad_color: int) -> tuple[list[Cell], int, int]:
    curr_top_left_x = 0
    curr_top_left_y = -2*pad[1] - cells[0].img.shape[0]
    new_cells = []
    last_cell = None
    highest_x = -1
    highest_y = -1
    for cell in cells:
        cell_copy = Cell(cell.top_left, cell.img.copy())
        top_left = cell.top_left
        curr_x = top_left[0]
        if curr_x == 0:
            curr_top_left_x = 0
            curr_top_left_y += 2*pad[1] + cell_copy.img.shape[0]
        cell_img = cell_copy.img
        cell_img = np_pad_rows(cell_img, pad[1], pad_color)
        cell_copy.img = np_pad_columns(cell_img, pad[0], pad_color)
        top_left = (curr_top_left_x, curr_top_left_y)
        curr_top_left_x = curr_top_left_x + cell_copy.img.shape[1]
        cell_copy.top_left = top_left
        new_cells.append(cell_copy)
        if top_left[0] > highest_x or top_left[1] > highest_y:
            last_cell = cell_copy
    if last_cell is None:
        return [], 0, 0
    return (new_cells,
            last_cell.top_left[1] + last_cell.img.shape[0],
            last_cell.top_left[0] + last_cell.img.shape[1])

def test_padding():
    color = 255

    os.makedirs('jx_files', exist_ok=True)
    start = (0, 0)
    bound = (24, 24)
    word = 'a'
    font_path = "C:/Windows/Fonts/consolab.ttf"
    font_size = 24
    font = ImageFont.truetype(font_path, font_size)
    img = Image.new("RGB", bound, "white")
    draw = ImageDraw.Draw(img)
    draw.text(start, word, font=font, fill="black")

    img = np.array(img)
    cv2.imwrite("jx_files/word_a.png", img)

    def make_img(name: str, top=0, bottom=0, left=0, right=0):
        img1 = np_pad(img, top=top, bottom=bottom, left=left, right=right, color=color)
        cv2.imwrite(f"jx_files/{name}.png", img1)

    make_img("pad_top_10", top=10)
    make_img("crop_top_10", top=-10)
    make_img("pad_rows_5", top=5, bottom=5)
    make_img("pad_all_5", top=5, bottom=5, left=5, right=5)
    make_img("crop_all_5", top=-5, bottom=-5, left=-5, right=-5)
    make_img("crop_too_much", top=-25)

def test():
    cells = [
        Cell((0, 0), np.full((22, 13, 3), 255, dtype=np.uint8)),
        Cell((13, 0), np.full((22, 13, 3), 255, dtype=np.uint8)),
        Cell((26, 0), np.full((22, 13, 3), 255, dtype=np.uint8)),
        Cell((0, 22), np.full((22, 13, 3), 255, dtype=np.uint8)),
        Cell((13, 22), np.full((22, 13, 3), 255, dtype=np.uint8)),
        Cell((26, 22), np.full((22, 13, 3), 255, dtype=np.uint8)),
        Cell((0, 44), np.full((22, 13, 3), 255, dtype=np.uint8)),
        Cell((13, 44), np.full((22, 13, 3), 255, dtype=np.uint8)),
        Cell((26, 44), np.full((22, 13, 3), 255, dtype=np.uint8)),
    ]
    cells = sorted(cells, key=lambda obj: (obj.top_left[1], obj.top_left[0]))
    new_cells, h, w = pad_cells(cells, (3, 2), 255)
    for cell in new_cells:
        print(cell.top_left, cell.img.shape[:2])
    print(f"h: {h}, w: {w}")

if __name__ == '__main__':
    test_padding()
