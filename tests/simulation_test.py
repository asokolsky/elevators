'''
Testing the simulation/simulton stuff
'''
import unittest
import requests

from simultons import rest_client, FastLauncher, \
    SimulationStateResponse


root = '/api/v1/simulation'


class TestSimulation(unittest.TestCase):
    '''
    Verify Simulation launcher functionality
    '''
    @classmethod
    def setUpClass(cls):
        '''
        Launch FastAPI process
        '''
        #print('setUpClass')
        cls._service = FastLauncher('simultons/simulation.py', 9000)
        #
        # start the simulton process
        #
        assert cls._service.launch()
        if not cls._service.wait_until_reachable(3):
            cls._service.shutdown()
            assert False
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
        #print('tearDownClass')
        cls.restc.close()
        #
        # shut the simulton process
        #
        cls._service.shutdown()
        return

    def setUp(self):
        #uri = '/state'
        #try:
        #    (status_code, rdata) = self.restc.get(uri)
        #    # print('status_code:', status_code)
        #    # print('rdata:', rdata)
        #    self.assertEqual(status_code, 200)
        #except requests.exceptions.ConnectionError as err:
        #    print('Caught:', err)
        #    self.assertFalse(err)
        return

    def tearDown(self):
        return

    def test_all(self) -> None:
        '''
        Poke into the application service APIs
        '''
        try:
            (status_code, rdata) = self.restc.get(f'{root}/state')
            self.assertTrue(status_code, 200)
            expected = {'state': 'init', 'rate': 0}
            self.assertEqual(rdata, expected)

            (status_code, rdata) = self.restc.get(f'{root}/rate')
            self.assertTrue(status_code, 200)
            expected = {'state': 'init', 'rate': 0}
            self.assertEqual(rdata, expected)

        except requests.exceptions.ConnectionError as err:
            print('Caught:', err)
            self.assertFalse(err)
        return
