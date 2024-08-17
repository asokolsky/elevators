'''
All the elevator-related stuff
'''
from enum import Enum
from typing import List, Union

from .button import ButtonWithLedPanel  # [relative-beyond-top-level]


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

    # low power state for an empty elevator with closed doors
    IDLE = 'idle'
    # with or without load
    DOORS_OPENING = 'doors-opening'
    # with or without load
    DOORS_CLOSING = 'doors-closing'
    # moving to a destination floor with or without load
    GOING = 'going'
    # with or without load
    DOORS_OPENED = 'doors-opened'

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
    _label_open_doors = '< >'
    _label_close_doors = '> <'
    #
    # in kg
    #
    _min_load = 1
    _max_load = 700

    def __init__(self, name: str, floors: int, current_floor: int = 0) -> None:
        '''
        Initializer
        '''
        #
        # Instance Attributes
        #
        self._current_floor = current_floor
        self._current_load = 0
        self._destination_floors: List[int] = []
        self._name = name
        self._state = ElevatorState.IDLE
        #
        # Controls - create the control panel
        #
        labels = [str(i) for i in range(1, floors+1)]
        labels.append(self._label_open_doors)
        labels.append(self._label_close_doors)
        self._panel = ButtonWithLedPanel(labels, self.panel_callback)
        #
        # create indicators here
        # e.g. going up/down, current floor
        #
        return

    @property
    def name(self) -> str:
        '''
        just get the name
        '''
        return self._name

    def step_in(self, kilos: int) -> bool:
        '''
        passenger of weight kilos steps in
        '''
        if kilos <= 0:
            return False
        if self._state != ElevatorState.DOORS_OPENED:
            return False
        self._current_load += kilos
        return True

    def step_out(self, kilos: int) -> bool:
        '''
        passenger of weight kilos steps out
        '''
        if kilos <= 0:
            return False
        if self._state != ElevatorState.DOORS_OPENED:
            return False
        self._current_load -= kilos
        if self._current_load < 0:
            self._current_load = 0
        return True

    @property
    def load(self) -> LoadValue:
        '''
        returns the elevator's load value
        '''
        if self._current_load > self._max_load:
            return LoadValue.TOO_MUCH
        if self._current_load > self._min_load:
            return LoadValue.SOME
        return LoadValue.NONE

    def panel_callback(
            self, panel: ButtonWithLedPanel, leds_on: List[int]) -> None:
        '''
        Handle button press here.
        '''
        return

    def __repr__(self) -> str:
        '''
        Object print representation
        '''
        return f"<{type(self).__qualname__} {self._name} is {self._state} " \
            f"on {self._current_floor} floor {self._panel.annotated_labels} " \
            f"at {hex(id(self))}>"

    def floor_call(self, floor: int) -> None:
        '''
        Request for the elevator to go to that floor.
        '''
        return
