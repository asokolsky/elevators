'''
All the elevator-related stuff
'''
from enum import Enum
from typing import List, Union


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
    # Controls
    #

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

        return
