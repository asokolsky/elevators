'''
Playing with FastAPI, pydantic while simulating stuff
'''

from .arestc import async_rest_client
from .button import Button, ButtonWithLed, ButtonWithLedPanel
from .restc import rest_client, wait_until_reachable
from .globals import simulation_zspec, simulation_ztopic
from .schemas import NewClockParams, ClockResponse, \
    NewElevatorParams, ElevatorResponse, Message, \
    SimulationState, SimulationRequest, SimulationResponse, \
    SimultonState, NewSimultonParams, SimultonRequest, SimultonResponse
# order is important to avoid circular dependency!
from .fast_launcher import FastLauncher
from .simulton import Simulton
from .elevator import Elevator
from .clock import Clock
from .simulation import Simulation, SimultonProxy, theSimulation

__version__ = '0.0.1'

__all__ = [
    # globals.py
    'simulation_ztopic',
    'simulation_zspec',
    # arestc.py
    'async_rest_client',
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
    'SimulationState',
    'SimulationRequest',
    'SimulationResponse',
    'NewElevatorParams',
    'SimultonState',
    'NewSimultonParams',
    'SimultonRequest',
    'SimultonResponse',
    'NewElevatorParams',
    'ElevatorResponse',
    'Message',
    # simulation.py
    'Simulation',
    'SimulationState',
    'theSimulation',
    'SimultonProxy'
]
