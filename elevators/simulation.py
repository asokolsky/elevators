'''
Simulation launcher which in turn launches all the simultons
'''
from enum import Enum
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel, NonNegativeInt


class SimulationState(str, Enum):
    '''
    Possible values of the simulation state
    '''

    INIT = 'init'
    INITIALIZING = 'initializing'
    PAUSED = 'paused'
    RUNNING = 'running'
    SHUTTING = 'shutting'

    @classmethod
    def is_valid(cls, st: Union[str, 'SimulationState']) -> bool:
        '''
        Valid value recognizer
        '''
        return st in SimulationState._value2member_map_

    def __repr__(self):
        '''
        To enable serialization as a string...
        '''
        return repr(self.value)


class Simulation:
    '''
    Simulation launcher
    '''
    def __init__(self) -> None:
        '''
        Initializer
        '''
        self._state = SimulationState.INIT
        # start in paused
        self._rate = 0
        return

    @property
    def state(self) -> SimulationState:
        '''Simulation state'''
        return self._state

    @state.setter
    def state(self, state: SimulationState) -> SimulationState:
        print(f'Simulation state {self._state} -> {state}')
        self._state = state
        return self._state

    @property
    def rate(self) -> int:
        '''Simulation rate, 0 for paused '''
        return self._rate

    @rate.setter
    def rate(self, rate: int) -> int:
        print(f'Simulation rate {self._rate} -> {rate}')
        self._rate = rate
        return self._rate

    def is_paused(self) -> bool:
        '''
        is it paused?
        '''
        return self._rate == 0

    def __repr__(self) -> str:
        '''
        Object print representation
        '''
        return f"<{type(self).__qualname__} is {self._state} at {self._rate} at {hex(id(self))}>"


theSimulation = Simulation()


#
# In this section we describe REST APIs inputs and outputs
#
class SimulationStateResponse(BaseModel):
    '''
    JSON describing simulation state
    '''
    state: str
    rate: NonNegativeInt


class SimulationStateRequest(BaseModel):
    '''
    JSON describing simulation state
    '''
    state: str

#
# Create a REST API service
#


app = FastAPI(
    title='simulation',
    description='Simulation API',
    version='0.0.1',
    root_path='/api/v1/simulation')


@app.get('/state', response_model=SimulationStateResponse)
async def get_state():
    '''
    Get the simulation state
    '''
    return SimulationStateResponse(
        state=theSimulation.state, rate=theSimulation.rate).model_dump()

@app.put('/state', response_model=SimulationStateResponse)
async def put_state(req: SimulationStateRequest):
    '''
    Update the simulation state
    '''
    theSimulation.state = req.state
    return SimulationStateResponse(
        state=theSimulation.state, rate=theSimulation.rate).model_dump()

@app.get('/rate', response_model=SimulationStateResponse)
async def get_rate():
    '''
    Get the simulation rate
    '''
    return SimulationStateResponse(
        state=theSimulation.state, rate=theSimulation.rate).model_dump()
