"""
SoundButton
-----------

Play sounds when the button's status changes. This uses some
included sounds that were taken from ubuntu's system sounds.

You need the `pyglet` python package and `libavbin0` apt package
installed in order for this to work.

NOTE: while the sound is playing, the program is not reading the
device's status, so some events may be missed.

"""
from big_red import BigRedButton
import pyglet


def exit_playback(_):
    pyglet.app.exit()


class SoundButton(BigRedButton):

    def _play_sound(self, filename):
        sound = pyglet.media.load(filename)
        sound.play()
        pyglet.clock.schedule_once(exit_playback, sound.duration)
        pyglet.app.run()

    def on_cover_open(self):
        self._play_sound('examples/sounds/open.ogg')

    def on_cover_close(self):
        self._play_sound('examples/sounds/close.ogg')

    def on_button_press(self):
        self._play_sound('examples/sounds/press.ogg')


if __name__ == '__main__':
    button = SoundButton()
    button.run()
