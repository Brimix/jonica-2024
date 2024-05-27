import cv2
import keystrokes

import image_processing.process as imp
import actuators.units as act
import fsm

def main():
    keystrokes.init()
    imp.init()
    try:
        while True:
            key = keystrokes.get_stroke()

            # Turn on to debug
            # im_dbg.switch_step()
            # im_param.tweak_by_key(key)
            
            fsm.run(key)

            if key == 'q':
                break
            
    except KeyboardInterrupt:
        pass
    finally:
        act.motor.stop_motor()
        imp.stop()
        keystrokes.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()