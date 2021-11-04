#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <fcntl.h>
#include <time.h>

#include <sys/ioctl.h>
#include <linux/spi/spidev.h>

#include "config.h"

static const char *device = "/dev/spidev1.0";
static int fd;
static uint8_t bits = 8;
static uint32_t mode = 0;
static uint32_t speed = SPI_SPEED;
static uint16_t delay = 0;

int init_spidev() {
	int ret = 0;

	// open spi device
	fd = open(device, O_RDWR);
	if(fd < 0) {
		puts("can't open device");
		return -1;
	}

	// set write mode
	ret = ioctl(fd, SPI_IOC_WR_MODE32, &mode);
	if(ret == -1) {
		puts("can't set write mode");
		return -1;
	}

	// set bits per word
	ret = ioctl(fd, SPI_IOC_WR_BITS_PER_WORD, &bits);
	if (ret == -1) {
		puts("can't set bits per word");
		return -1;
	}

	// set max speed hz
	ret = ioctl(fd, SPI_IOC_WR_MAX_SPEED_HZ, &speed);
	if (ret == -1) {
		puts("can't set max speed");
		return -1;
	}

	return 0;
}

int spidev_write(uint8_t *tx, int len) {
	int ret = 0;

	struct spi_ioc_transfer tr = {
		.tx_buf = (unsigned long)tx,
		.len = len,
		.delay_usecs = delay,
		.speed_hz = speed,
		.bits_per_word = bits,
		.tx_nbits = 8,
		.rx_nbits = 0,
	};

	ret = ioctl(fd, SPI_IOC_MESSAGE(1), &tr);

	if(ret < 1) printf("can't send spi message\n");

	return ret;
}

// send data equivalent to sending one 76.8 KP (320x240) frame
// each pixel is a 565 color (16-bit color)
int test() {
	int ret = 0;

	// initialize spidev
	ret = init_spidev();
	if(ret < 0) return -1;

	// setup testcase (send 0-1023)
	int len = 1024;
	uint8_t *tx = (uint8_t *) malloc(sizeof(uint16_t) * 320 * 240);
	for(int i = 0; i < len; i++) tx[i] = i;

	// send several messages and time each
	int i = 0;
	clock_t st_t, en_t;
	while(i < 1) {
		st_t = clock();

		// send message
		ret = spidev_write(tx, len);

		if(ret >= 1) printf("%d: sent in %f\n", i, ((double)(clock() - st_t)/CLOCKS_PER_SEC));
		else return -1;
		i++;
	}

	return 0;
}
