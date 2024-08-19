'''
Playing with FastAPI, pydantic while simulating elevators
'''

from .button import Button, ButtonWithLed, ButtonWithLedPanel
# order is important to avoid circular dependency!
from .elevator import Elevator
from .elevator_simulton import app, NewElevatorParams, ElevatorResponse, \
    Message
from .restc import rest_client

__version__ = "0.0.1"

__all__ = [
    # button.py
    'Button',
    'ButtonWithLed',
    'ButtonWithLedPanel',
    # elevator_simulton.py
    'app',
    'NewElevatorParams',
    'ElevatorResponse',
    'Message',
    # elevator.py
    'Elevator',
    # restc.py
    rest_client
]
