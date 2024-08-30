'''
Clock simulation & simulton
'''
import time
import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from . import Simulton, NewClockParams, ClockResponse, Message, \
    ShutdownParams


class Clock:
    '''
    Clock counting simulated time
    '''

    def __init__(self, sim: Simulton, name: str) -> None:
        '''
        Initializer
        '''
        self._sim = sim
        self._id = sim.get_new_instance_id()
        self._name = name
        # accumulated simulation time until the last pause
        self._time: float = 0
        # os clock
        self._last_start: float = 0
        assert sim is not None
        sim.add_instance(self, self._id)
        return

    def on_pause(self) -> bool:
        '''
        Simulation pause event handler
        '''
        if self._last_start == 0:
            # can't pause if we are not running
            return False
        rate = self._sim._rate
        if rate == 0:
            # can't pause if we are not running
            return False
        # accumulate _time
        assert rate != 0
        assert self._last_start != 0
        self._time += (time.time() - self._last_start) * rate
        self._last_start = 0
        return True

    def on_run(self, rate: float) -> bool:
        '''
        Simulation run event handler
        '''
        if self._last_start != 0:
            # we are already running
            return False
        assert rate > 0
        assert self._last_start == 0
        self._last_start = time.time()
        return True

    @property
    def time(self) -> float:
        '''
        Get the simulation time.
        This can be complex - depends on teh simulation state
        '''
        if self._sim.rate == 0:
            return self._time
        assert self._sim._rate > 0
        assert self._last_start > 0
        return self._time + \
            ((time.time() - self._last_start) * self._sim._rate)

    def to_response(self) -> ClockResponse:
        return ClockResponse(
            id=self._id, name=self._name, time=self.time)


class ClockSimulton(Simulton):
    '''
    Clock counting simulated time
    '''

    def __init__(self) -> None:
        '''
        Initializer
        '''
        super().__init__()
        return


theClockSimulton = ClockSimulton()

#
# Create a REST API service - name of the global is significant!
#


app = FastAPI(
    title='clock',
    description='Clock API',
    version='0.0.1')


@app.on_event('startup')
async def startup_event():
    print('simulation startup_event')
    theClockSimulton.on_startup()
    return


@app.on_event('shutdown')
async def shutdown_event():
    print('simulation shutdown_event')
    theClockSimulton.on_shutdown()
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
    theClockSimulton.shutdown()
    pid = os.getpid()
    return Message(f'Clock simulton {pid} shutting down...').model_dump()


@app.post(
    '/api/v1/clocks/',
    response_model=ClockResponse,
    status_code=201)
async def create_instance(params: NewClockParams):
    '''
    Handle new instance creation
    '''
    cl = Clock(theClockSimulton, params.name)
    return cl.to_response().model_dump()


@app.get('/api/v1/clocks/{id}', response_model=ClockResponse)
async def get_time(id: str):
    '''
    Get the simulated time
    '''
    try:
        cl = theClockSimulton._instances[id]
        return cl.to_response().model_dump()
    except KeyError:
        pass
    content = Message("Item not found").model_dump()
    return JSONResponse(status_code=404, content=content)
