#include <stdint.h>

// XIP
#define XIP_BASE            0x10000000

// SSI
#define XIP_SSI_BASE        0x18000000
#define XIP_SSI_CTRLR0      ( *(volatile uint32_t *) ) (SSI_BASE + 0x00)
#define XIP_SSI_CTRLR1      ( *(volatile uint32_t *) ) (SSI_BASE + 0x04)
#define XIP_SSI_SSIENR      ( *(volatile uint32_t *) ) (SSI_BASE + 0x08)
#define XIP_SSI_BAUDR       ( *(volatile uint32_t *) ) (SSI_BASE + 0x14)
#define XIP_SSI_SR          ( *(volatile uint32_t *) ) (SSI_BASE + 0x28)
#define XIP_SSI_DR0         ( *(volatile uint32_t *) ) (SSI_BASE + 0x60)
#define XIP_SSI_SPI_CTRLR0  ( *(volatile uint32_t *) ) (SSI_BASE + 0xf4)

/* NOTES
 * - disable SSI before configuring it
 */

__attribute__((noreturn, section(".boot2")))
void boot_stage_2(void)
{
    XIP_SSI_SSIENR = 0;
    
}
