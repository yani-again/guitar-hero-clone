#+-+  Wiring & Buttons config +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
"""
Bitmask layout (1 byte):
    Bit 0 (0x01) - Note 1
    Bit 1 (0x02) - Note 2
    Bit 2 (0x04) - Note 3
    Bit 3 (0x08) - Note 4
    Bit 4 (0x10) - Note 5
    Bit 5 (0x20) - Strum
    Bit 6 (0x40) - unused
    Bit 7 (0x80) - unused

"""
# +-+  Import modules  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-


import board
import digitalio
import time
import usb_hid

# +-+ Button initiazation +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-

def button(pin):
    btn = digitalio.DigitalInOut(pin)
    btn.direction = digitalio.Direction.INPUT
    btn.pull = digitalio.Pull.UP
    return btn

note_buttons = [
    button(board.GP2),   # Note 1 - bit 0
    button(board.GP3),   # Note 2 - bit 1
    button(board.GP4),   # Note 3 - bit 2
    button(board.GP5),   # Note 4 - bit 3
    button(board.GP6),   # Note 5 - bit 4
]

strum_button = button(board.GP7)   # Strum - bit 5

# +-+  Bitmasking  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-


note_bits = [0x01, 0x02, 0x04, 0x08, 0x10]                     # xx111111, more details at the top
strum_bit = 0x20

# +-+ HID gamepad setup +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-

# Finds the gamepad device from the list of enabled HID devices
# (it is enabled in boot.py with report ID 4)

gamepad = None
for device in usb_hid.devices:
    if device.usage == 0x05 and device.usage_page == 0x01:
        gamepad = device
        break

if gamepad is None:
    raise RuntimeError("Gamepad HID device not found. Error in boot.py")


# +-+  Timing Config  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-

POLL_INTERVAL  = 0.01    # 10ms 
HEARTBEAT      = 0.5     # 500ms
DEBOUNCE_TIME  = 0.02    # 20ms

# +-+  Debounce Logic  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-

# Same logic as MicroPython version, just using time.monotonic()
# instead of utime.ticks_ms(). CircuitPython saves seconds as floats
# rather than as integers as in MicroPython, this disallows for warping (starting from 0)
# in case of a overflow

all_buttons = note_buttons + [strum_button]
num_buttons = len(all_buttons)

stable    = [True] * num_buttons
candidate = [True] * num_buttons
cand_time = [0.0]  * num_buttons

def debounced():
    now = time.monotonic()
    for i, btn in enumerate(all_buttons):
        raw = btn.value                         # True = not pressed, False = pressed
        if raw != candidate[i]:
            # if state changed then resets the timer, don't update stable
            candidate[i] = raw
            cand_time[i]  = now
        elif (now - cand_time[i]) >= DEBOUNCE_TIME:
             # if held steady for 20ms then update as stable
            stable[i] = raw
    return stable


# +-+  Strum pressed check  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-

def str_requirement(states):
    strum_pressed = (states[5] == False)
    if not strum_pressed:
        return 0x00

    bitmask = strum_bit
    for i in range(5):                        # iterates over the fret button values index(0-4)
        if states[i] == False:                # checking for state False (pull_up)
            bitmask |= note_bits[i]
    return bitmask


# +-+  HID Report  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-

report_buffer = bytearray(1)

def send_report(report_byte):
    report_buffer[0] = report_byte
    gamepad.send_report(report_buffer, report_id=4)

# +-+  Main  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-

prev_bitmask     = None
prev_heartbeat  = time.monotonic()

print("Guitar controller activated, wating for input...")

while True:
    now    = time.monotonic()
    states = debounced()
    bitmask = str_requirement(states)

    state_changed = (bitmask != prev_bitmask)
    heartbeat_due = (now - prev_heartbeat) >= HEARTBEAT

    if state_changed or heartbeat_due:
        send_report(bitmask)
        prev_bitmask    = bitmask
        prev_heartbeat = now

    time.sleep(POLL_INTERVAL)

 # type: ignore
