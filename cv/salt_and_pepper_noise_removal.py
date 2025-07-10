import cv2
import numpy as np
import os


def add_salt_and_pepper_noise(image, salt_prob=0.02, pepper_prob=0.02):
    noisy_image = np.copy(image)
    total_pixels = image.size
    salt_count = int(total_pixels * salt_prob)
    pepper_count = int(total_pixels * pepper_prob)

    # Add salt noise
    coords = [np.random.randint(0, i - 1, salt_count) for i in image.shape]
    noisy_image[coords[0], coords[1]] = 255  # White

    # Add pepper noise
    coords = [np.random.randint(0, i - 1, pepper_count) for i in image.shape]
    noisy_image[coords[0], coords[1]] = 0  # Black

    return noisy_image


def remove_noise_median(image):
    return cv2.medianBlur(image, 3)


def remove_noise_gaussian(image):
    return cv2.GaussianBlur(image, (3, 3), 0)


def remove_noise_bilateral(image):
    return cv2.bilateralFilter(image, 9, 75, 75)


def save_image(image, path):
    cv2.imwrite(path, image)


def main():
    input_image_path = "Sharooh-Kalam-e-Iqbal_pg37_ln5.jpg"  # Replace with your image path
    output_dir = "output/sat_and_pepper"
    os.makedirs(output_dir, exist_ok=True)

    # Read the image
    image = cv2.imread(input_image_path, cv2.IMREAD_GRAYSCALE)

    # Add salt and pepper noise
    noisy_image = add_salt_and_pepper_noise(image)
    save_image(noisy_image, os.path.join(output_dir, "noisy_image.jpg"))

    # Denoising
    denoised_median = remove_noise_median(noisy_image)
    save_image(denoised_median, os.path.join(output_dir, "denoised_median.jpg"))

    denoised_gaussian = remove_noise_gaussian(noisy_image)
    save_image(denoised_gaussian, os.path.join(output_dir, "denoised_gaussian.jpg"))

    denoised_bilateral = remove_noise_bilateral(noisy_image)
    save_image(denoised_bilateral, os.path.join(output_dir, "denoised_bilateral.jpg"))
    print("Images saved in:", output_dir)


if __name__ == "__main__":
    main()
