big_red
=======

Python library to read and react to a 
[Big Red Button](http://www.dreamcheeky.com/big-red-button) 
(available on [amazon](http://www.amazon.com/Dream-Cheeky-902-Electronic-Reference/dp/B004D18MCK)).

This project uses [PyUSB](http://sourceforge.net/projects/pyusb/)
to communicate with the button and read its status.

I've tested this on Ubuntu, but you may have less luck 
running it on other platforms, due to the underlying USB library.


Let's push buttons
------------------

This library provides a class that can be extended to react 
to changes in the button's status. The USB button reports its
status as one of three things:

* closed -- the cover of the button is closed
* open -- the cover of the button is open
* depressed -- the button is being pressed down

The `BigRedButton` class will call one of four methods, depending
on how the button's status has changed:

* `on_cover_open` -- the cover has been opened
* `on_cover_closed` -- the cover has been closed
* `on_button_press` -- the big red button has been pressed
* `on_button_release` -- the big red button has been released

You can make the button do whatever you want by extending the
`BigRedButton` class and overriding the methods corresponding
to whichever action you want to react to.

### Simple Example

```python
from big_red import BigRedButton


class SimpleButton(BigRedButton):

    def on_button_press(self):
        print 'BOOM!'


if __name__ == '__main__':
    simple = SimpleButton()
    simple.run()

```

The `run` method will constantly poll the button's status and,
when the status changes, calls the appropriate method. In this 
example, `BOOM!` will be printed whenever the button is pressed.


## Ah, ah, ah, didn't say the magic word

Before plugging the USB button in, you may need to ensure that
sufficient permissions are given to read from the button. 

On linux, this can be done with [a `udev` rule](http://www.reactivated.net/writing_udev_rules.html).
You can create a file `/etc/udev/rules.d/99-big_red.rules` with
the following contents:

```
SUBSYSTEM=="usb", ATTR{idVendor}=="1d34", ATTR{idProduct}=="000d", MODE="666"
``` 

After restarting udev (`service udev restart`) and plugging the USB 
button back in, the button's status should be able to be read.
