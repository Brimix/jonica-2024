import cv2
import numpy as np
import time
import keyboard
import parameters as param
import analyze
import servo_pigpio as servo

import image_processing.process as imp
import image_processing.filter_parameters as im_param
import image_processing.debug_tools as im_dbg

def kick():
    servo.set_angle(135)
    time.sleep(0.4)       
    servo.set_angle(45)

def process_frame():
    [fp, fr] = imp.get_filtered_frame()
    analyze.execute(fp, fr)
    if (analyze.current_color == 'red' and analyze.current_shape == 'circle'):
        kick()

def main():
    imp.init()
    keyboard.init()
    servo.init()

    last_time = time.time()
    try:
        while True:
            key = keyboard.getKey()
            im_param.tweak_by_key(key)
            im_dbg.switch_step()

            current_time = time.time()
            timespan = current_time - last_time
            if timespan >= param.frame_timespan:
                process_frame()
                last_time = current_time

            if not param.keep_running:
                break
    except KeyboardInterrupt:
        pass
    finally:
        imp.stop()
        keyboard.stop()
        servo.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
