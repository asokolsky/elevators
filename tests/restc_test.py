#
# HTTP Client Test
#
# Launch it by issuing:
#  python3 -m unittest -v restc_test
#

import unittest
from json import loads

from elevators import restc


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
        iface = 'httpbin.org'
        port = 80
        verbose = True
        dumpHeaders = True
        self.cl = restc.rest_client(iface, port, verbose, dumpHeaders)

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
        self.assertEqual(len(rdata), 4)
        self.assertTrue('args' in rdata)
        self.assertEqual(rdata['args'], {})
        self.assertTrue('headers' in rdata)
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
        self.assertEqual(len(rdata), 8)
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
        self.assertEqual(len(rdata), 8)
        self.assertTrue('args' in rdata)
        self.assertEqual(rdata['args'], {})
        self.assertTrue('data' in rdata)
        self.assertEqual(rdata['data'], '')
        self.assertTrue('files' in rdata)
        self.assertEqual(rdata['files'], {})
        self.assertTrue('form' in rdata)
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
        self.assertEqual(len(rdata), 8)
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
        self.assertEqual(len(rdata), 8)
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


if __name__ == '__main__':
    unittest.main()
