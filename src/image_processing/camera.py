from picamera2 import Picamera2, Preview

cam = Picamera2()

def init(debug = False):
    preview_config = cam.create_preview_configuration()

    # Set the resolution and adjust FOV settings here
    preview_config['main']['size'] = (820, 616)  # You can change this to your preferred resolution
    preview_config['raw']['size'] = (1640, 1232)  # You can change this to your preferred resolution

    cam.configure(preview_config)
    if debug:
        cam.start_preview(Preview.QTGL)
    cam.start()
    # print("Camera started with configuration:", preview_config)


def capture():
    return cam.capture_array()

def stop():
    cam.stop()