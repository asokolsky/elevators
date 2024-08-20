'''
FastAPI process launcher
'''
from . import wait_until_reachable

import os
import signal
import subprocess


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
        return

    @property
    def host(self) -> str:
        '_host accessor'
        return self._host

    @property
    def port(self) -> int:
        '_port accessor'
        return self._port

    def launch(self) -> int:
        '''
        start the FastAPI service process, returns service process pid
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
        '''
        return wait_until_reachable(
            f'http://{self._host}:{self._port}/{self._health_uri}', timeout)

    def shutdown(self) -> bool:
        '''
        Stop the FastAPI service process
        '''
        os.kill(self._popen.pid, signal.SIGINT)
        stdout_value, stderr_value = self._popen.communicate()
        dashes = '==========================='
        print(dashes, 'FastAPI stdout', dashes)
        print(stdout_value)
        print(dashes, 'FastAPI stderr', dashes)
        print(stderr_value)
        return True
