'''
All the button-related stuff
'''
from typing import Callable, List


class Button:
    '''
    Simple (stateless) push button
    '''
    label = ''
    callback = None

    def __init__(self, label: str, callback: Callable) -> None:
        '''
        Initializer
        '''
        self.callback = callback
        self.label = label
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
        if self.callback is not None:
            self.callback(self)
        return

    def __repr__(self) -> str:
        '''
        Object print representation
        '''
        return f"<{type(self).__qualname__} '{self.label}' at {hex(id(self))}>"

class ButtonWithLed(Button):
    '''
    A push button with feedback LED
    '''
    led_on = False

    def __init__(self, label: str, callback: Callable) -> None:
        '''
        Initializer
        '''
        super().__init__(label, callback)
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

    def __repr__(self) -> str:
        '''
        Object print representation
        '''
        if self.led_on:
            annotated_label = '*' + self.label + '*'
        else:
            annotated_label = self.label
        return f"<{type(self).__qualname__} '{annotated_label}' at {hex(id(self))}>"

class ButtonWithLedPanel:
    '''
    A panel with N push buttons with feedback LEDs
    '''
    buttons = []
    callback = None

    def __init__(self, labels: List[str], callback: Callable) -> None:
        self.buttons = []
        self.callback = callback
        for label in labels:
            self.buttons.append(ButtonWithLed(label, self.button_callback))
        return

    def button_callback(self, button: Button) -> None:
        return

    def click(self, button: int) -> None:
        '''
        Definitive button action to be called by users.
        Activate button press and release, on release, I guess.
        '''
        self.buttons[button].click()
        self.on_click()
        return

    def on_click(self) -> None:  # [useless-return]
        '''
        Click event handler
        '''
        if self.callback is not None:
            self.callback(self, self.get_leds_on())
        return

    def get_leds_on(self) -> List[int]:
        '''
        update button led status
        '''
        return [
            i for i,button in enumerate(self.buttons) if button.is_on()
        ]

    def get_annotated_labels(self) -> List[str]:
        return [
            (button.is_on() and f'*{button.label}*') or button.label
                for button in self.buttons
        ]

    def __repr__(self) -> str:
        '''
        Object print representation
        '''
        return f"<{type(self).__qualname__} {self.get_annotated_labels()} at {hex(id(self))}>"
