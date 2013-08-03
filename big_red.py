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

statuses = {
    21: 'closed',
    22: 'depressed',
    23: 'open',
}

class BigRedButton(object):

    def __init__(self):
        self.device = usb.core.find(
            idVendor=VENDOR_ID, idProduct=PRODUCT_ID)

        if self.device is None:
            raise ValueError('Device not found')

        interface = self.device[0][(0, 0)]
        try:
            if self.device.is_kernel_driver_active(interface):
                self.device.detach_kernel_driver(interface)
        except USBError:
            print 'no kernel driver to detach'

        self.device.set_configuration()
        self.endpoint = self.device[0][(0, 0)][0]

    def _get_status(self):
        self._send_query()
        response = self._read_response()
        return statuses.get(response[0], 'unkown')

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
        previous = self._get_status()
        while True:
            status = self._get_status()
            if previous != status:
                self._handle_new_status(status)
            sleep(0.1)
            previous = status

    def _handle_unknown(self):
        print 'the button is now in an unknown state'

    def _handle_open(self):
        print 'the button cover has been opened!'

    def _handle_close(self):
        print 'the button cover has been closed'

    def _handle_button_press(self):
        print 'BOOM!'

    def _handle_new_status(self, new_status):
        callbacks = {
            'unknown': self._handle_unknown,
            'open': self._handle_open,
            'closed': self._handle_close,
            'depressed': self._handle_button_press,
        }
        method = callbacks[new_status]
        method()


if __name__ == '__main__':
    button = BigRedButton()
    button.run()
