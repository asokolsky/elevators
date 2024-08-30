'''
FastAPI process launcher
'''

import os
import signal
import subprocess
import time
from requests import get
from requests.exceptions import RequestException
from typing import Optional

from . import rest_client, ShutdownParams


class FastLauncher:
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
        self._popen: Optional[subprocess.Popen] = None
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
        print('command_line:', command_line)
        self._popen = subprocess.Popen(
            command_line, cwd=parent_dir,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return self._popen.pid

    def wait_until_reachable(self, timeout: int) -> bool:
        '''
        give some room for the process to start
        '''
        url = f'http://{self._host}:{self._port}/{self._health_uri}'
        start = time.time()
        time_to_timeout = start + timeout
        print(f'wait_until_reachable({url}, {timeout})', end='', flush=True)
        assert self._popen is not None
        while time.time() < time_to_timeout:
            try:
                self._popen.wait(0.2)
                # if we are here, this means the process has terminated
                print(f'\nwait_until_reachable({url}, {timeout}) => True, after {time.time()-start:.2f} secs, process terminated')
                return False

            except subprocess.TimeoutExpired:
                print('.', end='', flush=True)

            try:
                # are we there yet?
                x = get(url, timeout=0.01)
                if x.ok:
                    # YES!
                    print(f'\nwait_until_reachable({url}, {timeout}) => True, after {time.time()-start:.2f} secs')
                    return True

            except RequestException:
                pass

        print(f'\nwait_until_reachable({url}, {timeout}) => False')
        return False

    def request_shutdown(self) -> bool:
        '''
        Issue simulton shutdown request
        '''
        verbose = True
        dumpHeaders = True
        restc = self.get_rest_client(verbose, dumpHeaders)
        params = ShutdownParams(message='Ciao').model_dump()
        (status_code, rdata) = restc.put('/api/v1/simulton/shutdown', params)
        return (status_code == 202)

    def shutdown(self, timeout:float = 0.5) -> bool:
        '''
        Stop the FastAPI service process
        '''
        assert self._popen is not None
        if not self.request_shutdown():
            if self._popen.returncode is None:
                try:
                    os.kill(self._popen.pid, signal.SIGINT)
                except ProcessLookupError:
                    print('Failed to locate process:', self._popen.pid)
            else:
                print('FastAPI is already down, ec:', self._popen.returncode)
        #
        # wait for the process to actually terminate
        #
        res = True
        try:
            self._popen.wait(timeout)
            # the process has terminated
            print(f'Process {self._popen.pid} shut, ec: {self._popen.returncode}')
            res = True

        except subprocess.TimeoutExpired:
            print(f'Failed to shut {self._popen.pid}')
            res = False
        #
        # get the child's stdout and stderr
        #
        stdout_value, stderr_value = self._popen.communicate()
        dashes = '==========================='
        print(dashes, self._path, self._popen.pid, 'stdout', dashes, '\n',
              stdout_value,
              dashes, self._path, self._popen.pid, 'stderr', dashes, '\n',
              stderr_value,
              dashes, self._path, self._popen.pid, 'end', dashes)
        return res

    def get_rest_client(self, verbose: bool, dumpHeaders: bool):
        return rest_client(self._host, self._port, verbose, dumpHeaders)
