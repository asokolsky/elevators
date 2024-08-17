'''
Simulation launcher
'''
from enum import Enum
import multiprocessing
from typing import List, Union

from simulton import Simulton      # [relative-beyond-top-level]


class SimulationState(str, Enum):
    '''
    Possible values of the simulation state
    '''

    INIT = 'init'
    INITIALIZING = 'initializing'
    PAUSED = 'paused'
    RUNNING = 'running'
    SHUTTING = 'shutting'

    @classmethod
    def is_valid(cls, st: Union[str, 'SimulationState']) -> bool:
        '''
        Valid value recognizer
        '''
        return st in SimulationState._value2member_map_

    def __repr__(self):
        '''
        To enable serialization as a string...
        '''
        return repr(self.value)


class Simulation:
    '''
    Simulation launcher
    '''

    # IPC to broadcast commands to simultons
    to_sims = multiprocessing.JoinableQueue()
    # IPC to receive responses from simultons
    from_sims = multiprocessing.Queue()

    sims: List[Simulton] = []
    state: SimulationState = SimulationState.INIT

    def __init__(self) -> None:
        '''
        Initializer
        '''
        return

    def __repr__(self) -> str:
        '''
        Simulation print representation
        '''
        return f"<{type(self).__qualname__} in {self.state} with {self.sims} at {hex(id(self))}>"

    def initialize(self) -> None:
        '''
        promote state from INIT -> INITIALIZING -> PAUSED
        '''
        if self.state != SimulationState.INIT:
            raise ValueError

        self.state = SimulationState.INITIALIZING
        self.__start()
        self.state = SimulationState.PAUSED
        return

    def __start(self) -> None:
        '''
        Start all the simulton processes
        Not to be called by users.
        '''
        if self.state != SimulationState.INITIALIZING:
            raise ValueError
        for sim in self.sims:
            sim.start()
        return

    def shutdown(self) -> None:
        if self.state not in (SimulationState.PAUSED, SimulationState.RUNNING):
            return
            #raise ValueError
        # do the actual work here
        return

    def pause(self) -> None:
        '''
        promote state RUNNING -> PAUSED
        '''
        if self.state == SimulationState.PAUSED:
            return
        if self.state != SimulationState.RUNNING:
            raise ValueError
        # do the actual work here
        return

    def run(self, duration: int) -> None:
        '''
        promote state PAUSED -> RUNNING
        '''
        if self.state == SimulationState.RUNNING:
            return
        if self.state != SimulationState.PAUSED:
            raise ValueError
        return

    def add(self, sim_class: str, label: str) -> None:
        '''
        Create and add a simulton to the simulation
        '''
        if self.state == SimulationState.INITIALIZING:
            raise ValueError
        if self.state == SimulationState.SHUTTING:
            raise ValueError
        sim = sim_class(self.to_sims, self.from_sims, label)
        self.sims.append(sim)
        if self.state == SimulationState.INIT:
            return
        sim.start()
        return

    def remove(self, sim: Simulton) -> None:
        return
