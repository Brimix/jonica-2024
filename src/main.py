import cv2
import numpy as np
import time
import camera
import keyboard
import filter
import parameters as param
import analyze
import servo_pigpio as servo

def kick():
    servo.set_angle(135)
    time.sleep(0.4)       
    servo.set_angle(45)

def process_frame():
    frame = camera.capture()

    # En este caso dijimos de trabajar en HSV
    f_color = cv2.cvtColor(np.asarray(frame), cv2.COLOR_BGR2RGB) #SIRVE ESTO?
    f = cv2.cvtColor(np.asarray(frame), cv2.COLOR_RGB2HSV)

    # split_hsv(f)

    f_adjust = filter.hsv_adjust(f)
    f_blur = filter.blur(f_adjust)
    f_can = filter.segment(f_blur)
    f_exp = filter.expand(f_can)
    f_closed = filter.close_shape(f_exp)
    f_full = filter.fill_holes(f_closed)
    f_eros = filter.erode(f_full)

    # cv2.imshow("Color", f_color)
    # cv2.imshow("Adjusted", f_adjust)
    # cv2.imshow("Blurred", f_blur)
    # cv2.imshow("Uncanny", f_can)
    # cv2.imshow("Expanded", f_exp)
    # cv2.imshow("Closed", f_closed)
    # cv2.imshow("Full", f_full)
    # cv2.imshow("Eroted", f_eros)

    analyze.execute(f_eros, f)
    cv2.waitKey(1)

def main():
    camera.init(param.cam_debug)
    keyboard.init()
    servo.init()

    last_time = time.time()
    try:
        while True:
            key = keyboard.getKey()
            param.tweak_by_key(key)
            servo.set_angle(param.angle)

            current_time = time.time()
            timespan = current_time - last_time
            if timespan >= param.frame_timespan:
                process_frame()
                # param.show()
                last_time = current_time
                if (analyze.current_color == 'red' and analyze.current_shape == 'circle'):
                    kick()

            if not param.keep_running:
                break
    except KeyboardInterrupt:
        pass
    finally:
        camera.stop()
        keyboard.stop()
        servo.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
