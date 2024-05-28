import cv2
import numpy as np
from collections import Counter

blank_image = np.zeros((480, 640), dtype=np.uint8)

def count_ranges(values, step=20):
    """
    Count the number of occurrences in each range for a list of values.
    
    :param values: List of integer values.
    :param step: Range size for grouping values.
    :return: None
    """
    # Group values by range
    range_counts = Counter((x // step) * step for x in values)

    # Print the counts for each range
    for i in range(0, 360, step):
        # Calculate the range string, e.g., "[0, 10)"
        range_str = f"[{i}, {i + step})"
        # Print the count for the range, defaulting to 0 if not in the dictionary
        print(f"{range_str}: {range_counts.get(i, 0)}")

def split_hsv(img):
    # Split into individual channels
    hue, saturation, value = cv2.split(img)

    # Display each channel
    cv2.imshow("Hue Channel", hue)
    cv2.imshow("Saturation Channel", saturation)
    cv2.imshow("Value Channel", value)

current_step_id = 0
steps = [blank_image]
pressed_key = None

def display_steps():
    global current_step_id, steps, pressed_key
    cv2.imshow('Steps', steps[current_step_id])
    pressed_key = cv2.waitKey(1) & 0xFF

def set_steps(new_steps):
    global steps
    steps = new_steps
    display_steps()

def next_step():
    global current_step_id, steps
    current_step_id = (current_step_id + 1) % len(steps)

def prev_step():
    global current_step_id, steps
    current_step_id = (current_step_id - 1) % len(steps)

def switch_step():
    global pressed_key
    if (pressed_key == 57):
        next_step()
    elif (pressed_key == 56):
        prev_step()
    display_steps()
