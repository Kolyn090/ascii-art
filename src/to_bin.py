import os.path

import cv2

def to_bin(input_path: str, threshold: int, save_folder: str):
    img = cv2.imread(input_path)

    # 1. Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 2. Apply binary threshold
    _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)

    cv2.imwrite(os.path.join(save_folder, f"bin_{threshold}.png"), binary)

def main():
    save_folder = './binary'
    input_path = './f_input/prof.jpg'
    os.makedirs(save_folder, exist_ok=True)
    for threshold in range(50, 205, 5):
        to_bin(input_path, threshold, save_folder)


if __name__ == '__main__':
    main()
