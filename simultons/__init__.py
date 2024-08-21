'''
Playing with FastAPI, pydantic while simulating elevators
'''

from .button import Button, ButtonWithLed, ButtonWithLedPanel
# order is important to avoid circular dependency!
from .elevator import Elevator
from .elevator_simulton import app, NewElevatorParams, ElevatorResponse, \
    Message
from .clock_simulton import Clock
from .restc import rest_client, wait_until_reachable
from .service import Service
from .simulation import Simulation, SimulationState, SimulationStateResponse

__version__ = "0.0.1"

__all__ = [
    # button.py
    'Button',
    'ButtonWithLed',
    'ButtonWithLedPanel',
    # clock_simulton.py
    'Clock',
    # elevator_simulton.py
    'app',
    'NewElevatorParams',
    'ElevatorResponse',
    'Message',
    # elevator.py
    'Elevator',
    # restc.py
    'rest_client',
    'wait_until_reachable',
    # service.py
    'Service',
    # simulation.py
    'Simulation',
    'SimulationState',
    'SimulationStateResponse'
]
