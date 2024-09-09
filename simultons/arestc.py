'''
Async REST client and other utilities
'''
from urllib.parse import urljoin
import time
from typing import Any, Optional, Tuple
from httpx import AsyncClient, Response
from requests import get
#from requests.exceptions import JSONDecodeError
JSONDecodeError = Exception


class rest_client:
    '''
    Async REST client
    '''

    def __init__(self, host: str, port: int, verbose: bool,
                 dumpHeaders: bool) -> None:
        '''
        In: iface - server interface, or host name
            port - server port
        '''
        self.base_url = f'http://{host}:{port}'
        self.verbose = verbose
        self.dumpHeaders = dumpHeaders
        self.ses = AsyncClient()
        return

    async def close(self) -> None:
        '''
        Close the underlying TCP connection
        '''
        await self.ses.aclose()
        return

    def print_req(self, method: str, url: str, data: Optional[Any]) -> None:
        if not self.verbose:
            return
        if data is None:
            data = ''
        print('HTTP', method, url, data, '...')
        return

    def print_resp(self, method: str, resp: Response) -> None:
        if self.verbose:
            try:
                jresp = resp.json()
            except JSONDecodeError as err:
                print('Caught: ', err)
                jresp = resp
            print('HTTP', method, '=>', resp.status_code, str(jresp))
        if self.dumpHeaders:
            print('HTTP Response Headers:')
            for h in resp.headers:
                print('   ', h, ':', resp.headers[h])
        return

    async def get(self, uri: str) -> Tuple[int, Any]:
        '''
        Issue HTTP GET to a base_url + uri
        returns (http_status, response_json)
        Throws requests.exceptions.ConnectionError when connection fails
        '''
        url = urljoin(self.base_url, uri)
        self.print_req('GET', url, None)
        resp = await self.ses.get(url)
        self.print_resp('GET', resp)
        try:
            jresp = resp.json()
        except JSONDecodeError as err:
            print('Caught: ', err)
            jresp = resp
        return (resp.status_code, jresp)

    async def post(self, uri: str, data: Any):
        '''
        Issue HTTP POST to a base_url + uri
        returns (http_status, response_json)
        Throws requests.exceptions.ConnectionError when connection fails
        '''
        url = urljoin(self.base_url, uri)
        self.print_req('POST', url, data)
        resp = await self.ses.post(url, json=data)
        self.print_resp('POST', resp)
        try:
            jresp = resp.json()
        except JSONDecodeError as err:
            print('Caught: ', err)
            jresp = resp
        return (resp.status_code, jresp)

    async def delete(self, uri: str) -> Tuple[int, Any]:
        '''
        Issue HTTP DELETE to a base_url + uri
        returns (http_status, response_json)
        Throws requests.exceptions.ConnectionError when connection fails
        '''
        url = urljoin(self.base_url, uri)
        self.print_req('DELETE', url, None)
        resp = await self.ses.delete(url)
        self.print_resp('DELETE', resp)
        try:
            jresp = resp.json()
        except JSONDecodeError as err:
            print('Caught: ', err)
            jresp = resp
        return (resp.status_code, jresp)

    async def put(self, uri: str, data: Any) -> Tuple[int, Any]:
        '''
        Issue HTTP PUT to a base_url + uri
        returns (http_status, response_json)
        Throws requests.exceptions.ConnectionError when connection fails
        '''
        url = urljoin(self.base_url, uri)
        self.print_req('PUT', url, data)
        resp = await self.ses.put(url, json=data)
        self.print_resp('PUT', resp)
        try:
            jresp = resp.json()
        except JSONDecodeError as err:
            print('Caught: ', err)
            jresp = resp
        return (resp.status_code, jresp)

    async def patch(self, uri: str, data: Any) -> Tuple[int, Any]:
        '''
        Issue HTTP PATCH to a base_url + uri
        returns (http_status, response_json)
        Throws requests.exceptions.ConnectionError when connection fails
        '''
        url = urljoin(self.base_url, uri)
        self.print_req('PATCH', url, data)
        resp = await self.ses.patch(url, json=data)
        self.print_resp('PATCH', resp)
        try:
            jresp = resp.json()
        except JSONDecodeError as err:
            print('Caught: ', err)
            jresp = resp
        return (resp.status_code, jresp)


def wait_until_reachable(url: str, timeout: int) -> Optional[Response]:
    '''
    Wait upto timeout secs until the url is reachable
    '''
    start = time.time()
    time_to_timeout = start + timeout
    print(f'wait_until_reachable({url}, {timeout})', end='', flush=True)
    while time.time() < time_to_timeout:
        time.sleep(0.1)
        try:
            # are we there yet?
            x = get(url)
            if x.ok:
                # YES!
                print(f'\nwait_until_reachable({url}, {timeout}) => {x},'
                      f' after {time.time()-start:.2f} secs')
                return x
        except Exception:
            print('.', end='', flush=True)
            pass
    print(f'\nwait_until_reachable({url}, {timeout}) => None')
    return None
