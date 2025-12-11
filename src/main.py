import os
import shutil
import time
import cv2
from grid_maker import slice_grid
from writer import match_slice
from util import invert_image_in_place, floor_fill_in_place, resize_nearest_neighbor_in_place

def main():
    sliced_save_path = 'sliced'
    input_path = './binary/bin_85.png'

    timeout = 5
    start = time.time()
    while os.path.exists(sliced_save_path):
        try:
            shutil.rmtree(sliced_save_path)
        except FileNotFoundError:
            break
        except PermissionError:
            pass  # folder locked, wait a bit
        time.sleep(0.05)

        if time.time() - start > timeout:
            raise TimeoutError("Folder deletion timed out")

    os.makedirs(sliced_save_path, exist_ok=True)
    resize_nearest_neighbor_in_place(input_path, 8)
    slice_grid(input_path, sliced_save_path)
    img = cv2.imread(input_path)
    h, w = img.shape[:2]
    match_slice('./sliced', './chars', w, h, 'ascii_art.png')
    invert_image_in_place('ascii_art.png')
    floor_fill_in_place('ascii_art.png')

if __name__ == '__main__':
    main()
