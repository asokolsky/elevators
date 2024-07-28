'''
All the button-related stuff
'''
from typing import Callable


class Button:
    '''
    Simple (stateless) push button
    '''

    def __init__(self, callback: Callable) -> None:
        '''
        Initializer
        '''
        self.callback = callback
        return

    def click(self) -> None:
        '''
        Definitive button action to be called by users.
        Activate button press and release, on release, I guess.
        '''
        self.on_click()
        return

    def on_click(self) -> None:
        '''
        Click event handler
        '''
        self.callback(self)
        return


class ButtonWithLed(Button):
    '''
    A push button with feedback LED
    '''
    led_on = False

    def __init__(self, callback: Callable) -> None:
        '''
        Initializer
        '''
        super().__init__(callback)
        self.led_on = False
        return

    def on_click(self) -> None:
        '''
        Handle button press and release, on release, I guess
        '''
        self.led_on = not self.led_on
        super().on_click()
        return

    def get_led(self) -> bool:
        '''
        Retrieve led status
        '''
        return self.led_on

    def is_on(self) -> bool:
        '''
        Retrieve led status
        '''
        return self.led_on


class ButtonWithLedPanel:
    '''
    A panel with N push buttons with feedback LEDs
    '''
    buttons = []
    leds_on = []

    def __init__(self, buttons: int, callback: Callable) -> None:
        self.buttons = []
        self.callback = callback
        self.leds_on = []
        for _ in range(buttons):
            self.buttons.append(ButtonWithLed(self.button_callback))
        return

    def button_callback(self, button: Button) -> None:
        return

    def click(self, button: int) -> None:
        '''
        Definitive button action to be called by users.
        Activate button press and release, on release, I guess.
        '''
        self.buttons[button].click()
        #
        # update button led status
        #
        self.leds_on = []
        i = 0
        for button in self.buttons:
            if button.is_on():
                self.leds_on.append(i)
            i += 1

        self.on_click()
        return

    def on_click(self) -> None:  # [useless-return]
        '''
        Click event handler
        '''
        self.callback(self, self.leds_on)
        return
