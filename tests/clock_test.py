import time
import unittest
from simultons import Clock


class TestClockSimulton(unittest.TestCase):
    '''
    Verify Simulation Clock functionality
    '''

    def setUp(self):
        self._clock = Clock()
        return

    def tearDown(self):
        # self._clock.shut()
        self._clock = None
        return

    def test_all(self):
        '''
        Test the simulation clock functionality
        '''

        # clock was never started yet
        self.assertEqual(self._clock.time, 0)
        self.assertFalse(self._clock.on_pause())

        # start it at normal rate
        self.assertTrue(self._clock.on_run(1))
        duration = 0.1
        time.sleep(duration)
        print(duration, self._clock.time)
        self.assertGreaterEqual(self._clock.time, duration)

        return
