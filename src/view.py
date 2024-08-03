import cv2
import numpy as np

blank_image = np.zeros((480, 640), dtype=np.uint8)

current_step_id = 0
steps = [blank_image]

def get_step_id():
    global current_step_id
    return current_step_id

def get_steps():
    global steps
    return steps

def display_steps():
    global current_step_id, steps
    cv2.imshow('View', steps[current_step_id])
    cv2.waitKey(1)

def set_steps(new_steps):
    global steps
    steps = new_steps

def next_step():
    global current_step_id, steps
    current_step_id = (current_step_id + 1) % len(steps)

def on_mouse_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        next_step()

def create_window():
    cv2.namedWindow('View')
    cv2.setWindowProperty('View', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.setMouseCallback('View', on_mouse_click)
    while (True):
        current_step_id = get_step_id()
        steps = get_steps()
        print(current_step_id, ' - ', len(steps))
        cv2.imshow('View', steps[current_step_id])
        cv2.waitKey(1)
