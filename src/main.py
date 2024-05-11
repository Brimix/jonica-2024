import cv2
import numpy as np
import time
from camera import camera_init, camera_stop, camera_capture_array
from filter import filter_adjust, filter_blur, filter_segment, filter_toGray, filter_expand, filter_toSaturated
from servo_gpio import servo_init, servo_setAngle, servo_stop

# Initial constants
camDebug = False            # If true, displays camera preview
requiredSpan = 0.05         # 0.05 seconds between shots

# Tweak constants
blurIntensity = 2.5
cannyThreshold1 = 0.0001*255
cannyThreshold2 = 0.19*255
angle = 0
keepRunning = True

def applyKey(key):
    global keepRunning, blurIntensity, cannyThreshold1, cannyThreshold2, angle
    if key & 0xFF == ord('q'):
        keepRunning = False
    elif key & 0xFF == ord('w'):
        blurIntensity += 0.5
    elif key & 0xFF == ord('s'):
        if blurIntensity > 0.5:
            blurIntensity -= 0.5
    elif key & 0xFF == ord('e'):
        cannyThreshold1 += 0.0001 * 255
    elif key & 0xFF == ord('d'):
        if cannyThreshold1 > 0.0001 * 255:
            cannyThreshold1 -= 0.0001 * 255
    elif key & 0xFF == ord('r'):
        cannyThreshold2 += 0.01 * 255
    elif key & 0xFF == ord('f'):
        if cannyThreshold2 > 0.01 * 255:
            cannyThreshold2 -= 0.01 * 255
    elif key & 0xFF == ord('p'):
        angle += 1
    elif key & 0xFF == ord('o'):
        if angle > 1:
            angle -= 1

def process_frame():
    # global 

    frame = camera_capture_array()
    f = cv2.cvtColor(np.asarray(frame), cv2.COLOR_RGB2BGR)    #en este caso habria que ver porque dijimos de capaz trabajar en HSV no en RGB
    f_gray = library_toGray(f)
    f_just = filter_adjust(f_gray)
    f_blur = filter_blur(f_just, blurIntensity)
    f_can = filter_segment(f_blur, cannyThreshold1, cannyThreshold2)
    f_exp = filter_expand(f_can)

    f_color = filter_toSaturated(frame)

    # Here goes the plot
    # cv2.imshow("Gray", f_gray)
    # cv2.imshow("Adjusted", f_just)
    # cv2.imshow("Blurred", f_blur)
    # cv2.imshow("Uncanny", f_can)
    cv2.imshow("Expanded", f_exp)
    cv2.imshow("Color", f_color)

    key = cv2.waitKey(1)
    applyKey(key)

def main():
    camera_init(camDebug)
    servo_init()

    last_time = time.time()
    servo_setAngle(angle)

    try:
        while True:
            current_time = time.time()
            span_time = current_time - last_time
            if span_time >= requiredSpan:
                process_frame()
                print('blur:', blurIntensity)
                print('ct1:', cannyThreshold1)
                print('ct2:', cannyThreshold2)
                print('angle:', angle)
                servo_setAngle(angle)
                if not keepRunning:
                    break
                last_time = current_time
    except KeyboardInterrupt:
        pass
    finally:
        camera_stop()
        servo_stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
