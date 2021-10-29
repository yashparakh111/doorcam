import io
import time
import busio
import board
import digitalio

from picamera import PiCamera
from PIL import Image

from adafruit_rgb_display.rgb import color565
from adafruit_rgb_display import ili9341

# Camera config
camera_dim = (256, 320)

# SPI config
SCLK = board.D21
MOSI = board.D20
MISO = board.D19
DC   = board.D16
RST  = board.D26
CS   = board.D18

MHZ = 1000000
baudrate = 50 * MHZ

# Setup SPI bus using hardware SPI
spi = busio.SPI(clock=SCLK, MOSI=MOSI, MISO=MISO)

# Create TFT LCD display class
display = ili9341.ILI9341(
        spi, digitalio.DigitalInOut(DC),
        digitalio.DigitalInOut(CS),
        rst=digitalio.DigitalInOut(RST),
        baudrate=baudrate)
 
with PiCamera() as camera:
    # config camera
    camera.resolution = camera_dim
    camera.framerate = 32
    camera.rotation = 270
    camera.hflip = False
    camera.vflip = False

    # allow the camera to warmup
    time.sleep(0.1)

    # capture buffer
    stream = io.BytesIO()

    curr_time = time.time()
    disp_time = 0

    # perform continuous capture
    for frame in camera.capture_continuous(stream, format='jpeg', resize=(240, 320), burst=True):
        print('----')
        print('capture', time.time() - curr_time)
        curr_time = time.time()

        # capture stream
        image = Image.open(stream)

        curr_time = time.time()

        # Draw the image on the display hardware
        display.image(image)

        print('display', time.time() - curr_time)
        curr_time = time.time()

        print('fps', int(1.0 / (time.time() - disp_time)))
        disp_time = time.time()

        # reset buffer
        stream.truncate()
        stream.seek(0)

        curr_time = time.time()
