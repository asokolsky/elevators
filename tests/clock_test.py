'''
Testing all the clock functionality
'''
from elevators import rest_client, Service, SimulationStateResponse, Clock

import unittest
from typing import List


class TestClock(unittest.TestCase):
    '''
    Verify Simulation Clock functionality
    '''

    @classmethod
    def setUpClass(cls):
        '''
        Launch simulation
        '''
        # print('setUpClass')
        cls._service = Service('elevators/simulation.py', 9000)
        #
        # start the simulton process
        #
        assert cls._service.launch()
        assert cls._service.wait_until_reachable(10)
        #
        #
        # create client
        verbose = True
        dumpHeaders = False
        cls.restc = rest_client(
            cls._service.host, cls._service.port, verbose, dumpHeaders)
        return

    @classmethod
    def tearDownClass(cls):
        '''
        Shut FastAPI process
        '''
        # print('tearDownClass')
        cls.restc.close()
        #
        # shut the simulton process
        #
        cls._service.shutdown()
        return

    def setUp(self):
        return

    def tearDown(self):
        return
