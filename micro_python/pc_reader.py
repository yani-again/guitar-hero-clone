"""
Guitar Hero Controller - PC Side (pygame + pyserial)
=====================================================
Reads the bitmask byte sent by the Pico over USB serial.

dependencies required:
    pip install pyserial pygame

Usage in game:
    from guitar_reader import GuitarController

    guitar = GuitarController()         # opens serial, starts reading
    guitar.start()

    # for game loop:
    state = guitar.get_state()
    if state['strum'] and state['notes'][0]:
        print("Note 1 strummed!")

    guitar.stop()                       # on game exit
"""

import serial
import serial.tools.list_ports
import threading
import time

# ── Bitmasks (MUST match the Pico code) ──────────────────────────────────────

NOTE_BITS = [0x01, 0x02, 0x04, 0x08, 0x10]
STRUM_BIT = 0x80

BAUD_RATE = 115200

# ── Auto-detect the Pico's serial port ───────────────────────────────────────

def find_pico_port():
    """

    Looks for the Raspberry Pi vendor ID (2E8A).
    Elsewise falls back to asking the user if not found.
    
    """
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if port.vid == 0x2E8A:   # Raspberry Pi vendor ID
            print(f"Pico found on {port.device}")
            return port.device

    # Fallback: list all ports and let the user pick
    print("Could not auto-detect Pico. Available ports:")
    for i, port in enumerate(ports):
        print(f"  [{i}] {port.device} - {port.description}")
    idx = int(input("Enter port number: "))
    return ports[idx].device

# ── Bitmask decoder ───────────────────────────────────────────────────────────

def decode_bitmask(byte_val):
    """
    Decodes a raw bitmask byte into an state dict.

    Returns:
        {
            'raw':   int,           # raw byte e.g. 0x85
            'strum': bool,          # true if strum is held
            'notes': [bool * 5],    # True for each note button held
        }

    If strum is not held, all notes will be False (Pico code enforces this,
    but we double-check here for safety).
    """
    strum = bool(byte_val & STRUM_BIT)
    notes = [bool(byte_val & bit) for bit in NOTE_BITS]

    if not strum:
        notes = [False] * 5   # safety: ignore notes if no strum

    return {
        'raw':   byte_val,
        'strum': strum,
        'notes': notes,
    }

# ── Controller class ──────────────────────────────────────────────────────────

class GuitarController:
    """
    Threaded serial reader. Runs in the background so it never
    blocks your game loop.
    """

    def __init__(self, port=None, baud=BAUD_RATE):
        self.port     = port or find_pico_port()
        self.baud     = baud
        self._state   = decode_bitmask(0x00)   # start with nothing pressed
        self._lock    = threading.Lock()
        self._running = False
        self._thread  = None
        self._ser     = None

    def start(self):
        """Open serial and start the background reader thread."""
        self._ser     = serial.Serial(self.port, self.baud, timeout=1)
        self._running = True
        self._thread  = threading.Thread(target=self._read_loop, daemon=True)
        self._thread.start()
        print(f"Guitar controller started on {self.port}")

    def stop(self):
        """Stop the reader thread and close the serial port."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=2)
        if self._ser and self._ser.is_open:
            self._ser.close()
        print("Guitar controller stopped")

    def get_state(self):
        """
        Returns the latest decoded button state (thread-safe).
        Call this every frame in your game loop.

        Example return value:
            {'raw': 133, 'strum': True, 'notes': [True, False, True, False, False]}
        """
        with self._lock:
            return dict(self._state)   # return a copy

    def _read_loop(self):
        """Background thread: continuously reads 1-byte packets from the Pico."""
        while self._running:
            try:
                data = self._ser.read(1)   # blocks until 1 byte arrives (or timeout)
                if data:
                    new_state = decode_bitmask(data[0])
                    with self._lock:
                        self._state = new_state
            except serial.SerialException as e:
                print(f"Serial error: {e}")
                self._running = False

# ── Simple test / demo (run this file directly to test without a game) ────────

if __name__ == "__main__":
    import sys

    print("Guitar Controller Test")
    print("Press Ctrl+C to exit\n")

    controller = GuitarController()
    controller.start()

    NOTE_NAMES = ["Green", "Red", "Yellow", "Blue", "Orange"]

    try:
        last_raw = -1
        while True:
            state = controller.get_state()

            # Only print when state changes
            if state['raw'] != last_raw:
                last_raw = state['raw']

                if state['raw'] == 0x00:
                    print("-- Released --")
                else:
                    held_notes = [NOTE_NAMES[i] for i in range(5) if state['notes'][i]]
                    notes_str  = " + ".join(held_notes) if held_notes else "(strum only)"
                    print(f"STRUM | Notes: {notes_str}  (raw: 0x{state['raw']:02X})")

            time.sleep(0.01)

    except KeyboardInterrupt:
        print("\nExiting...")
        controller.stop()
        sys.exit(0)
