#include <stdint.h>


// XIP
#define XIP_BASE            0x10000000

// SSI
#define XIP_SSI_BASE        0x18000000
#define XIP_SSI_CTRLR0      ( *(volatile uint32_t *) (XIP_SSI_BASE + 0x00) )
#define XIP_SSI_SSIENR      ( *(volatile uint32_t *) (XIP_SSI_BASE + 0x08) )
#define XIP_SSI_BAUDR       ( *(volatile uint32_t *) (XIP_SSI_BASE + 0x14) )
#define XIP_SSI_SR          ( *(volatile uint32_t *) (XIP_SSI_BASE + 0x28) )
#define XIP_SSI_DR0         ( *(volatile uint32_t *) (XIP_SSI_BASE + 0x60) )
#define XIP_SSI_SPI_CTRLR0  ( *(volatile uint32_t *) (XIP_SSI_BASE + 0xf4) )

// QSPI values
#define QSPI_ENABLE         2       // switch SPI to QSPI I/O
#define QSPI_CLOCKS         31      // 32 clocks per frame
#define QSPI_TRANS_MODE     3       // EEPROM read mode
#define QSPI_INST_LEN       2       // 8-bit instructions
#define QSPI_INST_PREFIX    0x6B
#define QSPI_WAIT           8       // clocks to wait between TX & RX
#define QSPI_ADDR_LEN       6       // 24-bit addrs

// SPI flash standard values
#define SPI_SR1_R           0x05
#define SPI_SR2_R           0x35
#define SPI_SR_W            0x01

// M0PLUS
#define M0PLUS_BASE         0xE0000000
#define M0PLUS_VTOR         ( *(volatile uint32_t *) (M0PLUS_BASE + 0xED08) )
#define VECTOR_TABLE_BASE   XIP_BASE + 0x100
#define VECTOR_TABLE_SP     VECTOR_TABLE_BASE
#define VECTOR_TABLE_RST    VECTOR_TABLE_BASE + 0x04    // reset handler


// compiler attributes
#if defined(__GNUC__) || defined(__clang__)
#define BOOT2_ATTR __attribute__((noreturn, section(".boot2")))
#else
#error "Compiler must support GNU-style \"__attribute__\""
#endif


BOOT2_ATTR
void boot_stage_2(void)
{
    // initial SSI config
    XIP_SSI_SSIENR = 0;
    XIP_SSI_BAUDR = 4;
    XIP_SSI_CTRLR0 |= (7 << 16);    // 8 clocks per frame for 8-bit
                                    // SR registers
    XIP_SSI_SSIENR = 1;

    // check if QE bit is on in SR2, enable if not
    XIP_SSI_DR0 = SPI_SR1_R;
    XIP_SSI_DR0 = SPI_SR2_R;
    while ((~XIP_SSI_SR & (1 << 2)) || (XIP_SSI_SR & 1))
        ;   // wait for transmission to finish
    uint8_t status_reg1 = XIP_SSI_DR0;
    uint8_t status_reg2 = XIP_SSI_DR0;
    if (~status_reg2 & (1 << 1))
    {
        XIP_SSI_DR0 = 0x06; // enable write
        XIP_SSI_DR0 = 0x01; // write command
        XIP_SSI_DR0 = status_reg1;
        XIP_SSI_DR0 = status_reg2 | (1 << 1);
        XIP_SSI_DR0 = 0x04; // disable write
    }

    // configure QSPI
    XIP_SSI_SSIENR = 0;
    XIP_SSI_CTRLR0 |= (QSPI_ENABLE << 21)
                    | (QSPI_CLOCKS << 16)
                    | (QSPI_TRANS_MODE << 8);
    XIP_SSI_SPI_CTRLR0 |= (QSPI_INST_PREFIX << 24)
                        | (QSPI_WAIT << 11)
                        | (QSPI_INST_LEN << 8)
                        | (QSPI_ADDR_LEN << 2);
    XIP_SSI_SSIENR = 1;

    // load SP & call reset handler using vector table
    M0PLUS_VTOR = VECTOR_TABLE_BASE;
    
    asm("MSR MSP, %0"
            :
            : "r" ( *(uint32_t *) (M0PLUS_VTOR + 0x00) )
        );
    asm("BX %0"
            :
            : "r" ( *(uint32_t *) (M0PLUS_VTOR + 0x04) )
        );

    __builtin_unreachable();
}

