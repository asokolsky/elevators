'''
Testing the elevator-related stuff
'''
import unittest

from elevators import Elevator


class TestElevator(unittest.TestCase):
    '''
    Verify Elevator functionality
    '''

    def setUp(self):
        self.el = Elevator(5, 0)
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
