import os

import cv2
import numpy as np

def contour(img: np.ndarray, canny1: float, canny2: float):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(gray, canny1, canny2)
    kernel = np.ones((2, 2), np.uint8)
    edges = cv2.dilate(edges, kernel, iterations=1)
    edges = cv2.erode(edges, kernel, iterations=1)
    contour_img = cv2.bitwise_not(edges)
    return contour_img

def test():
    img_path = '../f_input/prof.jpg'
    img = cv2.imread(img_path)
    save_to_folder = True
    save_folder = 'test'
    if save_to_folder:
        os.makedirs(save_folder, exist_ok=True)

    canny1s = list(range(10, 80, 5))
    canny2s = list(range(100, 260, 10))
    for canny1 in canny1s:
        for canny2 in canny2s:
            c = contour(img, canny1, canny2)
            if save_to_folder:
                save_path = os.path.join(save_folder, f"contour_{canny1}_{canny2}.png")
                cv2.imwrite(save_path, c)

if __name__ == '__main__':
    test()
