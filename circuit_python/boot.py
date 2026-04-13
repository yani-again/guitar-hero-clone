import usb_hid


GAMEPAD_REPORT_DESCRIPTOR = bytes([
    0x05, 0x01,        # Usage Page (Generic Desktop)
    0x09, 0x05,        # Usage (Gamepad)
    0xA1, 0x01,        # Collection (Application)
    0x85, 0x04,        #   Report ID (4)
    0x05, 0x09,        #   Usage Page (Buttons)
    0x19, 0x01,        #   Usage Minimum (Button 1)
    0x29, 0x08,        #   Usage Maximum (Button 8)
    0x15, 0x00,        #   Logical Minimum (0)
    0x25, 0x01,        #   Logical Maximum (1)
    0x95, 0x08,        #   Report Count (8 buttons)
    0x75, 0x01,        #   Report Size (1 bit each)
    0x81, 0x02,        #   Input (Data, Variable, Absolute)
    0xC0               # End Collection
])

gamepad = usb_hid.Device(
    report_descriptor=GAMEPAD_REPORT_DESCRIPTOR,
    usage_page=0x01,                                     # Generic Desktop
    usage=0x05,                                          # Gamepad
    report_ids=(4,),                                     # Report ID 4
    in_report_lengths=(1,),                              # 1 byte per report (8 buttons)
    out_report_lengths=(0,)                              # output size declaration
)

# This enables the custom gamepad, disable everything else (pheperials) on the pico

usb_hid.enable((gamepad,))
