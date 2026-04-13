# MicroPython (The Serial Workaround)

This was supposed to be the easiest among the three languages, but pride would not let me stop at just basic logic. Because of the challenge of proper input registration, it turned out to be I dare say harder than the other two. This phase turned into a deep dive into the back end of the project. Since MicroPython does not natively support HID libraries, I had to get creative to make the PC recognize the guitar, though admittedly a lot of AI was used for the HID part.

## The Eureka Moment: Serial Emulation

Instead of a standard plug-and-play controller, I programmed the Pico to mimic an HID device by sending raw data over the USB Serial port. By using sys.stdout.buffer.write(), I could bypass standard debugging text and send a pure, high-speed stream of button data directly to a custom reader on the PC. A solution that felt like a true Eureka moment.

## How it Works

### 1. Pico-Side Logic (Code-micro_over_serial.py)

* The Hardware Setup: The Pico uses its internal pull-up resistors for all 6 buttons. 
* An unpressed button reads as 1 and a pressed one as 0. 
* Bitmasking: To keep communication efficient, I pack the state of every button into a single 8-bit byte. 
* For example, hitting the Strum and Note 1 and Note 3 creates a bitmask of 0x85. 
* The Heartbeat: Every 500ms, the Pico sends a heartbeat signal. 
* This prevents the PC from getting stuck thinking a button is held down if a single data packet is missed. 

### 2. The PC-Side (guitar_reader.py)

DISCLAIMER: A lot of AI was used here because it was simply out of my bounds, so I cannot personally assure perfect efficiency.

Since the PC sees a serial port rather than a gamepad, I wrote a Python script using pyserial and threading to translate that data:

* Auto-Detect: The script scans COM ports to find the Pico specific Vendor ID (0x2E8A). 
* Background Listening: I used a background thread so the reader constantly listens for the Pico without blocking the main game loop. 
* The Lock: To prevent data corruption, I implemented a Lock system so the game loop and the serial reader never try to update the button state at the exact same millisecond. 

## The Debounce Dilemma

Physical buttons are messy. They bounce for about 10ms, producing rapid false reads. I chose a software solution that is both easy and efficient to filter this noise. My logic tracks every pin and requires a signal to stay steady for 20ms before it is officially accepted into the stable state.

## Wiring & Bitmask Map

| Component | GPIO Pin | Bitmask |
| :--- | :--- | :--- |
| Note 1 | GP2 | 0x01 |
| Note 2 | GP3 | 0x02 |
| Note 3 | GP4 | 0x04 |
| Note 4 | GP5 | 0x08 |
| Note 5 | GP6 | 0x10 |
| Strum Bar | GP7 | 0x80 |

---
*Part of the Zero to Pico Hero
