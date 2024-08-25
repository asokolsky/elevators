'''
Test launching/shutting FastAPI server programmatically
'''
import unittest
import requests

from simultons import rest_client, FastLauncher, NewElevatorParams, \
    ElevatorResponse


class TestSimulton(unittest.TestCase):
    '''
    Verify launching/shutting a fastapi process
    '''

    @classmethod
    def setUpClass(cls):
        '''
        Launch FastAPI process
        '''
        # print('setUpClass')
        cls._service = FastLauncher('simultons/elevator_simulton.py', 9000)
        #
        # start the simulton process
        #
        assert cls._service.launch()
        if not cls._service.wait_until_reachable(3):
            cls._service.shutdown()
            assert False
        #
        # create client
        #
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
        # print('setUp', 'fastapi pid:', self.popen.pid)
        #
        # verify the FastAPI server is running
        #
        uri = '/'
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
        return

    def test_all(self):
        '''
        This pretty much repeats elevator_simulton_test except a real HTTP
        communication is used, not test client.
        '''
        # print('test_all', 'fastapi pid:', self.popen.pid)

        root = '/api/v1/simulation'
        (status_code, rdata) = self.restc.get(f'{root}/state')
        self.assertTrue(status_code, 200)
        self.assertTrue(status_code, 200)
        expected = {'state': 'INIT', 'rate': 0}
        self.assertEqual(rdata, expected)
        #
        # Create some elevators
        #
        floors = 10
        names = ['foo', 'bar', 'baz']
        for id, name in enumerate(names):
            params = NewElevatorParams(name=name, floors=floors)
            (status_code, rdata) = self.restc.post(
                f'{root}/', params.model_dump())
            self.assertTrue(status_code, 201)
            expected = ElevatorResponse(id=id, name=name)
            self.assertEqual(
                rdata, expected.model_dump(), 'response as expected')
        #
        # retrieve them, one at a time
        #
        for id, name in enumerate(names):
            (status_code, rdata) = self.restc.get(f'{root}/{id}')
            expected = ElevatorResponse(id=id, name=name)
            self.assertEqual(
                rdata, expected.model_dump(), 'response as expected')
        #
        # retrieve them all
        #
        (status_code, rdata) = self.restc.get(f'{root}/')
        expected = []
        for id, name in enumerate(names):
            expected.append(ElevatorResponse(id=id, name=name).model_dump())
        print('received:', rdata)
        print('expected:', expected)
        self.assertEqual(rdata, expected, 'response as expected')

        return
