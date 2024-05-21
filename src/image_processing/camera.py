from picamera2 import Picamera2, Preview

cam = Picamera2()

def init(debug = False):
    preview_config = cam.create_preview_configuration()
    cam.configure(preview_config)
    if debug:
        cam.start_preview(Preview.QTGL)
    cam.start()

def capture():
    return cam.capture_array()

def stop():
    cam.stop()