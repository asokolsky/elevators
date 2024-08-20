'''
Clock simulton
'''
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
        self._time = 0
        return

    @property
    def time(self) -> float:
        '''
        Get the simulation time.
        This can be complex - depends on teh simulation state
        '''
        return self._time


theClock = Clock()

# In this section we describe REST APIs inputs and outputs


class ClockResponse(BaseModel):
    '''
    JSON describing simulation state
    '''
    time: float
#
# Create a REST API service
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
