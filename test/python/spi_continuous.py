import spidev
import time

spi = spidev.SpiDev(1, 0)
spi.max_speed_hz = 100000
spi.mode = 0
spi.cshigh = True

try:
    while True:
        spi.writebytes([0x3A])
        time.sleep(1)
finally:
    spi.close()
