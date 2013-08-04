from big_red import BigRedButton


class BoringButton(BigRedButton):

    def on_unknown(self):
        print 'The button is in an unknown state'

    def on_cover_open(self):
        print 'The cover has been opened'

    def on_cover_close(self):
        print 'The cover has been closed'

    def on_button_press(self):
        print 'The button has been pressed'

    def on_button_release(self):
        print 'The button has been released'


if __name__ == '__main__':
    button = BoringButton()
    button.run()
