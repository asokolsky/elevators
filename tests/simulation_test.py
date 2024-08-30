'''
Testing the simulation/simulton stuff
'''
import unittest
import requests
from typing import Optional, Dict

from simultons import rest_client, wait_until_reachable, \
    FastLauncher, SimulationResponse, NewSimultonParams, SimultonResponse


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
        For all the test...
        '''
        print('setUpClass')
        return

    @classmethod
    def tearDownClass(cls):
        '''
        After all the tests...
        '''
        print('tearDownClass')
        return

    def setUp(self):
        '''
        For every test
        '''
        self._service = FastLauncher('simultons/simulation.py', 9000)
        #
        # start the simulation process
        #
        assert self._service.launch()
        if not self._service.wait_until_reachable(3):
            self._service.shutdown()
            assert False
        #
        #
        # create simulation REST client
        #
        verbose = True
        dumpHeaders = False
        self.restc = self._service.get_rest_client(verbose, dumpHeaders)
        return

    def tearDown(self):
        # print('tearDown')
        self.restc.close()
        self.restc = None
        self._service.shutdown()
        self._service = None
        return

    def tt_minimal(self) -> None:
        '''
        Minimum test of the simulation API
        '''
        assert self.restc is not None
        (status_code, rdata) = self.restc.get('/api/v1/simulation')
        self.assertTrue(status_code, 200)
        expected = {'state': 'PAUSED', 'rate': 0}
        self.assertEqual(rdata, expected)
        return

    def create_clock_simultons(
            self, num_simultons: int) -> Dict[int, SimultonResponse]:
        res: Dict[int, SimultonResponse] = {}
        assert self.restc is not None
        for _ in range(num_simultons):
            params = NewSimultonParams(src_path='simultons/clock.py')
            (status_code, rdata) = self.restc.post(
                '/api/v1/simulation/simultons', params.model_dump())
            self.assertEqual(status_code, 201)
            port = rdata['port']
            state = rdata['state']
            self.assertEqual(state, 'INIT')
            res[port] = SimultonResponse(state=state, port=port)
        return res

    def test_one_simulton(self) -> None:
        '''
        Minimum test of the simulation API
        '''
        assert self.restc is not None
        (status_code, rdata) = self.restc.get('/api/v1/simulation')
        self.assertTrue(status_code, 200)
        expected = {'state': 'PAUSED', 'rate': 0}
        self.assertEqual(rdata, expected)
        (status_code, rdata) = self.restc.get('/api/v1/simulation/simultons')
        self.assertTrue(status_code, 200)
        expected = {}
        self.assertEqual(rdata, expected)

        sims = self.create_clock_simultons(1)
        print(sims)
        self.assertEqual(len(sims), 1)
        for port, sim in sims.items():
            # reach out to the sim!
            url = f'http://127.0.0.1:{port}/api/v1/clock'
            self.assertTrue(wait_until_reachable(url, 5))
            resp = requests.get(url)
            self.assertAlmostEqual(resp.status_code, 200)
            print('Clock:', resp)
        return

    def tt_all(self) -> None:
        '''
        Poke into the application service APIs
        '''
        assert self.restc is not None
        (status_code, rdata) = self.restc.get('/api/v1/simulation')
        self.assertTrue(status_code, 200)
        expected = {'state': 'PAUSED', 'rate': 0}
        self.assertEqual(rdata, expected)

        (status_code, rdata) = self.restc.get('/api/v1/simulation/simultons')
        self.assertTrue(status_code, 200)
        expected = {}
        self.assertEqual(rdata, expected)
        #
        # create a few clock simultons
        #
        sims = self.create_clock_simultons(5)
        #
        #
        #
        (status_code, rdata) = self.restc.get('/api/v1/simulation/simultons')
        self.assertTrue(status_code, 200)
        self.assertEqual(len(rdata), len(sims))
        self.assertIsInstance(rdata, dict)

        self.assertEqual(rdata, sims)

        return
