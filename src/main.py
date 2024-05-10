import cv2
import numpy as np
import time
from camera import camera_init, camera_stop, camera_capture_array
from library import library_adjust, library_filter, library_segment, library_toGray

def process_frame(label, blur_intensity):
    frame = camera_capture_array()
    f = cv2.cvtColor(np.asarray(frame), cv2.COLOR_RGB2BGR)
    f_gray = library_toGray(f)
    f_just = library_adjust(f_gray)
    f_blur = library_filter(f_just, blur_intensity)
    f_can = library_segment(f_blur)

    # Here goes the plot
    # cv2.imshow("Gray", f_gray)
    # cv2.imshow("Adjusted", f_just)
    cv2.imshow("Blurred", f_blur)
    cv2.imshow("Uncanny", f_can)

    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        return False, blur_intensity
    elif key & 0xFF == ord('w'):  # Up arrow key
        blur_intensity += 0.1
    elif key & 0xFF == ord('s'):  # Down arrow key
        blur_intensity -= 0.1
    return True, blur_intensity

def main():
    cam_debug = False
    camera_init(cam_debug)

    last_time = time.time()
    required_span = 0.1
    it_number = 0
    blur_intensity = 2.5

    try:
        while True:
            current_time = time.time()
            span_time = current_time - last_time
            if span_time >= required_span:
                # print('Process..')
                result, blur_intensity = process_frame(it_number, blur_intensity)
                print(blur_intensity)
                if not result:
                    break  # Exit the loop if process_frame returns False
                it_number = it_number + 1
                last_time = current_time
    except KeyboardInterrupt:
        pass
    finally:
        camera_stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
