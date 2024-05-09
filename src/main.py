import cv2
import numpy as np
import time
from camera import camera_init, camera_stop, camera_capture_array

def process_frame(label):
    frame = camera_capture_array()
    img = cv2.cvtColor(np.asarray(frame), cv2.COLOR_RGB2BGR)
    filename = f"img/frame_{int(label)}.jpg"
    cv2.imwrite(filename, img)

def main():
    camera_init()

    last_time = time.time()
    required_span = 1
    it_number = 0

    try:
        while True:
            current_time = time.time()
            span_time = current_time - last_time
            if span_time >= required_span:
                print('Process..')
                process_frame(it_number)
                it_number = it_number + 1
                last_time = current_time
    except KeyboardInterrupt:
        pass
    finally:
        camera_stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
