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
from simultons import async_rest_client, rest_client

uris = [
    '/ip', '/html', '/cookies',
    '/dump/request',
    '/gzip',
    # '/image',
    '/user-agent', '/get', '/headers', '/json', '/uuid'
]
user_agent = ['python-httpx/0.27.2']


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
        self.host = 'httpbin.io'
        port = 80
        verbose = True
        dumpHeaders = False
        self.cl = rest_client(self.host, port, verbose, dumpHeaders)
        self.acl = async_rest_client(self.host, port, verbose, dumpHeaders)

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
        self.assertIn('origin', rdata)

        uri = '/user-agent'
        (status_code, rdata) = self.cl.get(uri)
        self.assertEqual(status_code, 200)
        self.assertEqual(len(rdata), 1)
        self.assertIn('user-agent', rdata)
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
                'User-Agent': user_agent
            },
            'method': 'GET',  # optional
            'origin': '1.8.9.1:37470',
            'url': f'http://{self.host}/get'
        }
        self.assertEqual(len(rdata), len(expected))
        for hdr in ('args', 'method', 'url'):
            self.assertEqual(rdata[hdr], expected[hdr])
        self.assertIn('origin', rdata)
        self.assertIn('headers', rdata)
        headers = rdata['headers']
        # self.assertEqual(len(headers), 6)
        for hdr in ('Accept', 'Accept-Encoding', 'Host', 'User-Agent'):
            self.assertEqual(headers[hdr], expected['headers'][hdr])

        # self.assertIn('Cache-Control', headers)
        # self.assertIn('If-Modified-Since', headers)
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
                'User-Agent': user_agent
            },
            'method': 'POST',
            'origin': '1.8.9.1:57320',
            'url': 'http://httpbin.io/post',
            'data': '{"a": "value-of-a", ... "e": "done"}}',
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
        for hdr in ('args', 'method', 'files', 'url'):
            self.assertEqual(rdata[hdr], expected[hdr])
        self.assertIn('data', rdata)
        self.assertEqual(loads(rdata['data']), da)
        self.assertIn('origin', rdata)

        self.assertIn('headers', rdata)
        headers = rdata['headers']
        # self.assertEqual(len(headers), 6)
        for hdr in ('Accept', 'Accept-Encoding', 'Host', 'User-Agent'):
            self.assertEqual(headers[hdr], expected['headers'][hdr])

        # self.assertIn('Cache-Control', headers)
        # self.assertIn('If-Modified-Since', headers)
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
                'User-Agent': user_agent
            },
            'method': 'DELETE',
            'origin': '1.8.9.1:42064',
            'url': f'http://{self.host}/delete',
            'data': '',
            'files': {},
            'form': {},
            'json': None
        }
        self.assertEqual(len(rdata), len(expected))
        for hdr in ('args', 'method', 'data', 'files', 'form', 'json', 'url'):
            self.assertEqual(rdata[hdr], expected[hdr])

        self.assertIn('headers', rdata)
        headers = rdata['headers']
        for hdr in ('Accept', 'Accept-Encoding', 'Host', 'User-Agent'):
            self.assertEqual(headers[hdr], expected['headers'][hdr])
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
                'User-Agent': user_agent
            },
            'method': 'PUT',
            'origin': '1.8.9.1:55592',
            'url': 'http://httpbin.io/put',
            'data': '{"a": "value-of-a", ... "e": "done"}}',
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
        for hdr in ('args', 'method', 'files', 'form', 'json', 'url'):
            self.assertEqual(rdata[hdr], expected[hdr], hdr)
        self.assertEqual(loads(rdata['data']), da)
        self.assertIn('origin', rdata)
        self.assertIn('headers', rdata)
        headers = rdata['headers']
        for hdr in ('Accept', 'Accept-Encoding', 'Host', 'User-Agent'):
            self.assertEqual(headers[hdr], expected['headers'][hdr])
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
                'User-Agent': user_agent
            },
            'method': 'PATCH',
            'origin': '151.83.9.13:38166',
            'url': 'http://httpbin.io/patch',
            'data': '{"a": "value-of-a", ... "e": "done"}}',
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
        for hdr in ('args', 'method', 'files', 'form', 'json', 'url'):
            self.assertEqual(rdata[hdr], expected[hdr])
        self.assertEqual(loads(rdata['data']), da)
        self.assertIn('origin', rdata)
        self.assertIn('headers', rdata)
        headers = rdata['headers']
        for hdr in ('Accept', 'Accept-Encoding', 'Host', 'User-Agent'):
            self.assertEqual(headers[hdr], expected['headers'][hdr])
        return

    async def get_one(self, uri) -> int:
        # response = await client.get(uri)
        sc, jresp = self.acl.get(uri)
        return sc

    async def get_many(self) -> None:
        '''
        Try to GET multiple URIs in parallel
        '''
        print(f'Retrieving {len(uris)} URIs in parallel')
        start = time.time()

        results = await asyncio.gather(*(self.acl.get(uri) for uri in uris))

        elapsed = time.time() - start
        print(results)
        print(f'Retrieved {len(uris)} URIs in {elapsed:.3f} secs')
        return

    def test_multiple_gets_parallel(self):
        '''
        Try rest_client.get in parallel.
        To run just this test:
        python3 -m unittest -k test_multiple_gets_p tests/restc_test.py
        '''
        asyncio.run(self.get_many())
        # produces:
        # Retrieved 6 URIs in 1.043 secs
        return

    def test_multiple_gets_sequential(self):
        '''
        To run just this test:
        python3 -m unittest -k test_multiple_gets_s tests/restc_test.py
        '''
        print(f'Retrieving {len(uris)} URIs sequentially')
        start = time.time()

        for uri in uris:
            self.cl.get(uri)

        elapsed = time.time() - start
        print(f'Retrieved {len(uris)} URIs in {elapsed:.3f} secs')

        # produces:
        # Retrieved 6 URIs in 4.805 secs
        return


if __name__ == '__main__':
    unittest.main()
