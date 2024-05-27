from collections import Counter

import image_processing.process as img_process
import computer_vision.tools as cv_tools;

def identify_object():
    return img_process.detect_movement()

def get_object():
    [frame_processed, frame_hsv] = img_process.get_filtered_frame()

    object_mask = cv_tools.find_largest_component_under_threshold(frame_processed)
    if (object_mask is not None):
        return cv_tools.get_component_color_and_shape(object_mask, frame_hsv)

    return

def get_mode_object():
    color = 'red'
    shape = 'square'
    return (color, shape)
    color_results = []
    shape_results = []

    # Call get_object 10 times
    for _ in range(10):
        result = get_object()
        if result is not None:
            color, shape = result
            color_results.append(color)
            shape_results.append(shape)

    # Calculate the mode for color and shape
    color_counter = Counter(color_results)
    shape_counter = Counter(shape_results)

    # Find the most common color and shape and their counts
    color, color_count = color_counter.most_common(1)[0] if color_counter else (None, 0)
    shape, shape_count = shape_counter.most_common(1)[0] if shape_counter else (None, 0)

    # Check if the mode count meets the minimum requirement of 5
    if color_count >= 5 and shape_count >= 5:
        return color, shape
    return None
