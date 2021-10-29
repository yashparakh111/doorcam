import busio
import digitalio
import board

from adafruit_bus_device.spi_device import SPIDevice

prime_numbers = list(range(10))
print(prime_numbers)

SCK = board.D21
MOSI = board.D20
MISO = board.D19

with busio.SPI(SCK, MOSI, MISO) as spi_bus:
    cs = digitalio.DigitalInOut(board.D18)
    device = SPIDevice(spi_bus, cs, cs_active_value=True)
    bytes_read = bytearray(prime_numbers)

    # write to spi
    print("Sending data...", len(bytes_read))
    with device as spi:
        spi.write(bytes_read)

