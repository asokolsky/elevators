'''
Playing with FastAPI, pydantic while simulating stuff
'''

from .button import Button, ButtonWithLed, ButtonWithLedPanel
from .restc import rest_client, wait_until_reachable
from .schemas import NewClockParams, ClockResponse, \
    NewElevatorParams, ElevatorResponse, Message, \
    SimulationRequest, SimulationResponse, \
    NewSimultonParams, SimultonResponse, ShutdownParams
# order is important to avoid circular dependency!
from .fast_launcher import FastLauncher
from .simulton import Simulton
from .elevator import Elevator
from .clock import Clock
from .simulation import Simulation, SimulationState, theSimulation

__version__ = "0.0.1"

__all__ = [
    # button.py
    'Button',
    'ButtonWithLed',
    'ButtonWithLedPanel',
    # clock.py
    'Clock',
    # fast_launcher.py
    'FastLauncher',
    # elevator_simulton.py
    'app',
    # elevator.py
    'Elevator',
    # restc.py
    'rest_client',
    'wait_until_reachable',
    # simulton.py
    'Simulton',
    # schemas.py
    'NewClockParams',
    'ClockResponse',
    'SimulationRequest',
    'SimulationResponse',
    'NewElevatorParams',
    'NewSimultonParams',
    'SimultonResponse',
    'NewElevatorParams',
    'ElevatorResponse',
    'Message',
    'ShutdownParams',
    # simulation.py
    'Simulation',
    'SimulationState',
    'theSimulation'
]
