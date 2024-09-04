'''
Simulation launcher which in turn launches all the simultons
'''
# import asyncio
import os
import signal
from typing import Dict
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.background import BackgroundTask
import zmq
from . import FastLauncher,  \
    SimulationState, SimulationRequest, SimulationResponse, \
    SimultonState, Simulton, NewSimultonParams, \
    SimultonRequest, SimultonResponse, Message


class SimultonProxy(Simulton):
    '''
    This is how simulation thinks of simulton(s)
    '''
    simulton_uri = '/api/v1/simulton'

    def __init__(self, source_path: str, port: int) -> None:
        super().__init__()
        self._launcher = FastLauncher(source_path, port)
        self.title = ''
        self.description = ''
        self.version = ''
        return

    def to_response(self) -> SimultonResponse:
        return SimultonResponse(
            description=self.description,
            port=self.port,
            rate=self.rate,
            state=self.state,
            title=self.title,
            version=self.version)

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
        jresp = self._launcher.wait_until_reachable(
            self.simulton_uri, timeout)
        if jresp is None:
            return False
        print('wait_until_reachable =>', jresp)
        self.description = jresp['description']
        self.rate = jresp['rate']
        self.title = jresp['title']
        self.version = jresp['version']
        self.state = jresp['state']
        return True

    def pause(self) -> bool:
        '''
        Move the simulton into the PAUSED state
        '''
        params = SimultonRequest(state=SimultonState.PAUSED)
        (status_code, rdata) = self._launcher._restc.put(
            self.simulton_uri, params.model_dump())
        return status_code == 202

    def run(self, rate: float = 1.0) -> bool:
        '''
        Move the simulton into the RUNNING state
        '''
        params = SimultonRequest(state=SimultonState.RUNNING, rate=rate)
        (status_code, rdata) = self._launcher._restc.put(
            self.simulton_uri, params.model_dump())
        return status_code == 202

    def shutdown(self):
        '''
        Shut the simulton process
        '''
        params = SimultonRequest(state=SimultonState.SHUTTING)
        (status_code, rdata) = self._launcher._restc.put(
            self.simulton_uri, params.model_dump())
        # if status_code != 202:
        self._launcher.shutdown()
        return


async def exit_app():
    '''
    This is how we exit FastAPI app
    '''
    # loop = asyncio.get_running_loop()
    # loop.stop()
    pid = os.getpid()
    os.kill(pid, signal.SIGTERM)
    print(f'Simulation {pid} shutting down...')
    return


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
        self._rate = 0.0
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
        if self._state == state:
            return state
        print(f'Simulation state {self._state} -> {state}')
        self._state = state
        # share the sate update with the subscribers
        self._zsocket.send_string(SimulationResponse(
            state=self._state, rate=self._rate).model_dump_json())
        if state == SimulationState.RUNNING:
            self.on_running()
        elif state == SimulationState.PAUSED:
            self.on_paused()
        elif state == SimulationState.SHUTTING:
            self.on_shutting()
        else:
            assert False
        return state

    @property
    def rate(self) -> float:
        '''Simulation rate, 0 for paused '''
        return self._rate

    @rate.setter
    def rate(self, rate: float) -> float:
        if self._rate == rate:
            return rate
        print(f'Simulation rate {self._rate} -> {rate}')
        self._rate = rate
        return self._rate

    def is_paused(self) -> bool:
        '''
        is it paused?
        '''
        return self._state == SimulationState.PAUSED

    def __repr__(self) -> str:
        '''
        Object print representation
        '''
        return f"<{type(self).__qualname__} is {self._state}" \
            " at {self._rate} at {hex(id(self))}>"

    def on_running(self) -> None:
        '''
        State just transitioned to RUNNING
        '''
        print('Simulation.on_running')
        for _, s in self._simultons.items():
            s.run(self._rate)
        return

    def on_paused(self) -> None:
        '''
        State just transitioned to PAUSED
        '''
        print('Simulation.on_paused')
        for _, s in self._simultons.items():
            s.pause()
        return

    def on_shutting(self) -> None:
        '''
        State just transitioned to SHUTTING
        '''
        print('Simulation.on_shutting')
        # TODO: make tis an async using httpx
        # https://stackoverflow.com/questions/71516140/fastapi-runs-api-calls-in-serial-instead-of-parallel-fashion/71517830#71517830
        for _, s in self._simultons.items():
            s.shutdown()
        # TODO  wait for all the simultons to shut...
        return

    def on_startup(self) -> None:
        '''
        Simulation FastAPI startup event handler
        '''
        print('Simulation.on_startup')
        self.state = SimulationState.PAUSED
        return

    def on_shutdown(self) -> None:
        '''
        Simulation FastAPI shutdown event handler
        '''
        print('Simulation.on_shutdown')
        self.state = SimulationState.SHUTTING
        return

    def shutdown(self) -> None:
        '''
        Simulation shutdown handler
        '''
        if self.state != SimulationState.SHUTTING:
            self.state = SimulationState.SHUTTING
        return

    def create_simulton(self, params: NewSimultonParams) -> SimultonResponse:
        '''
        Handle new simulton creation
        '''
        simulton = SimultonProxy(params.src_path, self._next_simulton_port)
        if not simulton.launch():
            raise ValueError(f'Bad path {params.src_path}')
        self._simultons[simulton.port] = simulton
        self._next_simulton_port += 1
        return simulton.to_response()

    def to_response(self) -> SimulationResponse:
        return SimulationResponse(state=self.state, rate=self.rate)


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


@app.put(
    '/api/v1/simulation',
    response_model=SimulationResponse,
    status_code=202,
    responses={400: {"model": Message}})
def put_simulation(req: SimulationRequest):
    '''
    Update the simulation state
    '''
    if req.rate is not None:
        theSimulation.rate = req.rate
    # this assignment will result in multiple functions being called
    theSimulation.state = req.state
    if theSimulation.state == SimulationState.SHUTTING:
        background = BackgroundTask(exit_app)
    else:
        background = None
    content = SimulationResponse(
        state=theSimulation.state, rate=theSimulation.rate).model_dump()
    return JSONResponse(content=content, background=background)

@app.post(
    '/api/v1/simultons',
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


@app.get('/api/v1/simultons', response_model=Dict[int, SimultonResponse])
async def get_simultons():
    '''
    Get the simulation rate
    '''
    return {
        port: s.to_response()
        for port, s in theSimulation._simultons.items()
    }


@app.get(
    '/api/v1/simultons/{id}',
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
