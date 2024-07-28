'''
All the elevator-related stuff
'''
from enum import Enum
from typing import List, Union

from .button import ButtonWithLedPanel # [relative-beyond-top-level]

class LoadValue(str, Enum):
    '''
    Possible values of the elevator load
    '''

    NONE = 'none'
    SOME = 'some'
    TOO_MUCH = 'too-much'

    @classmethod
    def is_valid(cls, st: Union[str, 'LoadValue']) -> bool:
        '''
        Valid value recognizer
        '''
        return st in LoadValue._value2member_map_

    def __repr__(self):
        '''
        To enable serialization as a string...
        '''
        return repr(self.value)


class ElevatorState(str, Enum):
    '''
    Possible values of the Elevator State
    '''

    IDLE = 'idle'

    @classmethod
    def is_valid(cls, st: Union[str, 'ElevatorState']) -> bool:
        '''
        Valid value recognizer
        '''
        return st in ElevatorState._value2member_map_

    def __repr__(self):
        '''
        To enable serialization as a string...
        '''
        return repr(self.value)


class Elevator:
    '''
    Elevator
    '''
    #
    # constant labels
    #
    label_open_doors = '< >'
    label_close_doors = '> <'
    #
    # in kg
    #
    max_load = 700
    #
    # Controls
    #
    panel = None # ButtonWithLedPanel(N, panel_callback)
    #
    # Attributes
    #
    current_floor = 0
    destination_floors: List[int] = []
    load = LoadValue.NONE
    state = ElevatorState.IDLE
    #
    # Indicators
    #

    def __init__(self, floors: int, current_floor: int) -> None:
        '''
        Initializer
        '''
        self.current_floor = current_floor
        self.destination_floors = []
        self.load = LoadValue.NONE
        self.state = ElevatorState.IDLE
        #
        # create the control panel
        #
        labels = [str(i) for i in range(1, floors+1)]
        labels.append(self.label_open_doors)
        labels.append(self.label_close_doors)
        self.panel = ButtonWithLedPanel(labels, self.panel_callback)
        return

    def panel_callback(
            self, panel: ButtonWithLedPanel, leds_on: List[int]) -> None:
        return

    def __repr__(self) -> str:
        '''
        Object print representation
        '''
        return f"<{type(self).__qualname__} {self.state} at {self.current_floor} {self.panel.get_annotated_labels()} at {hex(id(self))}>"
