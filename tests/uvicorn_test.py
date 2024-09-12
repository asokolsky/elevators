'''
Test launching/shutting uvicorn/FastAPI server process
'''
from multiprocessing import Process
import os
import signal
import unittest
import fastapi
import uvicorn
from simultons import rest_client, wait_until_reachable

host = '127.0.0.1'
port = 8000
app = fastapi.FastAPI()


@app.on_event('startup')
async def startup_event():
    print('Server starting up...')
    return


@app.on_event('shutdown')
async def on_shutdown():
    print('Server shutting down...')
    return


@app.get('/hello')
async def hello():
    return {
        'message': 'hello world'
    }


def shut_the_process() -> None:
    os.kill(os.getpid(), signal.SIGTERM)
    # raise KeyboardInterrupt
    return


@app.get('/shutdown')
async def shutdown(background_tasks: fastapi.BackgroundTasks):
    '''
    An endpoint to shut a FastAPI server
    '''
    # os.kill(os.getpid(), signal.SIGTERM)
    background_tasks.add_task(shut_the_process)
    return {
        'message': 'Server shutting down...'
    }


def launch_uvicorn() -> None:
    '''
    Start FastAPI uvicorn app
    see also:
    https://bugfactory.io/articles/starting-and-stopping-uvicorn-in-the-background/
    '''
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
        res = wait_until_reachable(f'http://{host}:{port}/hello', 2)
        assert res is not None

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
        return

    def test_all(self):
        '''
        Comprehensive functionality testing
        '''
        print('test_all')

        (status_code, rdata) = self.restc.get(f'http://{host}:{port}/hello')
        self.assertEqual(status_code, 200)
        return
