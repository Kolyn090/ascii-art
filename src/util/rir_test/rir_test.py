import os
import sys
import cv2
from pathlib import Path
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from row_img_reconstruct import reconstruct  # type: ignore
from static import to_binary_strong, to_grayscale, increase_contrast  # type: ignore

def test():
    short_imgs: list[np.ndarray] = [cv2.imread(img_path) for img_path in find_all_png("jx_files/short_imgs")]
    short_imgs = [to_grayscale(img) for img in short_imgs]
    short_imgs = [to_binary_strong(img) for img in short_imgs]
    long_img: np.ndarray = cv2.imread("jx_files/long_img.png")
    long_img = increase_contrast(long_img, 2)
    long_img = to_grayscale(long_img)
    long_img = to_binary_strong(long_img)
    result = reconstruct(long_img, short_imgs)

    # os.makedirs("jx_files/verify", exist_ok=True)
    # count = 0
    # for short_img in short_imgs:
    #     cv2.imwrite(f"jx_files/verify/short_img_{count}.png", short_img)
    #     count += 1
    # cv2.imwrite("jx_files/verify/long_img.png", long_img)

    if result is not None:
        # os.makedirs("jx_files/result", exist_ok=True)
        seq, score = result
        seq = [img.astype(np.uint8) * 255 for img in seq]
        # count = 0
        # for img in seq:
        #     cv2.imwrite(f"jx_files/result/img_{count}.png", img)
        #     count += 1
        cv2.imwrite("jx_files/concat.png", concat_images_left_to_right(seq))

def concat_images_left_to_right(images: list[np.ndarray]) -> np.ndarray:
    """
    Concatenates a list of images (all same height) horizontally (left to right).
    """
    # check that all images have the same height
    heights = [img.shape[0] for img in images]
    if len(set(heights)) != 1:
        raise ValueError("All images must have the same height")

    # concatenate along the width axis
    concatenated = np.hstack(images)
    return concatenated

def find_all_png(root: str) -> list[str]:
    root = Path(root)
    png_files = list(root.rglob("*.png"))
    return [str(png_file) for png_file in png_files]

if __name__ == '__main__':
    test()
