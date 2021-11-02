#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <fcntl.h>
#include <time.h>

#include <sys/ioctl.h>
#include <linux/spi/spidev.h>

int main() {
	int ret = 0;
	int fd;

	const char *device = "/dev/spidev1.0";
	uint8_t bits = 8;
	uint32_t mode = 0;
	uint32_t speed = 100*1000;
	uint16_t delay = 0;
	printf("speed: %d\n", speed);

	int len = 1024;
	uint8_t *tx = (uint8_t *)malloc(sizeof(uint8_t) * len);
	for(int i = 0; i < len; i++) {
		tx[i] = i;
	}

	// open spi device
	fd = open(device, O_RDWR);
	if(fd < 0) puts("can't open device");

	// set write mode
	ret = ioctl(fd, SPI_IOC_WR_MODE32, &mode);
	if(ret == -1) puts("can't set write mode");

	// set bits per word
	ret = ioctl(fd, SPI_IOC_WR_BITS_PER_WORD, &bits);
	if (ret == -1) puts("can't set bits per word");

	// set max speed hz
	ret = ioctl(fd, SPI_IOC_WR_MAX_SPEED_HZ, &speed);
	if (ret == -1) puts("can't set max speed");

	struct spi_ioc_transfer tr = {
		.tx_buf = (unsigned long)tx,
		.len = len,
		.delay_usecs = delay,
		.speed_hz = speed,
		.bits_per_word = bits,
		.tx_nbits = 8,
		.rx_nbits = 0,
	};

	int num_msg = 1;
	int i = 0;
	clock_t st_t, en_t;
	while(i < 5) {
		st_t = clock();
		ret = ioctl(fd, SPI_IOC_MESSAGE(num_msg), &tr);

		if(ret < 1) printf("%d: can't send spi message\n", i);
		else printf("%d: sent in %f\n", i, ((double)(clock() - st_t)/CLOCKS_PER_SEC));
		i++;
	}

	return ret;
}
