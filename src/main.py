import cv2
import numpy as np
import time
import camera
import keyboard
import filter
import parameters as param
import analyze

def split_hsv(img):
    # Split into individual channels
    hue, saturation, value = cv2.split(img)

    # Display each channel
    cv2.imshow("Hue Channel", hue)
    cv2.imshow("Saturation Channel", saturation)
    cv2.imshow("Value Channel", value)

def process_frame():
    frame = camera.capture()

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

    # cv2.imshow("Color", f)
    # cv2.imshow("Adjusted", f_adjust)
    # cv2.imshow("Blurred", f_blur)
    # cv2.imshow("Uncanny", f_can)
    # cv2.imshow("Expanded", f_exp)
    # cv2.imshow("Closed", f_closed)
    # cv2.imshow("Full", f_full)
    # cv2.imshow("Eroted", f_eros)

    analyze.execute(f_eros, f)
    cv2.waitKey(0)

def main():
    camera.init(param.cam_debug)
    keyboard.init()

    last_time = time.time()
    try:
        while True:
            key = keyboard.getKey()
            param.tweak_by_key(key)

            current_time = time.time()
            timespan = current_time - last_time
            if timespan >= param.frame_timespan:
                process_frame()
                # param.show()
                last_time = current_time

            if not param.keep_running:
                break
    except KeyboardInterrupt:
        pass
    finally:
        camera.stop()
        keyboard.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
