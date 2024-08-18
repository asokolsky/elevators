'''
Test launching/shutting FastAPI server programmatically
'''
import subprocess
import unittest

host = '127.0.0.1'
port = 9000

command_line = [
    'fastapi',
    'run',
    '--host', host,
    '--port', port,
    '--workers', 1
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
        cls.popen = subprocess.Popen(
            command_line,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True)
        return

    @classmethod
    def tearDownClass(cls):
        '''
        Shut FastAPI process
        '''
        print('tearDownClass')
        return

    def setUp(self):
        print('setUp')
        return

    def tearDown(self):
        print('tearDown')
        return

    def test_all(self):
        print('test_all')
        output, errors = self.popen.communicate()
        print(output)
        print(errors)
        return
