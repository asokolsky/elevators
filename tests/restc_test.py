#
# HTTP Client Test
#
# Launch it by issuing:
#  python3 -m unittest -v restc_test
#
import asyncio
import time
import unittest
from json import loads
import httpx
from simultons import restc


class TestRestC(unittest.TestCase):
    '''
    Test HTTP client.
    We test the client against http://httpbin.org
    Here is what you can do:
    https://github.com/dcos/examples/tree/master/httpbin/1.9#use-httpbin
    '''

    def setUp(self):
        '''
        Executed prior to each test.
        '''
        self.host = 'httpbin.org'
        port = 80
        verbose = True
        dumpHeaders = True
        self.cl = restc.rest_client(self.host, port, verbose, dumpHeaders)

        return

    def tearDown(self):
        '''
        executed after each test
        '''
        self.cl.close()
        return

    def test_get(self):
        '''
        rest_client.get test
        '''
        uri = '/ip'
        (status_code, rdata) = self.cl.get(uri)
        self.assertEqual(status_code, 200)
        self.assertEqual(len(rdata), 1)
        self.assertTrue('origin' in rdata)

        uri = '/user-agent'
        (status_code, rdata) = self.cl.get(uri)
        self.assertEqual(status_code, 200)
        self.assertEqual(len(rdata), 1)
        self.assertTrue('user-agent' in rdata)
        ua = rdata['user-agent']
        self.assertTrue(ua.startswith('python'))

        uri = '/get'
        (status_code, rdata) = self.cl.get(uri)
        self.assertEqual(status_code, 200)
        expected = {
            'args': {},
            'headers': {
                'Accept': ['*/*'],
                'Accept-Encoding': ['gzip, deflate'],
                'Connection': ['keep-alive'],
                'Host': [self.host],
                'User-Agent': 'python-httpx/0.27.2'
            },
            # 'method': 'GET', optional
            'origin': '1.8.9.1:37470',
            'url': 'http://httpbin.io/get'
        }
        self.assertEqual(len(rdata), len(expected))
        self.assertEqual(rdata['args'], {})
        self.assertTrue('headers' in rdata)
        # self.assertEqual(rdata['method'], 'GET')
        self.assertTrue('origin' in rdata)
        self.assertTrue('url' in rdata)

        headers = rdata['headers']
        # self.assertEqual(len(headers), 6)
        self.assertTrue('Accept' in headers)
        self.assertTrue('Accept-Encoding' in headers)
        # self.assertTrue('Cache-Control' in headers)
        # self.assertTrue('If-Modified-Since' in headers)
        self.assertTrue('Host' in headers)
        self.assertTrue('User-Agent' in headers)
        return

    def test_post(self):
        '''
        rest_client.post test
        '''
        uri = '/post'
        da = {
            'a': 'value-of-a',
            'b': 1234,
            'c': {
                'd': ['I', 'love', 'REST'],
                'e': 'done'
            }
        }
        (status_code, rdata) = self.cl.post(uri, da)
        self.assertEqual(status_code, 200)
        expected = {
            'args': {},
            'headers': {
                'Accept': ['*/*'],
                'Accept-Encoding': ['gzip, deflate'],
                'Connection': ['keep-alive'],
                'Content-Length': ['78'],
                'Content-Type': ['application/json'],
                'Host': [self.host],
                'User-Agent': 'python-httpx/0.27.2'
            },
            # 'method': 'POST',
            'origin': '1.8.9.1:57320',
            'url': 'http://httpbin.io/post',
            'data': '{"a": "value-of-a", "b": 1234, "c": {"d": ["I", "love", "REST"], "e": "done"}}',
            'files': {},
            'form': {},
            'json': {
                'a': 'value-of-a',
                'b': 1234,
                'c': {
                    'd': ['I', 'love', 'REST'],
                    'e': 'done'
                }
            }
        }
        self.assertEqual(len(rdata), len(expected))
        self.assertTrue('args' in rdata)
        self.assertEqual(rdata['args'], {})
        self.assertTrue('data' in rdata)
        self.assertEqual(loads(rdata['data']), da)
        self.assertTrue('files' in rdata)
        self.assertTrue('form' in rdata)
        self.assertTrue('headers' in rdata)
        self.assertTrue('origin' in rdata)
        self.assertTrue('url' in rdata)
        return

    def test_delete(self):
        '''
        rest_client.delete test
        '''
        uri = '/delete'
        (status_code, rdata) = self.cl.delete(uri)
        self.assertEqual(status_code, 200)
        expected = {
            'args': {},
            'headers': {
                'Accept': ['*/*'],
                'Accept-Encoding': ['gzip, deflate'],
                'Connection': ['keep-alive'],
                'Content-Length': ['0'],
                'Host': [self.host],
                'User-Agent': 'python-httpx/0.27.2'
            },
            # 'method': 'DELETE',
            'origin': '1.8.9.1:42064',
            'url': f'http://{self.host}/delete',
            'data': '',
            'files': {},
            'form': {},
            'json': None
        }
        self.assertEqual(len(rdata), len(expected))
        self.assertEqual(rdata['args'], {})
        self.assertEqual(rdata['data'], '')
        self.assertEqual(rdata['files'], {})
        self.assertEqual(rdata['form'], {})
        self.assertTrue('headers' in rdata)
        self.assertTrue('json' in rdata)
        self.assertTrue('origin' in rdata)
        self.assertTrue('url' in rdata)
        return

    def test_put(self):
        '''
        rest_client.put test
        '''
        uri = '/put'
        da = {
            'a': 'value-of-a',
            'b': 1234,
            'c': {
                'd': ['I', 'love', 'REST'],
                'e': 'done'
            }
        }
        (status_code, rdata) = self.cl.put(uri, da)
        self.assertEqual(status_code, 200)
        expected = {
            'args': {},
            'headers': {
                'Accept': ['*/*'],
                'Accept-Encoding': ['gzip, deflate'],
                'Connection': ['keep-alive'],
                'Content-Length': ['78'],
                'Content-Type': ['application/json'],
                'Host': [self.host],
                'User-Agent': 'python-httpx/0.27.2'
            },
            # 'method': 'PUT',
            'origin': '1.8.9.1:55592',
            'url': 'http://httpbin.io/put',
            'data': '{"a": "value-of-a", "b": 1234, "c": {"d": ["I", "love", "REST"], "e": "done"}}',
            'files': {},
            'form': {},
            'json': {
                'a': 'value-of-a',
                'b': 1234,
                'c': {
                    'd': ['I', 'love', 'REST'],
                    'e': 'done'
                }
            }
        }
        self.assertEqual(len(rdata), len(expected))
        self.assertEqual(rdata['args'], {})
        self.assertEqual(loads(rdata['data']), da)
        self.assertEqual(rdata['files'], {})
        self.assertEqual(rdata['form'], {})
        self.assertTrue('headers' in rdata)
        self.assertEqual(rdata['json'], da)
        self.assertTrue('origin' in rdata)
        self.assertTrue('url' in rdata)
        return

    def test_patch(self):
        '''
        rest_client.patch test
        '''
        uri = '/patch'
        da = {
            'a': 'value-of-a',
            'b': 1234,
            'c': {
                'd': ['I', 'love', 'REST'],
                'e': 'done'
            }
        }
        (status_code, rdata) = self.cl.patch(uri, da)
        self.assertEqual(status_code, 200)
        expected = {
            'args': {},
            'headers': {
                'Accept': ['*/*'],
                'Accept-Encoding': ['gzip, deflate'],
                'Connection': ['keep-alive'],
                'Content-Length': ['78'],
                'Content-Type': ['application/json'],
                'Host': [self.host],
                'User-Agent': 'python-httpx/0.27.2'
            },
            # 'method': 'PATCH',
            'origin': '151.83.9.13:38166',
            'url': 'http://httpbin.io/patch',
            'data': '{"a": "value-of-a", "b": 1234, "c": {"d": ["I", "love", "REST"], "e": "done"}}',
            'files': {},
            'form': {},
            'json': {
                'a': 'value-of-a',
                'b': 1234,
                'c': {
                    'd': ['I', 'love', 'REST'],
                    'e': 'done'
                }
            }
        }
        self.assertEqual(len(rdata), len(expected))
        self.assertTrue('args' in rdata)
        self.assertEqual(rdata['args'], {})
        self.assertTrue('data' in rdata)
        self.assertEqual(loads(rdata['data']), da)
        self.assertTrue('files' in rdata)
        self.assertEqual(rdata['files'], {})
        self.assertTrue('form' in rdata)
        self.assertEqual(rdata['form'], {})
        self.assertTrue('headers' in rdata)
        self.assertTrue('json' in rdata)
        self.assertEqual(rdata['json'], da)
        self.assertTrue('origin' in rdata)
        self.assertTrue('url' in rdata)
        return

    async def get_one(self, client, uri) -> int:
        response = await client.get(uri)
        return response.status_code

    async def get_many(self) -> None:
        '''
        Try to GET multiple URIs in parallel
        '''
        uris = [
            '/ip', '/html',
            #'/dump/request',
            # '/image',
            '/user-agent', '/get', '/headers',
            '/json'
        ]
        print(f'Retrieving {len(uris)} URIs')
        start = time.time()

        async with httpx.AsyncClient(base_url=f'http://{self.host}') as client:
            results = await asyncio.gather(
                *(self.get_one(client, uri) for uri in uris))
            print(results)

        elapsed = time.time() - start
        print(f'Retrieved {len(uris)} URIs in {elapsed:.3f} secs')
        return

    def test_multiple_gets(self):
        '''
        Try rest_client.get in parallel.
        To run just this test:
        python3 -m unittest --verbose -k test_multiple_gets tests/restc_test.py
        '''
        asyncio.run(self.get_many())
        # produces:
        # Retrieving 7 URIs took 1.454 secs
        return


if __name__ == '__main__':
    unittest.main()
