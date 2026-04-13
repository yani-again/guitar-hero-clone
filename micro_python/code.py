# +-+  Wiring & Buttons config +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
"""" 
Bitmask layout (1 byte):
    Bit 0 (0x01) - Note 1
    Bit 1 (0x02) - Note 2
    Bit 2 (0x04) - Note 3
    Bit 3 (0x08) - Note 4
    Bit 4 (0x10) - Note 5
    Bit 7 (0x80) - Strum   
"""


# +-+  Import modules  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-

from machine import Pin
import time
import sys

# +-+ Button initiazation +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-

All_Pins = [Pin(i, Pin.IN, Pin.PULL_UP) for i in range(2,8) ]     # GP2-GP7, more details at the top

# +-+  Bitmasking  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-

Note_bits = [0x01, 0x02, 0x04, 0x08, 0x10]                        # 1xx11111, more details at the top
Strum_bit =  0x80

# +-+  Timing Config  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-

Poll_intervals_ms = 10
Heartbeat_ms      = 500
Debounce_ms       = 20 

# +-+  Debounce Logic  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-

Num_Pins  = len(All_Pins)

stable    = [1] * Num_Pins      # [1, 1, 1, 1, 1, 1]
suspect   = [1] * Num_Pins      # [1, 1, 1, 1, 1, 1]
susp_time = [0] * Num_Pins      # [0, 0, 0, 0, 0, 0]

def debounced():
    now_time = time.ticks_ms()
    for i, pin in enumerate(All_Pins):
        raw = pin.value()
        if raw != suspect[i]:
            # if state changed then resets the timer, don't update stable
            suspect[i]   = raw
            susp_time[i] = now_time
        elif time.ticks_diff(now_time, susp_time[i] >= Debounce_ms):
             # if held steady for 20ms then update as stable
             stable[i] = raw
    return stable


# +-+  Strum pressed check  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-


def str_requirement(states):                           # states == stable from debounced
    strum_pressed = (states[5] == 0)                   # 0 == not pressed (pull-up)
    if not strum_pressed:
        return 0x00
    
    bitmask = Strum_bit           

    for i in range(5):                              # iterates over the fret button values index(0-4)
        if states[i] == 0:                          # checking for state 0 (pull_up)
            bitmask |= Note_bits[i]
    return bitmask


# +-+  Main  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-

def main():
    prev_bitmask   = None
    prev_heartbeat = time.ticks_ms()

    print("Guitar controller activated, wating for input...")

    while True:
        now_time     = time.ticks_ms()
        states  = debounced()
        bitmask = str_requirement(states)

        state_changed = (bitmask != prev_bitmask)
        heartbeat_due = time.ticks_diff(now_time, prev_heartbeat) >= Heartbeat_ms

        if state_changed or heartbeat_due:
            sys.stdout.buffer.write(bytes([bitmask]))
            prev_bitmask   = bitmask
            prev_heartbeat = now_time

        time.sleep_ms(Poll_intervals_ms)

main()
