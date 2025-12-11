import os
import cv2
import numpy as np

def contour(input_path: str, save_path: str,
            canny1: float, canny2: float):
    # Load image
    img = cv2.imread(input_path)

    # Grayscale + blur
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5,5), 0)

    # Edge detection
    edges = cv2.Canny(gray, canny1, canny2)

    # Optional: thicken edges slightly
    kernel = np.ones((2,2), np.uint8)
    edges = cv2.dilate(edges, kernel, iterations=1)
    edges = cv2.erode(edges, kernel, iterations=1)

    # Invert for white background
    contour_img = cv2.bitwise_not(edges)

    cv2.imwrite(save_path, contour_img)

def main():
    input_path = './f_input/prof.jpg'
    save_name_prefix = 'prof'
    output_path = './f_output'
    os.makedirs(output_path, exist_ok=True)
    canny1s = list(range(10, 80, 5))
    canny2s = list(range(100, 260, 10))
    for canny1 in canny1s:
        for canny2 in canny2s:
            save_path = os.path.join(output_path, f"{save_name_prefix}_{canny1}_{canny2}_contour.png")
            contour(input_path, save_path, canny1, canny2)

if __name__ == '__main__':
    main()
