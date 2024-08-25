'''
Testing the simulation/simulton stuff
'''
import unittest
import requests
from typing import Optional

from simultons import rest_client, FastLauncher, NewSimultonParams, \
    SimulationStateResponse, SimultonResponse


root = '/api/v1/simulation'


class TestSimulation(unittest.TestCase):
    '''
    Verify:
      * simulation launcher
      * creation and interaction with simultons
    '''

    def __init__(self, methodName: str = 'runTest') -> None:
        super().__init__(methodName)

        self.restc: Optional[rest_client] = None
        return

    @classmethod
    def setUpClass(cls):
        '''
        Launch FastAPI process
        '''
        # print('setUpClass')
        cls._service = FastLauncher('simultons/simulation.py', 9000)
        #
        # start the simulton process
        #
        assert cls._service.launch()
        if not cls._service.wait_until_reachable(3):
            cls._service.shutdown()
            assert False
        return

    @classmethod
    def tearDownClass(cls):
        '''
        Shut FastAPI simulation process
        '''
        # print('tearDownClass')
        #
        # shut the simulton process
        #
        cls._service.shutdown()
        return

    def setUp(self):
        #
        #
        # create client
        verbose = True
        dumpHeaders = False
        self.restc = self._service.get_rest_client(verbose, dumpHeaders)

        uri = f'{root}/state'
        try:
            (status_code, rdata) = self.restc.get(uri)
            # print('status_code:', status_code)
            # print('rdata:', rdata)
            self.assertEqual(status_code, 200)
        except requests.exceptions.ConnectionError as err:
            print('Caught:', err)
            self.assertFalse(err)
        return

    def tearDown(self):
        # print('tearDown')
        self.restc.close()
        self.restc = None
        return

    def test_all(self) -> None:
        '''
        Poke into the application service APIs
        '''
        assert self.restc is not None
        (status_code, rdata) = self.restc.get(f'{root}/state')
        self.assertTrue(status_code, 200)
        expected = {'state': 'INIT', 'rate': 0}
        self.assertEqual(rdata, expected)

        (status_code, rdata) = self.restc.get(f'{root}/rate')
        self.assertTrue(status_code, 200)
        expected = {'state': 'INIT', 'rate': 0}
        self.assertEqual(rdata, expected)

        (status_code, rdata) = self.restc.get(f'{root}/simultons')
        self.assertTrue(status_code, 200)
        expected = []
        self.assertEqual(rdata, expected)
        #
        # create a clock simulton
        #
        params = NewSimultonParams(src_path='simultons/clock.py')
        print('posting:', params.model_dump())
        (status_code, rdata) = self.restc.post(
            f'{root}/simultons', params.model_dump())
        self.assertTrue(status_code, 201)
        expected = SimultonResponse(state='INIT', port=9000)
        self.assertEqual(rdata, expected.model_dump())

        return
