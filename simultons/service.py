'''
FastAPI process launcher
'''

import os
import signal
import subprocess
from typing import Optional

from fastapi import FastAPI

from . import wait_until_reachable


class Service:
    '''
    FastAPI Service Launcher
    '''

    def __init__(self, path: str, port: int) -> None:
        '''
        path - to the python file which has FastAPI global app defined
        '''
        self._host = '127.0.0.1'
        self._path = path
        self._port = port
        self._popen = None
        self._health_uri = 'docs'
        self._app: Optional[FastAPI] = None
        return

    @property
    def host(self) -> str:
        '_host accessor'
        return self._host

    @property
    def port(self) -> int:
        '_port accessor'
        return self._port

    def get_app(self) -> FastAPI:
        '''
        To be called by within the service itself
        '''
        if self._app is None:
            self._app = FastAPI(
                title='simulation',
                description='Simulation API',
                version='0.0.1',
                root_path='/api/v1/simulation')
        return

    def launch(self) -> int:
        '''
        start the FastAPI service process, returns service process pid
        To be called by a client
        '''
        parent_dir = os.path.abspath(
            os.path.dirname(os.path.realpath(__file__)) + '/..')
        command_line = [
            'fastapi', 'run', '--host', self._host,
            '--port', str(self._port), '--workers', str(1), self._path
        ]
        self._popen = subprocess.Popen(
            command_line, cwd=parent_dir,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return self._popen.pid

    def wait_until_reachable(self, timeout: int) -> bool:
        '''
        give some breathing room for the process to start
        To be called by a client
        '''
        return wait_until_reachable(
            f'http://{self._host}:{self._port}/{self._health_uri}', timeout)

    def shutdown(self) -> bool:
        '''
        Stop the FastAPI service process
        To be called by a client
        '''
        os.kill(self._popen.pid, signal.SIGINT)
        stdout_value, stderr_value = self._popen.communicate()
        dashes = '==========================='
        print(dashes, 'FastAPI stdout', dashes)
        print(stdout_value)
        print(dashes, 'FastAPI stderr', dashes)
        print(stderr_value)
        return True
