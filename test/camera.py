import io
import time
from picamera import PiCamera

from PIL import Image

# camera_dim = (640, 480)
camera_dim = (256, 320)

with PiCamera() as camera:
    # config camera
    camera.resolution = camera_dim
    camera.framerate = 32
    camera.rotation = 0
    camera.hflip = False
    camera.vflip = False

    # allow the camera to warmup
    time.sleep(0.1)

    # capture buffer
    stream = io.BytesIO()

    # perform continuous capture
    for frame in camera.capture_continuous(stream, format='jpeg'):
        stream.truncate()
        stream.seek(0)

        image = Image.open(stream)

        print(image.size)
