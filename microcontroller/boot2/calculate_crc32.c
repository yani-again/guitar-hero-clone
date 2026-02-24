#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>


#define BOOT2_LEN       252 * 8
#define CRC_LEN         32
#define POLYNOMIAL      (uint32_t) 0x04C11DB7


int main(int argc, char *argv[])
{
    char buffer[BOOT2_LEN + CRC_LEN + 1] = {0};
    unsigned int context_start = 0;
    uint32_t crc;
    FILE *p_file;

    // improper input check
    if (argc != 2)
    {
        printf("Bad usage!\n");
        printf("Requires exactly 1 file as parameter.\n");
        exit(1);
    }

    // zero out buffer (char 0, not int 0) without null-terminator
    for (int i = 0; i < BOOT2_LEN + CRC_LEN; ++i)
        buffer[i] = '0';

    p_file = fopen(argv[1], "r");
    if (p_file == NULL)
    {
        printf("unable to open %s\n", argv[1]);
        exit(1);
    }

    fgets(buffer, BOOT2_LEN, p_file);
    fclose(p_file);


    // copy first CRC_LEN bits from buffer (CRC_LEN / 8 bytes)
    crc = (buffer[0] << 24) +
          (buffer[1] << 16) +
          (buffer[2] << 8) +
          (buffer[3] << 0);
}

