#ifndef SPI_DRIVER_H
#define SPI_DRIVER_H

#include <stdint.h>

int init_spidev(void);
int spidev_write(uint8_t *buf, int len);

int test();

#endif // SPI_DRIVER_H
