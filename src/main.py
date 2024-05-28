import cv2
import keystrokes

# import image_processing.debug_tools as im_dbg
# import image_processing.filter_parameters as im_param
import image_processing.process as imp
import fsm
from units import train, trapdoor, motor

def main():
    keystrokes.init()
    imp.init()
    try:
        while True:
            key = keystrokes.get_stroke()
            # key = '0'

            # Turn on to debug
            # im_dbg.switch_step()
            # im_param.tweak_by_key(key)
            
            fsm.run(key)

            if key == 'q':
                break
            
    except KeyboardInterrupt:
        pass
    finally:
        motor.stop_motor()
        train.stop()
        trapdoor.stop()
        motor.stop()
        imp.stop()
        keystrokes.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()