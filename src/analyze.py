import cv2
import numpy as np

# These are the new midpoints of each segment
centers = [0, 30, 60, 90, 120, 150, 180]
tags = ['red', 'yellow', 'green', 'cyan', 'blue', 'magenta', 'red']

# Assume hsv_image is your HSV image and binary_image is your binary image
# both obtained from the same photo and already loaded as numpy arrays
def execute(binary_image, hsv_image):
    # Step 1: Find connected components in the binary image
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary_image, connectivity=8, ltype=cv2.CV_32S)

    print("------------------------")

    # Step 2: Iterate through the components to calculate additional statistics
    for label in range(1, num_labels):  # Start from 1 to skip the background
        # Create a mask for the current component
        component_mask = (labels == label).astype(np.uint8) * 255

        # Find contours for the component to calculate the perimeter
        contours, hierarchy = cv2.findContours(component_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        perimeter = cv2.arcLength(contours[0], True)

        # Calculate the mean hue value using the mask on the HSV image
        hue_channel = hsv_image[:, :, 0]  # Hue is the first channel
        masked_hue_values = np.extract(component_mask, hue_channel)
        mean_hue = np.mean(masked_hue_values)

        # Area is already available from the stats array
        area = stats[label, cv2.CC_STAT_AREA]

        # Ratio is around 4.pi for circles
        # Ratio is around 16 for squares (and other shapes)
        ratio = perimeter * perimeter / area
        color = 'unknown'

        for i in range(len(centers)):
            if abs(mean_hue - centers[i]) < 15 :
                color = tags[i]

        print(f"Component {label} - {centroids[label]}:")
        print(f"  Color: {color} - Ratio: {ratio}")
