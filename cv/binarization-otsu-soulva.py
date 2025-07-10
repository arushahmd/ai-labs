import os
import shutil

import cv2
import doxapy
import numpy as np


def get_gray_image(image):
    """
    Convert the given image to grayscale.

    Parameters:
        image (numpy.ndarray): Input image to be converted to grayscale.

    Returns:
        numpy.ndarray: Grayscale image.
    """
    if len(image.shape) == 3:  # Check if the image is in color (3 channels)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray_image = image  # If the image is already grayscale, return as is
    return gray_image


# Function for Sauvola binarization
def sauvola_binarization(image, window_size=94, k=0.3):
    """
    Perform Sauvola binarization on the given image.

    Parameters:
        image (numpy.ndarray): Grayscale image to be binarized.
        window_size (int): Size of the sliding window for adaptive thresholding.
        k (float): Constant to adjust the threshold sensitivity.

    Returns:
        numpy.ndarray: Binarized image.
    """
    gray_img = get_gray_image(image)
    binary_image = np.empty(gray_img.shape, gray_img.dtype)

    sauvola = doxapy.Binarization(doxapy.Binarization.Algorithms.SAUVOLA)
    sauvola.initialize(gray_img)
    sauvola.to_binary(binary_image, {"window": window_size, "k": k})

    return binary_image


# Function for Otsu binarization
def otsu_binarization(image, threshold_val):
    """
    Perform Otsu binarization on the given image.

    Parameters:
        image (numpy.ndarray): Grayscale image to be binarized.
        threshold_val (int): Otsu threshold value.

    Returns:
        numpy.ndarray: Binarized image.
    """
    gray_img = get_gray_image(image)
    _, binary_image = cv2.threshold(gray_img, threshold_val, 255, cv2.THRESH_BINARY)
    return binary_image


def save_image_with_label(binary_image, label, filename):
    """
    Save the binarized image with a label in the filename.

    Parameters:
        binary_image (numpy.ndarray): Binarized image.
        label (str): Label for the threshold/parameter values.
        filename (str): File path to save the image.
    """
    # Convert the binary image to 3 channels (if it's grayscale)
    if len(binary_image.shape) == 2:
        binary_image = cv2.cvtColor(binary_image, cv2.COLOR_GRAY2BGR)

    # Save the result with label in the filename
    cv2.imwrite(filename, binary_image)


def create_or_clear_directory(directory):
    """
    Create a directory if it doesn't exist or clear it if it already exists.

    Parameters:
        directory (str): Path of the directory to create or clear.

    Returns:
        None
    """
    if os.path.exists(directory):
        # Clear the existing directory
        shutil.rmtree(directory)
    # Create the directory
    os.makedirs(directory)


def binarization_comparison(image, otsu_thresholds, sauvola_params, otsu_flag=False, sauvola_flag=False):
    """
    Compare the results of Sauvola and Otsu binarization with different parameters.

    Parameters:
        image (numpy.ndarray): The input image to be binarized.
        otsu_flag (bool): Flag to save Otsu binarization results.
        sauvola_flag (bool): Flag to save Sauvola binarization results.

    Returns:
        None
    """

    # Create or clear the directories for saving results
    if otsu_flag:
        otsu_dir = 'output/otsu'
        create_or_clear_directory(otsu_dir)

    if sauvola_flag:
        sauvola_dir = 'output/sauvola'
        create_or_clear_directory(sauvola_dir)

    # Perform Otsu binarization with multiple threshold values
    if otsu_flag:
        for threshold_val in otsu_thresholds:
            otsu_results = otsu_binarization(image, threshold_val)
            otsu_filename = f'{otsu_dir}/otsu_binarization_threshold{threshold_val}.jpg'
            save_image_with_label(otsu_results, f"Otsu Threshold: {threshold_val}", otsu_filename)

    # Perform Sauvola binarization with multiple parameter combinations
    if sauvola_flag:
        for params in sauvola_params:
            sauvola_result = sauvola_binarization(image, window_size=params['window_size'], k=params['k'])
            sauvola_filename = f'{sauvola_dir}/sauvola_binarization_w{params["window_size"]}_k{params["k"]}.jpg'
            label = f"Window: {params['window_size']} K: {params['k']}"
            save_image_with_label(sauvola_result, label, sauvola_filename)


# Load the image
image = cv2.imread('Sharooh-Kalam-e-Iqbal_pg37_ln5.jpg')

# Define multiple threshold values for Otsu binarization
otsu_thresholds = [30, 60, 90, 120, 150, 180]

# Define multiple Sauvola parameters (with large differences for k and window size)

sauvola_params = [
    {'window_size': 10, 'k': 0.4},
    {'window_size': 15, 'k': 0.4},
    {'window_size': 20, 'k': 0.4},
    {'window_size': 25, 'k': 0.4},
    {'window_size': 32, 'k': 0.4},
    # {'window_size': 32, 'k': 0.6}
]

if __name__ == "__main__":
    # Check if the image was loaded properly
    if image is None:
        print("Error: Image not loaded. Check the file path.")
    else:
        # Set flags to control which binarizations to run
        otsu_flag = True  # Set to True if you want to save Otsu results
        sauvola_flag = True  # Set to True if you want to save Sauvola results

        # Run the binarization comparison
        binarization_comparison(image, otsu_thresholds, sauvola_params, otsu_flag=otsu_flag, sauvola_flag=sauvola_flag)
