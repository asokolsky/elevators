'''NewClockParams
All the elevator-related stuff
'''
from enum import auto
import os
from typing import Dict, List, Union
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi_utils.enums import StrEnum
from pydantic import NonNegativeInt

from . import ButtonWithLedPanel, Simulton, ShutdownParams, \
    ElevatorResponse, NewElevatorParams, Message


class LoadValue(StrEnum):
    '''
    Possible values of the elevator load
    '''

    NONE = auto()
    SOME = auto()
    TOO_MUCH = auto()

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


class ElevatorState(StrEnum):
    '''
    Possible values of the Elevator State
    '''

    # low power state for an empty elevator with closed doors
    IDLE = auto()
    # with or without load
    DOORS_OPENING = auto()
    # with or without load
    DOORS_CLOSING = auto()
    # moving to a destination floor with or without load
    GOING = auto()
    # with or without load
    DOORS_OPENED = auto()

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

    def __init__(self, sim: Simulton, name: str, floors: int,
                 current_floor: int = 0) -> None:
        '''
        Initializer
        '''
        self._sim = sim
        self._id = sim.get_new_instance_id()
        self._name = name
        #
        # Instance Attributes
        #
        self._current_floor = current_floor
        self._current_load = 0
        self._destination_floors: List[int] = []
        self._estate = ElevatorState.IDLE
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

    def step_in(self, kilos: int) -> bool:
        '''
        passenger of weight kilos steps in
        '''
        if kilos <= 0:
            return False
        if self._estate != ElevatorState.DOORS_OPENED:
            return False
        self._current_load += kilos
        return True

    def step_out(self, kilos: int) -> bool:
        '''
        passenger of weight kilos steps out
        '''
        if kilos <= 0:
            return False
        if self._estate != ElevatorState.DOORS_OPENED:
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
        return f"<{type(self).__qualname__} {self._name} is {self._estate} " \
            f"on {self._current_floor} floor {self._panel.annotated_labels} " \
            f"at {hex(id(self))}>"

    def floor_call(self, floor: int) -> None:
        '''
        Request for the elevator to go to that floor.
        '''
        return


class ElevatorSimulton(Simulton):
    '''
    Simulton for elevators
    '''

    def __init__(self) -> None:
        '''
        Initializer
        '''
        super().__init__()
        return


theElevatorSimulton = ElevatorSimulton()


app = FastAPI(
    title='elevator',
    description='Elevator API',
    version='0.0.1')


@app.on_event('startup')
async def startup_event():
    print('elevators startup_event')
    theElevatorSimulton.on_startup()
    return


@app.on_event('shutdown')
async def shutdown_event():
    print('elevators shutdown_event')
    theElevatorSimulton.on_shutdown()
    return


@app.put(
    '/api/v1/simulton/shutdown',
    response_model=Message,
    status_code=202,
    responses={400: {"model": Message}})
async def shutdown(params: ShutdownParams):
    '''
    Handle simulton shutdown
    '''
    theElevatorSimulton.shutdown()
    pid = os.getpid()
    return Message(f'Elevator simulton {pid} shutting down...').model_dump()


@app.post(
    '/api/v1/elevators/',
    response_model=ElevatorResponse,
    status_code=status.HTTP_201_CREATED)
async def create_elevator(params: NewElevatorParams):
    '''
    Handle new instance creation
    '''
    el = Elevator(theElevatorSimulton, params.name, params.floors)
    return ElevatorResponse(id=el._id, name=el._name).model_dump()


@app.get('/api/v1/elevators', response_model=Dict[str, ElevatorResponse])
async def get_elevators():
    '''
    Get all the elevators
    '''
    return {
        id: ElevatorResponse(id=id, name=el._name).model_dump()
        for id, el in theElevatorSimulton._instances.enumerate()
    }


@app.get('/api/v1/elevators/{id}', response_model=ElevatorResponse,
         responses={404: {"model": Message}})
async def get_elevator(id: NonNegativeInt):
    '''
    Get the specific elevator
    '''
    global elevators   # [global-variable-not-assigned]
    try:
        el = elevators[id]
        return ElevatorResponse(id=id, name=el.name).model_dump()
    except IndexError:
        pass
    content = Message("Item not found").model_dump()
    return JSONResponse(status_code=404, content=content)
