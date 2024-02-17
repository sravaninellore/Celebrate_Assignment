# -*- coding: utf-8 -*-
"""Untitled22.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1wmz08zSPEffmM2mYmoofPxsOzLyLJjmL
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
# Read the image
image_path = 'ab.png' # Assuming "ab.png" is in the current directory
# Read the image with alpha channel
image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
# Check if the image is loaded successfully
if image is None:
    print("Error: Unable to load image. Please check the file path.")
else:
     # If the image has an alpha channel, extract the alpha channel and create a 3-channel image
    if image.shape[2] == 4:
        bgr_image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
    else:
        bgr_image = image
        # Create a mask initialized with zeros
    mask = np.zeros(bgr_image.shape[:2], np.uint8)
    # Specify the background and foreground models
    background_model = np.zeros((1, 65), np.float64)
    foreground_model = np.zeros((1, 65), np.float64)
    # Define the rectangle encompassing the foreground object 
    # Refine the rectangle to better fit the foreground object
    rectangle = (150, 50, bgr_image.shape[1] - 50, bgr_image.shape[0] - 50)
    # Apply GrabCut algorithm to segment the foreground from the background
    cv2.grabCut(bgr_image, mask, rectangle, background_model, foreground_model, 5, cv2.GC_INIT_WITH_RECT)
    # Create a mask where all probable background pixels are marked with 0, and the probable foreground pixels are marked with 1
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
    # Apply the mask to the original image
    result = bgr_image * mask2[:, :, np.newaxis]
    # Replace the background with white
    result[mask2 == 0] = [255, 255, 255]
    # Display the result
    plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
    plt.title('Background Removed')
    plt.axis('off')
    plt.show()
