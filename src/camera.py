from picamera2 import Picamera2, Preview

cam = Picamera2()

def camera_init(debug):
    preview_config = cam.create_preview_configuration()
    cam.configure(preview_config)
    if debug:
        cam.start_preview(Preview.QTGL)
    cam.start()

def camera_capture_array():
    return cam.capture_array()

def camera_stop():
    cam.stop()