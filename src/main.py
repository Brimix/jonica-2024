import cv2
import threading

import image_processing.process as imp
import fsm
import view

from units import train, trapdoor, carrier

def run_fsm():
    while True:    
        fsm.run()

def main():
    imp.init()

    thread1 = threading.Thread(target=run_fsm)
    thread2 = threading.Thread(target=view.create_window)

    try:
        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()
            
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