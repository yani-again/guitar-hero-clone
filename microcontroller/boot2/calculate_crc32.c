#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>


#define BOOT2_LEN       252
#define POLYNOMIAL      (uint32_t) 0x04C11DB7


// NOTE: the RP2040 uses the CRC32 MPEG2 standard
int main(int argc, char *argv[])
{
    char data[BOOT2_LEN + 1] = {0};
    uint32_t crc = 0xFFFFFFFF;
    FILE *p_file;

    // improper input check
    if (argc != 2)
    {
        printf("Bad usage!\n");
        printf("Requires exactly 1 file as parameter.\n");
        exit(1);
    }

    p_file = fopen(argv[1], "r");
    if (p_file == NULL)
    {
        printf("unable to open %s\n", argv[1]);
        exit(1);
    }

    if (fgets(data, BOOT2_LEN + 1, p_file) == NULL)
    {
        printf("error while reading %s\n", argv[1]);
        fclose(p_file);
        exit(1);
    }
    fclose(p_file);

    for (int i = 0; i < BOOT2_LEN; ++i)
    {
        crc ^= (data[i] << 24);

        for (int j = 0; j < sizeof(data[0]) * 8; ++j)
        {
            // MSB == 1
            if (crc & 0x80000000)
                crc = (crc << 1) ^ POLYNOMIAL;
            else
                crc <<= 1;
        }
    }

    printf("The remainder for %s is %u\n", argv[1], crc);
}

