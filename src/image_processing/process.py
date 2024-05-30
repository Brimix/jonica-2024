import cv2
import numpy as np
import image_processing.camera as cam
import image_processing.filter as filter
import image_processing.debug_tools as dbg

bg_subtractor = None

def init():
    global bg_subtractor
    bg_subtractor = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=16, detectShadows=True)
    cam.init()
    # Init background by getting images
    for _ in range(100):
        cam.capture()

def get_frame():
    return cam.capture()

def get_quick_filtered_frame():
    frame = cam.capture()

    f = cv2.cvtColor(np.asarray(frame), cv2.COLOR_RGB2HSV)

    f_adjust = filter.hsv_adjust(f)
    f_blur = filter.blur(f_adjust)
    f_can = filter.segment(f_blur)
    f_exp = filter.expand(f_can)
    f_full = filter.fill_holes(f_exp)

    # For debugging only
    # dbg.split_hsv(f_adjust)
    f_color = cv2.cvtColor(np.asarray(frame), cv2.COLOR_BGR2RGB)
    dbg.set_steps([f_color, f_can, f_exp, f_full])

    return [f_full, f]

def get_filtered_frame():
    frame = cam.capture()

    # En este caso dijimos de trabajar en HSV
    f = cv2.cvtColor(np.asarray(frame), cv2.COLOR_RGB2HSV)

    f_adjust = filter.hsv_adjust(f)
    f_blur = filter.blur(f_adjust)
    f_can = filter.segment(f_blur)
    f_exp = filter.expand(f_can)
    f_closed = filter.close_shape(f_exp)
    f_full = filter.fill_holes(f_closed)
    f_eros = filter.erode(f_full)


    # For debugging only
    # dbg.split_hsv(f_adjust)
    # f_color = cv2.cvtColor(np.asarray(frame), cv2.COLOR_BGR2RGB)
    # dbg.set_steps([f_color, f_adjust, f_blur, f_can, f_exp, f_closed, f_full, f_eros])

    return [f_eros, f]

def detect_movement():
    THRESHOLD_PERCENT = 0.1
    # Capture frame-by-frame
    frame = cam.capture()
    f_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Apply background subtraction
    fg_mask = bg_subtractor.apply(f_hsv)
    fg_close = filter.open_shape(fg_mask)
    
    # Calculate the percentage of the frame that is considered foreground
    foreground_pixels = cv2.countNonZero(fg_close)
    total_pixels = frame.shape[0] * frame.shape[1]
    movement_ratio = foreground_pixels / total_pixels

    # Display the resulting frame and foreground mask
    # cv2.imshow('Frame', frame)
    # cv2.imshow('Foreground Mask', fg_close)
    cv2.waitKey(1)
    
    return movement_ratio > THRESHOLD_PERCENT

def stop():
    cam.stop()
