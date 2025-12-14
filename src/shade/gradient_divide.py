import os
import cv2
import sys
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../util')))
from static import resize_bilinear, invert_image, increase_contrast, to_grayscale, smooth_colors  # type: ignore

def divide(img_gray: np.ndarray, n_levels: int) -> list[np.ndarray]:
    # h, w = img_gray.shape
    #
    # # 1. Compute gradient magnitude
    # gx = cv2.Sobel(img_gray, cv2.CV_64F, 1, 0, ksize=3)
    # gy = cv2.Sobel(img_gray, cv2.CV_64F, 0, 1, ksize=3)
    # grad_mag = cv2.magnitude(gx, gy)
    #
    # # 2. Smooth gradient slightly to avoid sparse zeros
    # grad_mag = cv2.GaussianBlur(grad_mag, (5, 5), 1.0)

    # 3. Normalize to 0..255
    grad_scaled = img_gray / img_gray.max() * 255.0

    # 4. Even thresholds
    # step = 255 / n_levels
    # thresholds = [i * step for i in range(n_levels + 1)]

    # n_levels thresholds
    linear = np.linspace(0, 1, n_levels + 1)

    # Apply a power >1 to bias toward high values
    gamma = 2.5  # higher gamma -> more emphasis on bright pixels
    nonlinear = linear ** gamma

    # Scale to 0..255
    thresholds = nonlinear * 255
    print(thresholds)

    level_images = []

    for i in range(n_levels):
        lower = thresholds[i]
        upper = thresholds[i + 1]

        # Mask in scaled gradient
        mask = ((grad_scaled >= lower) & (grad_scaled <= upper)).astype(np.uint8)

        # # Include black / white pixels explicitly
        # if i == 0:
        #     mask |= (img_gray == 0)
        # if i == n_levels - 1:
        #     mask |= (img_gray == 255)

        # Create RGBA: white background + alpha mask
        # rgb = np.ones((h, w, 3), dtype=np.uint8) * 255
        # alpha = np.zeros((h, w), dtype=np.uint8)
        # alpha[mask > 0] = 255

        # level_img = np.dstack([rgb, alpha])
        level_img = cv2.bitwise_and(img_gray, img_gray, mask=mask)
        level_img[level_img > 0] = 255
        # level_img = invert_image(level_img)
        level_images.append(level_img)

    return level_images

def test():
    factor = 16
    img_path = '../f_input/prof.jpg'
    save_folder = 'test'
    save_to_folder = True
    img = cv2.imread(img_path)
    img = increase_contrast(img, 2)
    img = to_grayscale(img)
    img = resize_bilinear(img, factor)
    # img = smooth_colors(img, sigma_s=60, sigma_r=0.08)

    cv2.imwrite("test.png", img)

    if save_to_folder:
        os.makedirs(save_folder, exist_ok=True)

    gradient_imgs = divide(img, 4)
    level = 0
    for gradient_img in gradient_imgs:
        save_path = os.path.join(save_folder, f'gradient_{level}.png')
        cv2.imwrite(save_path, gradient_img)
        level += 1

if __name__ == '__main__':
    test()
