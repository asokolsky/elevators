import time
import unittest
from simultons import Clock, FastLauncher, SimulationStateResponse


class TestClock(unittest.TestCase):
    '''
    Verify Simulation Clock functionality
    '''

    def setUp(self):
        self._clock = Clock()
        return

    def tearDown(self):
        # self._clock.shut()
        self._clock = None
        return

    def test_all(self):
        '''
        Test the simulation clock functionality
        '''

        # clock was never started yet
        self.assertEqual(self._clock.time, 0)
        self.assertFalse(self._clock.on_pause())

        # start it at normal rate
        self.assertTrue(self._clock.on_run(1))
        duration = 0.1
        time.sleep(duration)
        print(duration, self._clock.time)
        self.assertGreaterEqual(self._clock.time, duration)

        return


class TestClockSimultonWithTestClient(unittest.TestCase):
    '''
    Verify Simulation Clock Simulton functionality
    '''

    @classmethod
    def setUpClass(cls):
        '''
        Launch simulation
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
        #
        # create client
        verbose = True
        dumpHeaders = False
        cls.restc = cls._service.get_rest_client(verbose, dumpHeaders)
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

    def test_all(self):
        '''
        Test the simulation clock functionality
        '''
        root = '/api/v1/simulation'

        (status_code, rdata) = self.restc.get(f'{root}/state')
        self.assertTrue(status_code, 200)
        expected = {'state': 'INIT', 'rate': 0}
        self.assertEqual(rdata, expected)

        (status_code, rdata) = self.restc.get(f'{root}/simultons')
        self.assertTrue(status_code, 200)
        expected = []
        self.assertEqual(rdata, expected)
        return
