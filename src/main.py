import cv2
import numpy as np
import time
import keyboard
import parameters as param
import analyze
import ServoController as SC

import image_processing.process as imp
import image_processing.filter_parameters as im_param
import image_processing.debug_tools as im_dbg

trapdoor_servo = SC.ServoController(12)
train_servo = SC.ServoController(13)

def trapdoor_open():
    global trapdoor_servo
    print('Lets kick')
    trapdoor_servo.sweep(180, 130, 2)
    time.sleep(1)
    trapdoor_servo.sweep(130, 180, 0.5)

def train_open():
    global train_servo
    print('Lets kick train')
    train_servo.sweep(180, 0, 1)
    time.sleep(1)
    train_servo.sweep(0, 180, 1)

def process_frame():
    [fp, fr] = imp.get_filtered_frame()
    analyze.execute(fp, fr)

def main():
    global trapdoor_servo, train_servo
    imp.init()
    keyboard.init()
    trapdoor_servo.set_angle(10)
    train_servo.set_angle(10)

    last_time = time.time()
    td = True
    try:
        while True:
            key = keyboard.getKey()
            im_param.tweak_by_key(key)
            im_dbg.switch_step()

            param.tweak_by_key(key)
            current_time = time.time()
            timespan = current_time - last_time

            if timespan >= param.frame_timespan:
                process_frame()
                if td:
                    trapdoor_open()
                else:
                    train_open()
                
                td = not td
                last_time = current_time

            if not param.keep_running:
                break
    except KeyboardInterrupt:
        pass
    finally:
        imp.stop()
        keyboard.stop()
        trapdoor_servo.stop()
        train_servo.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
