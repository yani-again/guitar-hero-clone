# RaspberryUSB
*RP2040 USB Device Drivers*

## About
Low-level USB device drivers for HID devices using the RP2040, implemented with no external libraries and designed to expose a large portion of the behaviour of the hardware USB controller.

The goal of RaspberryUSB is to be an abstraction layer between the hardware and software, allowing for a plug-and-play implementation of the USB protocol without reliance on bloated libraries.

As it's HID-focused, this means implementation is only supported for HID devices (e.g. keyboard, mouse, gamepad).

Taking a page out of  book, this is also a memory-safe implementation (no dynamic memory allocation).
As an unintended side-effect of the minimal approach, this is also a memory-safe USB implementation (no `malloc`)

## Motivation
Since the RP2040 is very limited on resources, the general functionality provided by libraries like [TinyUSB](https://github.com/hathach/tinyusb) can become noticeably bloated. While excellent production tools, they are (by nature) not as lean as some projects demand.

This is where RasberryUSB fits in.

As further motivation, USB is often treated as a black box. Large libraries make it trivial to use but don't let you understand what's happening under the surface.

RaspberryUSB tries its best to expose the inner workings of USB just enough to require a basic understanding of how USB works (for the learning experience), however it doesn't expect a level of technical knowledge anywhere near the likes of knowing the USB specification inside-out.

## Features
- Minimal USB device stack for the RP2040
- Follows the USB 2.0 specification
- HID device support (keyboard, mouse, gamepad)
- Full-speed USB (12 Mbps)
- Interrupt and endpoint support
    - Only control and interrupt endpoints supported currently
- Composite device support
- Lightweight, minimally abstracted driver-style API
- Designed to be a low-resource device USB implementation that aids with learning how USB works
- Memory safe (no `malloc`)

### Key Functionalities
- Provide easily digestible functions that require minimal USB specification knowledge to work with
- Directly handle enumeration and data transfers
- Provide a simple-to-use API for descriptor/endpoint configuration, IN/OUT transfer data buffers, and interrupt handling

## Getting Started

### Requirements
- RP2040 microcontroller
- C toolchain (ARM GCC)
- Basic knowledge of USB HID descriptors

### Installation
**TODO:** finish this once a working version is released

## API Overview

### Important Functions
```c
// TODO: complete once a working version is released
```

### Keyboard Enumeration Example
```c
// TODO: write keyboard enumeration code
```

## System Context
High-level overview of the driver's role in context to hardware/application layers.
```
┌─────────────────────────────┐
│        Application          │
├─────────────────────────────┤
│ Configure descriptors       │
│ Configure endpoints         │
│ Supply data for endpoints   │
│ Handle USB events           │
└─────────────▲───────────────┘
              │ API calls
┌─────────────┴───────────────┐
│        RaspberryUSB         │
├─────────────────────────────┤
│ Enumeration handling        │
│ Control transfers (EP0)     │
│ Descriptor management       │
│ Data transfer management    │
└─────────────▲───────────────┘
              │  USB engine
┌─────────────┴───────────────┐
│    RP2040 USB Controller    │
├─────────────────────────────┤
│ Endpoint buffers            │
│ CRC generation/check        │
│ Packet encoding/decoding    │
│ USB interrupts              │
└─────────────▲───────────────┘
              │  USB Bus
┌─────────────┴───────────────┐
│       USB Host Device       │
│     (Windows/Mac/Linux)     │
└─────────────────────────────┘
```

## Architecture
```
┌─── usb\_descriptors.c
│    all descriptors
│
├─── usb\_hw.c
│    USB controller interaction
│
├─── usb\_ep.c
│    endpoint configuration and buffer management
│
├─── usb\_control.c
│    control transfer handling
│
└─── usb.c
     public driver interface
```

## Limitations
No support for:
- Isochronous and bulk transfer support
- Non-HID devices
- Devices with multiple configurations
- Remote wakeup and suspend states
- Physical descriptors (the ones used during enumeration)

## Constraints
The RP2040's hardware USB controller poses several limitations for device-mode, the most notable being:
- Full-speed only (12 Mbps)
- Limited endpoint buffer memory (60 x 64-byte buffers)

## Non-Goals
***Currently,*** this project intentionally does ***not*** attempt to:
- replicate full production USB implementations
- support every USB device class
- support MCU's beyond the RP2040
- provide a high-level USB framework with extreme abstractions

## Future Improvements
Possible extensions could be:
- CDC or mass-storage class implementation
- integration with embedded RTOS-es
- higher-level abstractions
- support for an additional MCU

