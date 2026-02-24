# Guitar Hero Clone Game
This project is a student-led project that combines our skills & interests to produce a playable experience modelled after the hit game Guitar Hero.

It uses:
- Python & PyGame for the playable game experience
- Raspberry Pi RP2040 for the game controller
- bare-metal C to program the game controller

Below are further details on both halves of the project.

## Game (Python & PyGame)
*Programmers: @ar-eej, @tej-333, @sophiehardwick0*
```
TODO: complete this section when designs are finalised & coding begins.
```

## Game Controller (Bare-Metal RP2040 In C)
*Programmers: @yani-again, @*
### What Is This?
The code within the `microcontroller` folder is the code for an RP2040 Guitar Hero-inspired 'guitar'. It uses bare-metal C to implement minimal startup code and a USB stack for communication with the other half of this project - a Guitar Hero-inspired game written in Python's PyGame library.

It does not make use of Raspberry Pi's SDK, and requires no external libraries, just certain standard C libraries *(such as `stdint.h`).*

### Project Motivation
This project started when I wanted to learn about and implement the USB stack from scratch, without using pre-built ones like [TinyUSB](https://docs.tinyusb.org/en/latest/) and without the Raspberry Pi SDK (instead opting in to use bare-metal C).

**But, why not at least use the SDK?**

Because ~~I have a lot of time on my hands~~ I believe that building something from the ground-up is the best way to learn how it works *(and I wanted an interesting project)*.

However, what I didn't know at the time is skipping the SDK meant skipping all of the pre-written startup code. I'm still stubborn enough to stick to my promise of skipping the SDK, so that meant I had to learn concepts like:
- the RP2040 boot sequence
- minimal Assembly for the ARM Cortex-M0+
- SPI/QSPI communication
- CRC32 checksums
- vector tables
- reset handlers
- linker scripts
Since most *(reasonable)* people just opt for the SDK - or at the very least opt for using pre-written startup code - I had to mostly rely on documentation and reading pre-written code to understand what's happening and, perhaps more importantly, *why* it's happening, so I've linked what I mostly relied on at the bottom of this file.

### Sources
These are the sources I references a lot while programming this:
#### Written Sources
- [RP2040 Datasheet](https://pip-assets.raspberrypi.com/categories/814-rp2040/documents/RP-008371-DS-1-rp2040-datasheet.pdf)
- [The Definitive Guide To ARM Cortex-M0 And Cortex-M0+ Processors by Joseph Yiu](https://www.sciencedirect.com/book/monograph/9780128032770/the-definitive-guide-to-arm-cortex-m0-and-cortex-m0-and-processors)
- [SPI NOR Flash Standard](https://www.winbond.com/hq/product/code-storage-flash-memory/serial-nor-flash/?__locale=en&partNo=W25Q80DV)
- [GCC documentation](https://gcc.gnu.org/onlinedocs)
- [Universal Serial Bus Specification](https://wcours.gel.ulaval.ca/GIF1001/old/h20/docs/USB_20.pdf)
- [USB - Device Class Definition for Human Interface Devices (HID)](https://www.usb.org/sites/default/files/hid1_11.pdf)
- [YouTube: Error Detection and Correction 2: Cyclic Redundancy Check](https://www.youtube.com/watch?v=6gbkoFciryA)
#### Other Repositories
- [vxj9800/bareMetalRP2040](https://github.com/vxj9800/bareMetalRP2040)
- [carlosftm/RPi-Pico-Baremetal](https://github.com/carlosftm/RPi-Pico-Baremetal)

**A huge thank you to all of the dedicated people for these resources! It wouldn't be possible without them.**
