'''
Testing the elevator-related stuff
'''
import unittest

from simultons import Elevator


class TestElevator(unittest.TestCase):
    '''
    Verify Elevator functionality
    '''

    def setUp(self):
        self.el = Elevator(None, 'test', 5)
        return

    def tearDown(self):
        self.el = None
        return

    def test_all(self):
        '''
        Test Elevator functionality
        '''
        print(self.el)
        return
