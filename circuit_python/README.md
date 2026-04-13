# CircuitPython (Adafruit's HID)

This is the most "plug-and-play" version of the project. By moving from MicroPython to CircuitPython, I was able to use the `usb_hid` library to make the Pico act as a native USB Gamepad.

## How it Works

### 1. The Custom Descriptor (`boot.py`)
This uses a custom **HID Report Descriptor** found in `boot.py`. This tells the PC exactly what the Pico is:
* **Device Type:** Gamepad
* **Report ID:** 4
* **Inputs:** 8 digital buttons (1 byte total)

### 2. Strum-to-Note Logic (`code.py`)
One of the decisions I made for it to be challanging was that, unlike a standard controller where every button press sends an immediate signal, this Guitar Hero controller requires a "Strum" input. In my case, instead of the standard swing motion for the strum, I used a button. 
* The code uses **Bitmasking** to combine the fret (note) states and the strum state into a single byte.
* The `str_requirement` function enforces that note bits are only sent if the strum bar (Bit 5) is active.

### 3. Debounce
Mechanical switches "bounce" when pressed, causing multiple unwanted inputs. I reused the same debounce timer logic from MicroPython:
* **Poll Interval:** 10ms
* **Debounce Threshold:** 20ms
* **Heartbeat:** Sends a report every 500ms even if no buttons are pressed, just to keep the connection "alive" and stable.

## Wiring Map
Unlike in MicroPython, this isn't very configurable; for example, we can't use bits 7 and 8 (0x40 and 0x80) because the report descriptor requires the bits to be sequential.

| Component | Pico Pin | Bitmask |
| :--- | :--- | :--- |
| Note 1    | GP2 | `0x01` |
| Note 2    | GP3 | `0x02` |
| Note 3    | GP4 | `0x04` |
| Note 4    | GP5 | `0x08` |
| Note 5    | GP6 | `0x10` |
| Strum Bar | GP7 | `0x20` |

---
*Built as a personal learning project.*
