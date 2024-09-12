'''
Simulation launcher which in turn launches all the simultons
'''
# import asyncio
import os
import signal
from typing import Dict, Optional
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.background import BackgroundTask
import zmq
import zmq.asyncio
from .globals import simulation_zspec, simulation_ztopic
from . import FastLauncher, \
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
        self._launcher.shutdown(timeout=1)
        return


async def shut_the_process():
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

    _zspec = simulation_zspec
    _ztopic = simulation_ztopic

    def __init__(self) -> None:
        '''
        Initializer
        '''
        self._state = SimulationState.INIT
        # start in paused
        self._rate = 0.0
        # start zmq publisher - destroyed in on_shutdown
        self._zcontext = zmq.asyncio.Context()
        self._zsocket = self._zcontext.socket(zmq.PUB)
        self._zsocket.bind(self._zspec)
        # simulton accumulator
        self._simultons: Dict[int, SimultonProxy] = {}
        self._next_simulton_port = 9500
        return

    async def broadcast_state_update(self) -> None:
        '''
        share the state update with the subscribers
        '''
        message = SimulationResponse(
            state=self._state, rate=self._rate).model_dump_json()
        assert self._zsocket is not None
        print('Broadcasting state update:', message)
        self._zsocket.send_string(f'{self._ztopic} {message}')
        return

    @property
    def state(self) -> SimulationState:
        '''Simulation state'''
        return self._state

    async def setState(self, state: SimulationState) -> SimulationState:
        if self._state == state:
            return state
        print(f'Simulation state {self._state} -> {state}')
        # update the state first
        self._state = state
        await self.broadcast_state_update()
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
        return

    def on_shutting(self) -> None:
        '''
        Simulation state just transitioned to SHUTTING
        '''
        print('Simulation.on_shutting', self)
        return

    async def on_startup(self) -> None:
        '''
        Simulation FastAPI startup event handler
        '''
        print('Simulation.on_startup')
        await self.setState(SimulationState.PAUSED)
        return

    async def on_shutdown(self) -> None:
        '''
        Simulation FastAPI shutdown event handler
        '''
        print('Simulation.on_shutdown', self)
        await self.setState(SimulationState.SHUTTING)
        print('Shutting the simultons')
        for _, s in self._simultons.items():
            s.shutdown()
        print('Closing zmq publisher')
        # close the zmq publisher
        # to avoid hanging infinitely
        self._zsocket.setsockopt(zmq.LINGER, 0)
        self._zsocket.close()
        self._zcontext.term()
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


theSimulation: Optional[Simulation] = None  # Simulation()
# let's try to delay instantiation to ensure that just importing the package
# does NOT create network resources


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
    global theSimulation
    theSimulation = Simulation()
    await theSimulation.on_startup()
    return


@app.on_event('shutdown')
async def shutdown_event():
    print('simulation shutdown_event')
    global theSimulation
    assert theSimulation is not None
    await theSimulation.on_shutdown()
    theSimulation = None
    return


@app.get('/api/v1/simulation', response_model=SimulationResponse)
async def get_simulation():
    '''
    Get the simulation state
    '''
    assert theSimulation is not None
    return SimulationResponse(
        state=theSimulation.state, rate=theSimulation.rate).model_dump()


@app.put(
    '/api/v1/simulation',
    response_model=SimulationResponse,
    status_code=202,
    responses={400: {"model": Message}})
async def put_simulation(req: SimulationRequest):
    '''
    Update the simulation state
    '''
    assert theSimulation is not None
    if req.rate is not None:
        theSimulation.rate = req.rate
    # this assignment will result in multiple functions being called
    await theSimulation.setState(req.state)
    if theSimulation.state == SimulationState.SHUTTING:
        background = BackgroundTask(shut_the_process)
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
    assert theSimulation is not None
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
    assert theSimulation is not None
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
    assert theSimulation is not None
    try:
        sim = theSimulation._simultons[id]
    except IndexError:
        content = Message("Item not found").model_dump()
        return JSONResponse(status_code=404, content=content)
    return sim.to_response()
