'''
Simulation launcher which in turn launches all the simultons
'''
from enum import auto
import os
import signal
from typing import Dict, Union
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi_utils.enums import StrEnum
import zmq
from . import FastLauncher, Simulton, \
    SimulationRequest, SimulationResponse, \
    NewSimultonParams, SimultonResponse, Message, ShutdownParams


class SimultonProxy(Simulton):
    '''
    This is how simulation think of simulton(s)
    '''
    def __init__(self, source_path: str, port: int) -> None:
        super().__init__()
        self._launcher = FastLauncher(source_path, port)
        return

    def to_response(self) -> SimultonResponse:
        return SimultonResponse(
            state=self._state, port=self._launcher.port)

    @property
    def port(self) -> int:
        '_port accessor'
        return self._launcher.port

    def launch(self) -> int:
        '''
        Launch the simulton process
        '''
        return self._launcher.launch()

    def wait_until_reachable(self, timeout: int) -> bool:
        return self._launcher.wait_until_reachable(timeout)

    def shutdown(self):
        '''
        Shut the simulton process
        '''
        self._launcher.shutdown()
        return


class SimulationState(StrEnum):
    '''
    Possible values of the simulation state
    '''

    INIT = auto()
    INITIALIZING = auto()
    PAUSED = auto()
    RUNNING = auto()
    SHUTTING = auto()

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
    # _zspec = "tcp://*:5556"
    # _zspec = "ipc:///var/run/sss"
    _zspec = "ipc:///tmp/sss"

    def __init__(self) -> None:
        '''
        Initializer
        '''
        self._state = SimulationState.INIT
        # start in paused
        self._rate = 0
        # start zmq publisher
        self._zcontext = zmq.Context()
        self._zsocket = self._zcontext.socket(zmq.PUB)
        self._zsocket.bind(self._zspec)

        self._simultons: Dict[int, SimultonProxy] = {}
        self._next_simulton_port = 9500
        return

    @property
    def state(self) -> SimulationState:
        '''Simulation state'''
        return self._state

    @state.setter
    def state(self, state: SimulationState) -> SimulationState:
        print(f'Simulation state {self._state} -> {state}')
        self._state = state
        # share the sate update with the subscribers
        self._zsocket.send_string(SimulationResponse(
            state=self._state, rate=self._rate).model_dump_json())
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

    def shutdown(self) -> None:
        '''
        Simulation shutdown handler
        '''
        if self.state != SimulationState.SHUTTING:
            self.state = SimulationState.SHUTTING
            for _, s in self._simultons.items():
                s.shutdown()
        return

    def on_shutdown(self) -> None:
        '''
        Simulation shutdown event handler
        '''
        if self.state != SimulationState.SHUTTING:
            self.shutdown()
        return

    def on_startup(self) -> None:
        '''
        Simulation startup event handler
        '''
        self.state = SimulationState.PAUSED
        # signal.signal(signal.SIGINT, signal_handler)
        return

    def create_simulton(self, params: NewSimultonParams) -> SimultonResponse:
        '''
        Handle new simulton creation
        '''
        simulton = Simulton(params.src_path, self._next_simulton_port)
        if not simulton.launch():
            raise ValueError(f'Bad path {params.src_path}')
        self._simultons[simulton.port] = simulton
        self._next_simulton_port += 1
        return simulton.to_response()


theSimulation = Simulation()


'''
Create a REST API service
'''
app = FastAPI(
    title='simulation',
    description='Simulation API',
    version='0.0.1')


@app.on_event('startup')
async def startup_event():
    print('simulation startup_event')
    theSimulation.on_startup()
    return


@app.on_event('shutdown')
def shutdown_event():
    print('simulation shutdown_event')
    theSimulation.on_shutdown()
    return


@app.get('/api/v1/simulation', response_model=SimulationResponse)
async def get_simulation():
    '''
    Get the simulation state
    '''
    return SimulationResponse(
        state=theSimulation.state, rate=theSimulation.rate).model_dump()


@app.put('/api/v1/simulation', response_model=SimulationResponse)
async def put_state(req: SimulationRequest):
    '''
    Update the simulation state
    '''
    theSimulation.rate = req.rate
    theSimulation.state = req.state
    return SimulationResponse(
        state=theSimulation.state, rate=theSimulation.rate).model_dump()


@app.post(
    '/api/v1/simulation/simultons',
    response_model=SimultonResponse,
    status_code=201,
    responses={400: {"model": Message}})
async def create_simulton(params: NewSimultonParams):
    '''
    Handle new simulton creation
    '''
    try:
        return theSimulation.create_simulton(params)
    except ValueError as err:
        content = Message(f'Bummer: {err}').model_dump()
        return JSONResponse(status_code=400, content=content)


@app.get(
    '/api/v1/simulation/simultons',
    response_model=Dict[int, SimultonResponse])
async def get_simultons():
    '''
    Get the simulation rate
    '''
    return {
        port: s.to_response()
        for port, s in theSimulation._simultons.items()
    }


@app.get(
    '/api/v1/simulation/simultons/{id}',
    response_model=SimultonResponse,
    responses={404: {"model": Message}})
async def get_simulton(id: int):
    '''
    Get the simulation rate
    '''
    try:
        sim = theSimulation._simultons[id]
    except IndexError:
        content = Message("Item not found").model_dump()
        return JSONResponse(status_code=404, content=content)
    return sim.to_response()


@app.put(
    '/api/v1/simulton/shutdown',
    response_model=Message,
    status_code=202,
    responses={400: {"model": Message}})
async def shutdown_simulation(params: ShutdownParams):
    '''
    Handle new simulton creation
    '''
    theSimulation.shutdown()
    pid = os.getpid()
    os.kill(pid, signal.SIGTERM)
    return Message(f'Simulation {pid} shutting down...').model_dump()
