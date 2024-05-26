import cv2
import numpy as np
import time
import keyboard
import parameters as param

import image_processing.process as imp
import image_processing.filter_parameters as im_param
import image_processing.debug_tools as im_dbg

import computer_vision.functions as cvf

def process_frame():
    obj = cvf.get_mode_object()
    if (obj is not None):
        color, shape = obj
        print('--- ', color, shape)
    else:
        print('. Nothing to show')

def main():
    imp.init()
    keyboard.init()

    last_time = time.time()
    try:
        while True:
            key = keyboard.getKey()
            im_param.tweak_by_key(key)
            # im_dbg.switch_step()

            param.tweak_by_key(key)
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
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
