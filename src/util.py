import cv2
import numpy as np


def invert_image_in_place(img_path: str):
    img = cv2.imread(img_path)
    img = cv2.bitwise_not(img)
    cv2.imwrite(img_path, img)

def floor_fill_in_place(img_path: str):
    img = cv2.imread(img_path)
    flood_img = img.copy()
    h, w = img.shape[:2]
    seed_point = (w - 1, h - 1)

    # Determine newVal depending on channels
    if len(img.shape) == 2:  # grayscale
        new_val = (0,)
    else:  # color
        new_val = (0, 0, 0)

    mask = np.zeros((h + 2, w + 2), np.uint8)
    cv2.floodFill(flood_img, mask, seedPoint=seed_point, newVal=new_val)
    cv2.imwrite(img_path, flood_img)

def resize_nearest_neighbor_in_place(img_path: str, factor: int):
    img = cv2.imread(img_path)  # color or grayscale
    scale = factor
    new_width = int(img.shape[1] * scale)
    new_height = int(img.shape[0] * scale)
    new_size = (new_width, new_height)
    resized = cv2.resize(img, new_size, interpolation=cv2.INTER_NEAREST)
    cv2.imwrite(img_path, resized)

def main():
    floor_fill_in_place('ascii_art.png')

if __name__ == '__main__':
    main()
