import cv2
import numpy as np
import image_processing.camera as cam
import image_processing.filter as filter
import image_processing.debug_tools as dbg

def init():
    cam.init()

def get_frame():
    return cam.capture()

def get_filtered_frame():
    frame = cam.capture()

    # En este caso dijimos de trabajar en HSV
    f = cv2.cvtColor(np.asarray(frame), cv2.COLOR_RGB2HSV)

    # split_hsv(f)

    f_adjust = filter.hsv_adjust(f)
    f_blur = filter.blur(f_adjust)
    f_can = filter.segment(f_blur)
    f_exp = filter.expand(f_can)
    f_closed = filter.close_shape(f_exp)
    f_full = filter.fill_holes(f_closed)
    f_eros = filter.erode(f_full)


    # For debugging only
    f_color = cv2.cvtColor(np.asarray(frame), cv2.COLOR_BGR2RGB)
    dbg.set_steps([f_color, f_adjust, f_blur, f_can, f_exp, f_closed, f_full, f_eros])

    return [f_eros, f]

def stop():
    cam.stop()