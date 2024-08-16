from typing import List

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, ValidationError

from .elevator import Elevator

app = FastAPI(
    title='elevator',
    description='Elevator API',
    version='0.0.1',
    root_path='/api/v1/elevators')

elevators: List[Elevator] = []


class NewElevatorResponse(BaseModel):
    id: int


@app.post('/', response_model=NewElevatorResponse,
          status_code=status.HTTP_201_CREATED)
async def create_elevator(name: str, floors: int):
    '''
    Handle new elevator creation
    '''
    el = Elevator(name, floors)
    global elevators
    elevators.append(el)
    return {
        'id': len(elevators) - 1,
    }


class ElevatorResponse(BaseModel):
    id: int
    name: str


@app.get('/', response_model=List[ElevatorResponse])
async def get_elevators():
    '''
    Get all the elevators
    '''
    global elevators
    return [{'id': i, 'name': el._name} for i, el in enumerate(elevators)]


@app.get('/{id}', response_model=ElevatorResponse)
async def get_elevator(eid: int):
    '''
    Get the specific elevator
    '''
    global elevators
    try:
        el = elevators[eid]
    except Exception:
        raise HTTPException(status_code=404, detail='Item not found')

    return {
        'id': eid,
        'name': el._name
    }
