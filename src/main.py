import cv2

import image_processing.process as imp
import fsm
import view

from units import train, trapdoor, carrier

def main():
    imp.init()
    view.create_window()
    try:
        while True:    
            fsm.run()
            
    except KeyboardInterrupt:
        pass
    finally:
        train.stop()
        trapdoor.stop()
        carrier.stop()
        imp.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()