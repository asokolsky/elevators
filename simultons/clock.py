'''
Clock simulton
'''
import time
from fastapi import FastAPI
from pydantic import BaseModel


class Clock:
    '''
    Clock counting simulated time
    '''

    def __init__(self) -> None:
        '''
        Initializer
        '''
        # we will store the simulated time here...
        # in simulated seconds since the clock start
        self._rate = 0
        # accumulated simulation time until the last pause
        self._time = 0
        # os clock
        self._last_start = 0
        return

    def on_pause(self) -> bool:
        '''
        Simulation pause event handler
        '''
        if self._last_start == 0:
            # can't pause if we are not running
            return False
        if self._rate == 0:
            # can't pause if we are not running
            return False
        # accumulate _time
        assert self._rate != 0
        assert self._last_start != 0
        self._time += (time.time() - self._last_start) * self._rate
        self._last_start = 0
        self._rate = 0
        return True

    def on_run(self, rate: int) -> bool:
        '''
        Simulation run event handler
        '''
        if self._last_start != 0:
            # we are already running
            return False
        assert rate > 0
        assert self._last_start == 0
        self._last_start = time.time()
        self._rate = rate
        return True

    @property
    def time(self) -> float:
        '''
        Get the simulation time.
        This can be complex - depends on teh simulation state
        '''
        if self._rate == 0:
            return self._time
        assert self._rate > 0
        assert self._last_start > 0
        return self._time + ((time.time() - self._last_start) * self._rate)


theClock = Clock()

# In this section we describe REST APIs inputs and outputs


class ClockResponse(BaseModel):
    '''
    JSON describing simulation state
    '''
    time: float
#
# Create a REST API service - name of the global is significant!
#


app = FastAPI(
    title='clock',
    description='Clock API',
    version='0.0.1',
    root_path='/api/v1/clock')


@app.get('/', response_model=ClockResponse)
async def get_time():
    '''
    Get the simulated time
    '''
    return ClockResponse(time=theClock.time).model_dump()
