import os.path
import cv2
import numpy as np

def draw_reference_grid(input_path: str, save_path: str):
    img = cv2.imread(input_path)
    h, w = img.shape[:2]

    cell_w = 13
    cell_h = 22
    thick   = 2
    color = (255, 0, 0)

    grid = np.zeros_like(img)

    # draw vertical lines
    for x in range(0, w, cell_w):
        grid[:, x:x+thick] = color

    # draw horizontal lines
    for y in range(0, h, cell_h):
        grid[y:y+thick, :] = color

    # overlay the grid
    mask = grid.sum(axis=2) > 0
    img[0:h-1, 0:w-1][mask[1:, 1:]] = grid[1:, 1:][mask[1:, 1:]]

    cv2.imwrite(save_path, img)

def slice_grid(input_path: str, save_folder: str):
    img = cv2.imread(input_path)
    h, w = img.shape[:2]

    cell_w = 13
    cell_h = 22

    i = -1
    while i < w:
        j = -1
        while j < h:
            top_left = (i+1, j+1)
            bottom_right = (i+cell_w, j+cell_h)
            if in_range(top_left, bottom_right, w, h):
                save_path = os.path.join(save_folder, f"slice_{top_left[0]}_{top_left[1]}.png")
                cropped = img[top_left[1]:bottom_right[1]+1, top_left[0]:bottom_right[0]+1]
                cv2.imwrite(save_path, cropped)
            j += cell_h
        i += cell_w

def in_range(top_left, bottom_right, w, h):
    return top_left[0] >= 0 and top_left[1] >= 0 and bottom_right[0] < w and bottom_right[1] < h

def main():
    save_path = "sliced"
    os.makedirs(save_path, exist_ok=True)
    # draw_reference_grid('prof_10_100_contour.png', 'grid_output.png')
    slice_grid('prof_10_100_contour.png', save_path)

if __name__ == '__main__':
    main()
