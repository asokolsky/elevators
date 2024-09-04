'''
A simulton is:

* a simulation entity with a REST API
* holds the instances of the relevant class to be accessed via the REST API.

This simulton is not related to https://ogden.eu/simultons/
'''
import os
import random
import signal
import string
from typing import Any, Dict
from fastapi import FastAPI
from . import SimultonResponse, SimultonState


def get_random_id() -> str:
    length = 8
    return ''.join(
        random.choice(string.ascii_lowercase) for _ in range(length))


class Simulton:
    '''
    A unit of simulation with REST API exposed via FastAPI(s).
    This class is ued as a parent to an actual class to be instantiated in the
    simulton process.
    '''
    title = 'FooBar'
    description = 'FooBar API'
    version = '0.0.1'

    def __init__(self, name: str = '') -> None:
        self._state = SimultonState.INIT
        self._rate: float = 0
        if not name:
            name = f'{type(self).__qualname__}@{hex(id(self))}'
        self._name = name
        # map of instance ID to the instance itself
        self._instances: Dict[str, Any] = {}
        return

    @property
    def state(self) -> SimultonState:
        '''Simulton state'''
        return self._state

    @state.setter
    def state(self, state: SimultonState) -> SimultonState:
        '''Simulton state setter'''
        if state == self._state:
            return state
        print(f'Simulton {self.title} {self._state} -> {state}')
        # old_state = self._state
        self._state = state
        if state == SimultonState.RUNNING:
            self.on_running()
        elif state == SimultonState.PAUSED:
            self.on_paused()
        elif state == SimultonState.SHUTTING:
            self.on_shutting()
        else:
            assert False
        return state

    def is_running(self) -> bool:
        return self._state == SimultonState.RUNNING

    def is_paused(self) -> bool:
        return self._state == SimultonState.PAUSED

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

    @rate.setter
    def rate(self, rate: float) -> float:
        '''Simulton rate setter'''
        if rate == self._rate:
            return rate
        print(f'Simulton rate {self._rate} -> {rate}')
        self._rate = rate
        return rate

    @property
    def instances(self) -> Dict[str, Any]:
        return self._instances

    def on_running(self) -> None:
        '''
        State just transitioned to RUNNING
        '''
        print('Simulton.on_running')
        return

    def on_paused(self) -> None:
        '''
        State just transitioned to PAUSED
        '''
        print('Simulton.on_paused')
        return

    def on_shutting(self) -> None:
        '''
        State just transitioned to SHUTTING
        '''
        print('Simulton.on_shutting')
        return

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
        return f'{self.title}-{get_random_id()}'

    def add_instance(self, inst: Any, id: str) -> None:
        assert id
        self._instances[id] = inst
        return

    def get_instance_by_id(self, id: str) -> Any:
        '''Raises KeyError if id is not a key'''
        return self._instances[id]

    def del_instance_by_id(self, id: str) -> None:
        '''Raises KeyError if id is not a key'''
        del self._instances[id]
        return

    def create_app(self) -> FastAPI:
        return FastAPI(
            title=self.title, description=self.description,
            version=self.version)

    def to_response(self) -> SimultonResponse:
        return SimultonResponse(
            description=self.description,
            rate=self.rate,
            state=self.state,
            title=self.title,
            version=self.version)

#
# the derivatives have to have these:
#
# theDerivedSimulton = ClockSimulton()
#
# app = theDerivedSimulton.create_app()

# @app.on_event('startup')
# async def startup_event():
#     print('simulation startup_event')
#     theDerivedSimulton.on_startup()
#     return

# @app.on_event('shutdown')
# async def shutdown_event():
#     print('simulation shutdown_event')
#     theDerivedSimulton.on_shutdown()
#     return

# @app.get('/api/v1/simulton', response_model=SimultonResponse)
# async def get_simulton():
#    '''
#    Get the simulton - state and all
#    '''
#    return theDerivedSimulton.to_response()

# @app.put(
#    '/api/v1/simulton',
#    response_model=SimultonResponse,
#    status_code=202,
#    responses={400: {"model": Message}})
# async def put_simulton(params: SimultonRequest):
#    '''
#    Handle a request to change the simulton state
#    '''
#    if req.rate is not None:
#        theDerivedSimulton.rate = req.rate
#    theDerivedSimulton.state = req.state
#    return theDerivedSimulton.to_response()
