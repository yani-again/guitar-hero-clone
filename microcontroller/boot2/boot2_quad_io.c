/* written sources: (move these to README.md later)
 * RP2040 Datasheet
 * https://pip-assets.raspberrypi.com/categories/814-rp2040/documents/RP-008371-DS-1-rp2040-datasheet.pdf
 *
 * The Definitive Guide To ARM Cortex-M0 And Cortex-M0+ Processors by Joseph Yiu
 * https://www.sciencedirect.com/book/monograph/9780128032770/the-definitive-guide-to-arm-cortex-m0-and-cortex-m0-and-processors
 *
 * SPI NOR Flash Standard (for register offsets)
 * https://www.winbond.com/hq/product/code-storage-flash-memory/serial-nor-flash/?__locale=en&partNo=W25Q80DV
 *
 * MSVC /SECTION documentation
 * https://github.com/MicrosoftDocs/cpp-docs/blob/main/docs/build/reference/section-specify-section-attributes.md
 */

#include <stdint.h>

// XIP
#define XIP_BASE            0x10000000

// SSI
#define XIP_SSI_BASE        0x18000000
#define XIP_SSI_CTRLR0      ( *(volatile uint32_t *) ) (SSI_BASE + 0x00)
#define XIP_SSI_SSIENR      ( *(volatile uint32_t *) ) (SSI_BASE + 0x08)
#define XIP_SSI_BAUDR       ( *(volatile uint32_t *) ) (SSI_BASE + 0x14)
#define XIP_SSI_SR          ( *(volatile uint32_t *) ) (SSI_BASE + 0x28)
#define XIP_SSI_DR0         ( *(volatile uint32_t *) ) (SSI_BASE + 0x60)
#define XIP_SSI_SPI_CTRLR0  ( *(volatile uint32_t *) ) (SSI_BASE + 0xf4)

// SPI flash standard values
#define SPI_SR1_R   0x05
#define SPI_SR2_R   0x35
#define SPI_SR_W    0x01

/* Notes:
 * disable SSI before configuring it
 * clk_peri runs at 125MHz at startup (SSI runs from it)
 * DFS_32 = how many bits of data are transferred per frame
 */

#ifndef _MSC_VER
    __attribute__((noreturn, section(".boot2")))
#else
    #error "Please compile with a compiler that \
        supports \"__attribute__\" (e.g. GCC/Clang)"
#endif
void boot_stage_2(void)
{
    XIP_SSI_SSIENR = 0;
    XIP_SSI_BAUDR = 4;
    XIP_SSI_CTRLR0 |= (7 << 16);    // 8 clocks per data frame
    XIP_SSI_SSIENR = 1;

    // check if QE bit is on in SR2, enable if not
    XIP_SSI_DR0 = SPI_SR1_R;
    XIP_SSI_DR0 = SPI_SR2_R;

    XIP_SSI_SSIENR = 0;
    XIP_SSI_CTRLR0 |= (3 << 21)     // QSPI mode (4-channels)
                      | (31 << 16)  // 32 clocks per data frame
                      | (3 << 8);   // EEPROM read mode
    XIP_SSI_SSIENR = 1;

}
