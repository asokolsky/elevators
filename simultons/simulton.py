'''
A simulton is:

* a simulation entity with a REST API
* holds the instances of the relevant class to be accessed via the REST API.

This simulton is not related to https://ogden.eu/simultons/
'''
from enum import auto
import os
import random
import signal
import string
from typing import Any, Dict, Union
from fastapi_utils.enums import StrEnum


class SimultonState(StrEnum):
    '''
    Possible values of the Simulton state,
    which is somewhat related to the simulation state
    '''
    INIT = auto()
    RUNNING = auto()
    PAUSED = auto()
    SHUTTING = auto()

    @classmethod
    def is_valid(cls, st: Union[str, 'SimultonState']) -> bool:
        '''
        Valid value recognizer
        '''
        return st in SimultonState._value2member_map_

    def __repr__(self):
        '''
        To enable serialization as a string...
        '''
        return repr(self.value)


class Simulton:
    '''
    A unit of simulation with REST API exposed via FastAPI(s)
    '''
    def __init__(self, name: str = '') -> None:
        self._state = SimultonState.INIT
        self._rate: float = 0
        if not name:
            name = f'{type(self).__qualname__}@{hex(id(self))}'
        self._name = name
        self._instances: Dict[int, Any] = {}
        return

    @property
    def state(self) -> SimultonState:
        '''Simulton state'''
        return self._state

    @state.setter
    def state(self, state: SimultonState) -> SimultonState:
        '''Simulton state setter'''
        print(f'Simulton state {self._state} -> {state}')
        self._state = state
        return self._state

    @property
    def name(self) -> str:
        '''
        just get the name
        '''
        return self._name

    @property
    def rate(self) -> float:
        '''
        just get the rate
        '''
        return self._rate

    def on_startup(self) -> None:
        '''
        Simulton FastAPI app startup event handler
        '''
        self.state = SimultonState.PAUSED
        return

    def on_shutdown(self) -> None:
        '''
        Simulton FastAPI app shutdown event handler
        '''
        if self.state != SimultonState.SHUTTING:
            self.shutdown()
        return

    def shutdown(self) -> None:
        '''
        REST API handler
        '''
        self.state = SimultonState.SHUTTING
        pid = os.getpid()
        os.kill(pid, signal.SIGTERM)
        return

    def get_new_instance_id(self) -> str:
        length = 8
        id = ''.join(random.choice(string.ascii_lowercase)
                     for _ in range(length))
        return f'{type(self).__qualname__}#{id}'

    def add_instance(self, inst: Any, id: str = '') -> None:
        if not id:
            id = self.get_new_instance_id()
        self._instances[id] = inst
        return


#
# the derivatives have to have these:
#
# app = FastAPI(
#     title='clock',
#     description='FooBar API',
#     version='0.0.1')

# @app.on_event('startup')
# async def startup_event():
#     print('simulation startup_event')
#     theClockSimulton.on_startup()
#     return

# @app.on_event('shutdown')
# async def shutdown_event():
#     print('simulation shutdown_event')
#     theClockSimulton.on_shutdown()
#     return

# @app.put(
#    '/api/v1/simulton/shutdown',
#    response_model=Message,
#    status_code=202,
#    responses={400: {"model": Message}})
# async def shutdown(params: ShutdownParams):
#    '''
#    Handle new simulton shutdown request
#   '''
#    theClockSimulton.shutdown()
#    return Message(f'Clock simulton {pid} shutting down...').model_dump()
