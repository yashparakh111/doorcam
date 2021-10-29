import time
import busio
import board
import digitalio

from PIL import Image

from adafruit_rgb_display.rgb import color565
from adafruit_rgb_display import ili9341

# Raspberry Pi configuration.
SCLK = board.D21
MOSI = board.D20
MISO = board.D19
DC   = board.D16
RST  = board.D26
CS   = board.D18

MHZ = 1000000
baudrate = 48 * MHZ

# Setup SPI bus using hardware SPI:
spi = busio.SPI(clock=SCLK, MOSI=MOSI, MISO=MISO)

# Create TFT LCD display class.
display = ili9341.ILI9341(
        spi, digitalio.DigitalInOut(DC),
        digitalio.DigitalInOut(CS),
        rst=digitalio.DigitalInOut(RST),
        baudrate=baudrate)

# Load an image.
print('Loading image...')
image = Image.open('cat.jpg')
print(type(image))
 
# Resize the image and rotate it so it's 240x320 pixels.
image = image.rotate(90).resize((240, 320))


while True:
    print('new loop...')

    # Clear the display
    display.fill(0)

    # Draw a red pixel in the center.
    display.pixel(120, 160, color565(255, 0, 0))

    # Pause 2 seconds.
    time.sleep(2)

    # Clear the screen blue.
    display.fill(color565(0, 0, 255))

    # Pause 2 seconds.
    time.sleep(2)

    # Draw the image on the display hardware.
    display.image(image)

    # Pause 2 seconds.
    time.sleep(2)

