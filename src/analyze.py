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

def get_color(hsv_image, component_mask):
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

def get_shape(component_mask, stats, label):
    # Find contours for the component to calculate the perimeter
    contours, hierarchy = cv2.findContours(component_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    perimeter = cv2.arcLength(contours[0], True)

    # Area is already available from the stats array
    area = stats[label, cv2.CC_STAT_AREA]

    # Perimeter of a circle calculated from area
    circle_perimeter = np.sqrt(4 * np.pi * area)

    # Ratio is around 4.pi for circles and 16 for squares (and other shapes)
    ratio = perimeter / circle_perimeter

    if (ratio < 1.12):
        return 'circle'
    else:
        return 'square'


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

        color = get_color(hsv_image, component_mask)
        shape = get_shape(component_mask, stats, label)

        print(f"Component {label} - {centroids[label]}:")
        # print(f"  Color: {color} ({mean_hue}) - Tag: {tag} ({ratio})")
        print(f"  Color: {color} - Shape: {shape}")
