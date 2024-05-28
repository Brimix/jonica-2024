import cv2
import numpy as np

def mean_hue_value(hues):
    """
    Calculate the mean hue value from a list of hue by converting each hue to an angle in the
    range [0, 360) and then to a unit vector, summing them, and then computing the angle of the result.

    :param hues: List of angles in degrees.
    :return: Mean hue value in degrees.
    """
    # Convert hues to degree angles and then to radians for computation
    angles = [(hue * 2) % 360 for hue in hues]
    radians = np.radians(angles)

    # Compute sum of unit vectors
    sum_sin = np.sum(np.sin(radians))
    sum_cos = np.sum(np.cos(radians))

    # Calculate the angle of the resultant vector
    mean_angle_radians = np.arctan2(sum_sin, sum_cos)

    # Convert the mean angle from radians back to degrees
    mean_angle_degrees = np.degrees(mean_angle_radians) % 360

    # Convert back to hue amd return
    return mean_angle_degrees / 2

def get_component_color(hsv_image, component_mask):
    # These are the  central points of each color
    centers = [0, 15, 30, 60, 90, 120, 150, 180]
    colors = ['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'magenta', 'red']

    # Calculate the mean hue value using the mask on the HSV image
    hue_channel = hsv_image[:, :, 0]  # Hue is the first channel
    masked_hue_values = np.extract(component_mask, hue_channel)
    mean_hue = mean_hue_value(masked_hue_values)

    color = 'unknown'
    colorDistance = 181

    for i in range(len(centers)):
        distance = abs(mean_hue - centers[i])
        if distance < colorDistance :
            color = colors[i]
            colorDistance = distance

    return color

def get_component_shape(component_mask):
    # Find contours for the component to calculate the perimeter
    contours, hierarchy = cv2.findContours(component_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    perimeter = cv2.arcLength(contours[0], True)
    area = cv2.contourArea(contours[0])

    # Ratio is around 4.pi for circles and 16 for squares (and other shapes)
    rho = (perimeter*perimeter) / area
    ratio = rho / (4*np.pi)
    # print(f"  Ratio: ({ratio})")

    if (ratio < 1.30):
        return 'circle'
    else:
        return 'square'

def find_largest_component_under_threshold(binary_image):
    """
    Identifies connected components in the binary image, calculates the area for each,
    and returns the mask of the biggest object as long as its area does not exceed the defined threshold.

    :param binary_image: Binary image where objects are identified as foreground (255) against the background (0).
    :return: Mask of the largest object under the threshold or None if no such object exists.
    """

    MIN_AREA_THRESHOLD = 5000
    MAX_AREA_THRESHOLD = 40000

    # Step 1: Find connected components with statistics in the binary image
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary_image, connectivity=8, ltype=cv2.CV_32S)
    
    # Step 2: Initialize variables to find the largest component under the threshold
    max_area = MIN_AREA_THRESHOLD
    largest_component_mask = None

    # Step 3: Iterate through the components to find the largest under threshold
    for label in range(1, num_labels):  # Skip label 0 as it's the background
        area = stats[label, cv2.CC_STAT_AREA]

        if (area > MAX_AREA_THRESHOLD):
            return None
        
        if area > max_area:
            max_area = area
            # Create a mask for the current largest component
            largest_component_mask = (labels == label).astype(np.uint8) * 255

    # Return the mask of the largest component if found
    # print('Area', max_area)
    return largest_component_mask

def get_component_color_and_shape(component_mask, hsv_image):
    """
    Calculate color and shape for the provided component mask.

    :param component_mask: Binary mask of the component to analyze.
    :param hsv_image: HSV image from which color is to be extracted.
    :return: A tuple containing the color and shape of the component.
    """
    color = get_component_color(hsv_image, component_mask)
    shape = get_component_shape(component_mask)
    return (color, shape)