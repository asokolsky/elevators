'''
FastAPI process launcher
'''
import os
import signal
import subprocess
import time
from typing import Any, Dict, Optional
import httpx
from . import rest_client


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
        #
        # control REST client verbosity
        #
        verbose = True
        dumpHeaders = False
        self._restc = self.get_rest_client(verbose, dumpHeaders)
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

    def wait_until_reachable(
            self, health_uri: str, timeout: int) -> Optional[Dict[str, Any]]:
        '''
        give some room for the process to start.
        Returns a JSON produced by health_uri
        '''
        url = f'http://{self._host}:{self._port}{health_uri}'
        start = time.time()
        time_to_timeout = start + timeout
        print(f'wait_until_reachable({url}, {timeout})', end='', flush=True)
        assert self._popen is not None
        while time.time() < time_to_timeout:
            try:
                self._popen.wait(0.2)
                # if we are here, this means the process has terminated
                print(f'\nwait_until_reachable({url}, {timeout}) => None,'
                      f' after {time.time()-start:.2f} secs,'
                      ' process terminated')
                return None

            except subprocess.TimeoutExpired:
                print('.', end='', flush=True)

            try:
                # are we there yet?
                x = httpx.get(url, timeout=0.01)
                if x.status_code == 200:
                    # YES!
                    jres = x.json()
                    print(f'\nwait_until_reachable({url}, {timeout}) => {jres},'
                          f' after {time.time()-start:.2f} secs')
                    return jres

            except httpx.ConnectError:
                print('.', end='', flush=True)
                pass

        print(f'\nwait_until_reachable({url}, {timeout}) => None')
        return None

    def wait_to_die(self, timeout: float = 0.5) -> bool:
        assert self._popen is not None
        if self._popen.returncode is not None:
            print(f'Process {self._popen.pid} already terminated with ec:',
                  self._popen.returncode)
            return True
        #
        # wait for the process to actually terminate
        #
        print(f'Waiting for upto {timeout} secs for {self._popen.pid} to die...')
        try:
            self._popen.wait(timeout)
            # the process has terminated
            print(self._popen.pid, 'died, ec:', self._popen.returncode)
            return True

        except subprocess.TimeoutExpired:
            print(f'Waiting for {self._popen.pid} to die timed out after',
                  timeout, 'secs')
        return False

    def shutdown(self, timeout: float = 0.5) -> bool:
        '''
        Stop the FastAPI service process
        '''
        assert self._popen is not None
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
        res = self.wait_to_die(timeout)
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
