import cv2
import numpy as np
from computer_vision.tools import get_component_color, get_component_shape

# Assume hsv_image is your HSV image and binary_image is your binary image
# both obtained from the same photo and already loaded as numpy arrays
def display_shape_color_for_all(binary_image, hsv_image):
    # Step 1: Find connected components in the binary image
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary_image, connectivity=8, ltype=cv2.CV_32S)

    print("------------------------")
    # Step 2: Iterate through the components to calculate additional statistics
    for label in range(1, num_labels):  # Start from 1 to skip the background
        # Create a mask for the current component
        component_mask = (labels == label).astype(np.uint8) * 255

        color = get_component_color(hsv_image, component_mask)
        shape = get_component_shape(component_mask)
        area = stats[label, cv2.CC_STAT_AREA]

        print(f"Component {label} - {centroids[label]}:")
        print(f"  Color: {color} - Shape: {shape} - Area: {area}")