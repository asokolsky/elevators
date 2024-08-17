from . import Elevator

from typing import List

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, PositiveInt, NonNegativeInt


#
# In this section we describe REST APIs inputs and outputs
#


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
    id: NonNegativeInt
    name: str


class Message(BaseModel):
    '''
    JSON carrying a single message in the body of the HTTP response
    '''
    message: str

    def __init__(self, message: str) -> None:
        super().__init__(message=message)
        return

#
# Create a REST API service
#


app = FastAPI(
    title='elevator',
    description='Elevator API',
    version='0.0.1',
    root_path='/api/v1/elevators')

elevators: List[Elevator] = []


@app.post(
    '/',
    response_model=ElevatorResponse,
    status_code=status.HTTP_201_CREATED)
async def create_elevator(params: NewElevatorParams):
    '''
    Handle new elevator creation
    '''
    el = Elevator(params.name, params.floors)
    global elevators   # [global-variable-not-assigned]
    elevators.append(el)
    return ElevatorResponse(id=len(elevators) - 1, name=el.name).model_dump()


@app.get('/', response_model=List[ElevatorResponse])
async def get_elevators():
    '''
    Get all the elevators
    '''
    global elevators   # [global-variable-not-assigned]
    return [
        ElevatorResponse(id=i, name=el.name).model_dump()
        for i, el in enumerate(elevators)
    ]


@app.get('/{id}', response_model=ElevatorResponse,
         responses={404: {"model": Message}})
async def get_elevator(id: NonNegativeInt):
    '''
    Get the specific elevator
    '''
    global elevators   # [global-variable-not-assigned]
    try:
        el = elevators[id]
    except IndexError:
        content = Message("Item not found").model_dump()
        return JSONResponse(status_code=404, content=content)
    return ElevatorResponse(id=id, name=el.name).model_dump()
