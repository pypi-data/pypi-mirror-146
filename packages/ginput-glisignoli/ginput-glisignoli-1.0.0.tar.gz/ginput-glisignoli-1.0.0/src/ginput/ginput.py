#!/usr/bin/env python
import libevdev
import logging
import time
from ginput.keycodes import Keycodes

class ginput:
    def __init__(self):
        self._device = libevdev.Device()
        self._device.name = 'evdev-py-vkey'

    def _validate_chars(self, chars: str) -> bool:
        for c in chars:
            if c.lower() not in Keycodes.keycode:
                logging.error(f'{c} is not a valid key')
                return False

        return True

    def _setup(self, key_string: str) -> bool:
        if not self._validate_chars(key_string):
            logging.error('Invalid characters in key string')
            return False

        # self._device.enable(libevdev.EV_KEY.KEY_X)
        for c in key_string:
            new_c = f"libevdev.EV_KEY.{Keycodes.keycode[c.lower()]['code']}"
            self._device.enable(libevdev.EV_KEY.KEY_LEFTSHIFT)
            self._device.enable(eval(new_c))
        
        self._uinput = self._device.create_uinput_device()
        logging.info('device is now at {}'.format(self._uinput.devnode))

        return True

    def send_string(self, key_string: str) -> bool:
        time.sleep(0.05)
        for c in key_string:
            new_c = f"libevdev.EV_KEY.{Keycodes.keycode[c.lower()]['code']}"

            # Check if key is uppercase or lowercase
            if Keycodes.keycode[c.lower()]['capital'] or c.isupper():
                press = [
                    libevdev.InputEvent(libevdev.EV_KEY.KEY_LEFTSHIFT, 1),
                    libevdev.InputEvent(eval(new_c), 1),
                    libevdev.InputEvent(libevdev.EV_SYN.SYN_REPORT, value=0)
                ]
            else:
                press = [
                    libevdev.InputEvent(eval(new_c), value=1),
                    libevdev.InputEvent(libevdev.EV_SYN.SYN_REPORT, value=0)
                ]
            self._uinput.send_events(press)
            
            time.sleep(0.075)

            if Keycodes.keycode[c.lower()]['capital'] or c.isupper():
                release = [
                    libevdev.InputEvent(libevdev.EV_KEY.KEY_LEFTSHIFT, 0),
                    libevdev.InputEvent(eval(new_c), value=0),
                    libevdev.InputEvent(libevdev.EV_SYN.SYN_REPORT, value=0)
                ]
            else:
                release = [
                    libevdev.InputEvent(eval(new_c), value=0),
                    libevdev.InputEvent(libevdev.EV_SYN.SYN_REPORT, value=0)
                ]

            self._uinput.send_events(release)

        return True
