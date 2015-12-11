from time import sleep

from usb import USBError
from usb.util import (
    build_request_type,
    CTRL_OUT, 
    CTRL_TYPE_CLASS, 
    CTRL_RECIPIENT_INTERFACE,
)
import usb.core


VENDOR_ID = 0x1d34
PRODUCT_ID = 0x000d


class ButtonStatus(object):
    """Maps status codes to readable statuses."""

    CLOSED = 21
    """The button cover is closed."""
    DEPRESSED = 22
    """The button is being pressed."""
    OPEN = 23
    """The button cover is open."""
    RELEASED = 999
    """The button has been released."""


class BigRedButton(object):

    def __init__(self):
        self.device = usb.core.find(
            idVendor=VENDOR_ID, idProduct=PRODUCT_ID)

        if self.device is None:
            raise ValueError('Device not found')

        interface = self.device[0][(0, 0)].iInterface
        if self.device.is_kernel_driver_active(interface):
            self.device.detach_kernel_driver(interface)

        self.device.set_configuration()
        self.endpoint = self.device[0][(0, 0)][0]

    def _get_status(self):
        self._send_query()
        response = self._read_response()
        return response[0]

    def _send_query(self):
        command = bytearray(8)
        command[0] = 0x08
        command[-1] = 0x02
        bmRequestType = build_request_type(
            CTRL_OUT, CTRL_TYPE_CLASS, CTRL_RECIPIENT_INTERFACE)
        self.device.ctrl_transfer(
            bmRequestType=bmRequestType,
            bRequest=0x09,
            wValue=(2 << 8 | 0x08),
            wIndex=0,
            data_or_wLength=command,
        )

    def _read_response(self):
        return self.device.read(
            self.endpoint.bEndpointAddress, 
            self.endpoint.wMaxPacketSize,
        )

    def run(self):
        try:
            self._run_loop()
        except KeyboardInterrupt:
            pass

    def _run_loop(self):
        previous = self._get_status()
        while True:
            status = self._get_status()
            if previous != status:
                if previous == ButtonStatus.DEPRESSED:
                    self._handle_new_status(
                        ButtonStatus.RELEASED)
                else:
                    self._handle_new_status(status)
            sleep(0.1)
            previous = status

    def on_unknown(self):
        """The device is in an unknown state."""

    def on_cover_open(self):
        """The device's cover has been opened."""

    def on_cover_close(self):
        """The device's cover has been closed."""

    def on_button_press(self):
        """The big red button has been pressed."""

    def on_button_release(self):
        """The big red button has been released."""

    def _handle_new_status(self, new_status):
        callbacks = {
            ButtonStatus.OPEN: self.on_cover_open,
            ButtonStatus.CLOSED: self.on_cover_close,
            ButtonStatus.DEPRESSED: self.on_button_press,
            ButtonStatus.RELEASED: self.on_button_release,
        }
        method = callbacks.get(new_status, self.on_unknown)
        method()


if __name__ == '__main__':
    button = BigRedButton()
    button.run()
