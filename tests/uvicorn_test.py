'''
Test launching/shutting uvicorn/FastAPI
'''
import fastapi
from multiprocessing import Process
import os
import signal
import time
import uvicorn
import unittest
from simultons import rest_client

app = fastapi.FastAPI()


@app.get('/hello')
async def hello():
    return {
        'message': 'hello world'
    }


@app.get('/shutdown')
async def shutdown():
    os.kill(os.getpid(), signal.SIGTERM)
    return {
        'message': 'Server shutting down...'
    }


@app.on_event('shutdown')
def on_shutdown():
    print('Server shutting down...')
    return


host = '127.0.0.1'
port = 8000


def launch_uvicorn() -> None:
    uvicorn.run(app, host=host, port=port, workers=1, log_level='debug')
    return


class TestUvicorn(unittest.TestCase):
    '''
    Verify launching/shutting a fastapi process
    '''

    @classmethod
    def setUpClass(cls):
        '''
        Launch uvicorn/FastAPI process
        '''
        print('setUpClass')
        cls.process = Process(target=launch_uvicorn)
        cls.process.start()

        # wait until it is reachable
        time.sleep(2)

        cls.restc = rest_client(host, port, True, True)
        return

    @classmethod
    def tearDownClass(cls):
        '''
        Shut uvicorn/FastAPI process
        '''
        print('tearDownClass')
        (status_code, rdata) = cls.restc.get(f'http://{host}:{port}/shutdown')
        cls.process.join()
        return

    def setUp(self):
        print('setUp')
        return

    def tearDown(self):
        print('tearDown')

        # send shutdown request

        return

    def test_all(self):
        '''
        Do smth abt it
        '''
        print('test_all')

        (status_code, rdata) = self.restc.get(f'http://{host}:{port}/hello')
        return
