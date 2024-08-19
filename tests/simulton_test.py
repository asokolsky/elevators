'''
Test launching/shutting FastAPI server programmatically
'''
import os
import requests
import signal
import subprocess
import time
import unittest

from elevators import rest_client, NewElevatorParams, ElevatorResponse

host = '127.0.0.1'
port = 9000
root = '/api/v1/elevators'

command_line = [
    'fastapi', 'run',
    '--host', host,
    '--port', str(port),
    '--workers', str(1),
    'elevators/elevator_simulton.py'
    #'python3', '--help'
]

class TestElevatorSimulton(unittest.TestCase):
    '''
    Verify launching/shutting a fastapi process
    '''

    @classmethod
    def setUpClass(cls):
        '''
        Launch FastAPI process
        '''
        print('setUpClass')
        #
        # start the simulton process
        #
        this_dir = os.path.dirname(os.path.realpath(__file__))
        parent_dir = os.path.abspath(this_dir + '/..')
        cls.popen = subprocess.Popen(
            command_line, cwd=parent_dir,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        #
        #
        #
        timeout = 5
        time_to_timeout = time.time() + timeout
        while time.time() < time_to_timeout:
            time.sleep(0.1)
            try:
                # are we there yet?
                x = requests.get(f'http://{host}:{9000}/')
                pass
                # YES!
            except Exception as e:
                # no
                print('Caught', e)
        assert time.time() < time_to_timeout
        #
        #
        # create client
        verbose = True
        dumpHeaders = True
        cls.restc = rest_client(host, port, verbose, dumpHeaders)
        return

    @classmethod
    def tearDownClass(cls):
        '''
        Shut FastAPI process
        '''
        print('tearDownClass')
        cls.restc.close()
        #
        # shut the simulton process
        #
        #cls.popen.terminate()
        os.kill(cls.popen.pid, signal.SIGINT)
        stdout_value, stderr_value = cls.popen.communicate()
        print('========================= FastAPI stdout =========================')
        print(stdout_value)
        print('========================= FastAPI stderr =========================')
        print(stderr_value)
        return

    def setUp(self):
        print('setUp', 'fastapi pid:', self.popen.pid)
        #
        # verify the FastAPI server is running
        #
        uri = '/'
        try:
            (status_code, rdata) = self.restc.get(uri)
            print('status_code:', status_code)
            print('rdata:', rdata)
        except requests.exceptions.ConnectionError as err:
            print('Caught:', err)
            self.assertFalse(err)
        return

    def tearDown(self):
        print('tearDown')
        return

    def test_all(self):
        '''
        This pretty much repeats elevator_simulton_test except a real HTTP
        communication is used, not test client.
        '''
        print('test_all', 'fastapi pid:', self.popen.pid)

        try:
            (status_code, rdata) = self.restc.get(f'{root}/')
            self.assertTrue(status_code, 200)
            self.assertEqual(rdata, [])
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

        except requests.exceptions.ConnectionError as err:
            print('Caught:', err)
            self.assertFalse(err)
        return
