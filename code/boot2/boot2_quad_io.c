#include <stdint.h>

// XIP
#define XIP_BASE            0x10000000

// SSI
#define SSI_BASE            0x18000000
#define SSI_CTRLR0          ( *(volatile uint32_t *) ) (SSI_BASE + 0x00)
#define SSI_CTRLR1          ( *(volatile uint32_t *) ) (SSI_BASE + 0x04)
#define SSI_SSIENR          ( *(volatile uint32_t *) ) (SSI_BASE + 0x08)
#define SSI_SER             ( *(volatile uint32_t *) ) (SSI_BASE + 0x10)    // UNSURE
#define SSI_BAUDR           ( *(volatile uint32_t *) ) (SSI_BASE + 0x14)
#define SSI_TXFTLR          ( *(volatile uint32_t *) ) (SSI_BASE + 0x18)
#define SSI_RXFTLR          ( *(volatile uint32_t *) ) (SSI_BASE + 0x1C)
#define SSI_TXFLR           ( *(volatile uint32_t *) ) (SSI_BASE + 0x20)
#define SSI_RXFLR           ( *(volatile uint32_t *) ) (SSI_BASE + 0x24)
#define SSI_SR              ( *(volatile uint32_t *) ) (SSI_BASE + 0x28)
#define SSI_IMR             ( *(volatile uint32_t *) ) (SSI_BASE + 0x2C)
#define SSI_ISR             ( *(volatile uint32_t *) ) (SSI_BASE + 0x30)
#define SSI_RISR            ( *(volatile uint32_t *) ) (SSI_BASE + 0x34)
#define SSI_TXOICR          ( *(volatile uint32_t *) ) (SSI_BASE + 0x38)
#define SSI_RXOICR          ( *(volatile uint32_t *) ) (SSI_BASE + 0x3C)
#define SSI_RXUICR          ( *(volatile uint32_t *) ) (SSI_BASE + 0x40)
#define SSI_MSTICR          ( *(volatile uint32_t *) ) (SSI_BASE + 0x44)
#define SSI_ICR             ( *(volatile uint32_t *) ) (SSI_BASE + 0x48)
#define SSI_DMACR           ( *(volatile uint32_t *) ) (SSI_BASE + 0x4C)
#define SSI_DMATDLR         ( *(volatile uint32_t *) ) (SSI_BASE + 0x50)
#define SSI_DMARDLR         ( *(volatile uint32_t *) ) (SSI_BASE + 0x54)
#define SSI_IDR             ( *(volatile uint32_t *) ) (SSI_BASE + 0x58)
#define SSI_SSI_VERSION_ID  ( *(volatile uint32_t *) ) (SSI_BASE + 0x5C)
#define SSI_DR0             ( *(volatile uint32_t *) ) (SSI_BASE + 0x60)
#define SSI_RX_SAMPLE_DLY   ( *(volatile uint32_t *) ) (SSI_BASE + 0x64)
#define SSI_SPI_CTRLR0      ( *(volatile uint32_t *) ) (SSI_BASE + 0x68)
#define SSI_TXD_DRIVE_EDGE  ( *(volatile uint32_t *) ) (SSI_BASE + 0x6C)


