
all: spi gpio

spi: spi_driver.c
	gcc -o spi spi_driver.c

gpio: blink.c
	gcc -o gpio blink.c -lbcm2835 
