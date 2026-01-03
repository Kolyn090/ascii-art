import numpy as np
from PIL import Image
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
    num = max(num, 0)

    if img.ndim == 2:  # grayscale
        h, w = img.shape
        out = np.full((h, w + 2 * num), color, dtype=img.dtype)
        out[:, num:num + w] = img

    else:  # color
        h, w, c = img.shape
        if np.isscalar(color):
            color = (color,) * c
        out = np.full((h, w + 2 * num, c), color, dtype=img.dtype)
        out[:, num:num + w, :] = img

    return out

def np_pad_rows(img: np.ndarray, num: int, color=255) -> np.ndarray:
    num = max(num, 0)

    if img.ndim == 2:  # grayscale
        h, w = img.shape
        out = np.full((h + 2 * num, w), color, dtype=img.dtype)
        out[num:num + h, :] = img

    else:  # color
        h, w, c = img.shape
        if np.isscalar(color):
            color = (color,) * c
        out = np.full((h + 2 * num, w, c), color, dtype=img.dtype)
        out[num:num + h, :, :] = img

    return out

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
    test()
