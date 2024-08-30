'''
Schemas for the REST APIs inputs and outputs
'''
from pydantic import BaseModel, PositiveInt, NonNegativeInt


class NewClockParams(BaseModel):
    '''
    JSON describing new clock
    '''
    name: str


class ClockResponse(BaseModel):
    '''
    JSON describing simulation state
    '''
    id: str
    name: str
    time: float


class NewElevatorParams(BaseModel):
    '''
    JSON used to create a new elevator
    '''
    name: str
    floors: PositiveInt


class ElevatorResponse(BaseModel):
    '''
    JSON describing the elevator in the body of the HTTP response
    '''
    id: str
    name: str


class Message(BaseModel):
    '''
    JSON carrying a single message in the body of the HTTP response
    '''
    message: str

    def __init__(self, message: str) -> None:
        super().__init__(message=message)
        return


class NewSimultonParams(BaseModel):
    '''
    JSON describing new simulton
    '''
    src_path: str


class SimulationResponse(BaseModel):
    '''
    JSON describing simulation state
    '''
    state: str
    rate: NonNegativeInt


class SimulationRequest(BaseModel):
    '''
    JSON describing simulation state
    '''
    state: str
    rate: NonNegativeInt


class SimultonResponse(BaseModel):
    '''
    JSON describing simulton
    '''
    state: str
    port: int


class ShutdownParams(BaseModel):
    '''
    JSON describing Simulton Shutdown arguments
    '''
    message: str
