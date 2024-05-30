import cv2
import numpy as np
import time
import keystrokes
import _parameters as param

import image_processing.process as imp
import image_processing.filter_parameters as im_param
import image_processing.debug_tools as im_dbg

import computer_vision.functions as cvf
from cnn.predictor import predict_from_image

def process_frame():
    # obj = cvf.get_object()
    # if (obj is not None):
    #     color, shape = obj
    #     print('--- ', color, shape)
    # else:
    #     print('. Nothing to show')
    img = cvf.create_image()
    result = predict_from_image(img)
    if (img is None):
        print('Efe')
        return
    cv2.imshow('Coso', img)
    print('Eso', result)
    cv2.waitKey(1)


def main():
    imp.init()
    keystrokes.init()

    last_time = time.time()
    try:
        while True:
            key = keystrokes.get_stroke()
            im_param.tweak_by_key(key)
            im_dbg.switch_step()

            param.tweak_by_key(key)
            current_time = time.time()
            timespan = current_time - last_time

            if timespan >= param.frame_timespan:
                process_frame()
                # im_param.show()
                
                last_time = current_time
    except KeyboardInterrupt:
        pass
    finally:
        imp.stop()
        keystrokes.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
