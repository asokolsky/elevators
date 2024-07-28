'''
Testing the button-related stuff
'''
import unittest

from .button import Button, ButtonWithLed # [relative-beyond-top-level]


class TestButton(unittest.TestCase):
    '''
    Verify Button functionality
    '''

    clicks = 0

    def setUp(self):
        self.button = Button(self.callback)
        return

    def tearDown(self):
        self.button = None
        return

    def callback(self, button: Button) -> None:
        '''
        Button callback
        '''
        self.clicks += 1
        self.assertEqual(button, self.button)
        return

    def test_all(self):
        '''
        Test Button functionality
        '''
        clicks_old = self.clicks
        self.button.click()
        self.assertAlmostEqual(self.clicks,  clicks_old + 1)
        return


class TestButtonWithLed(unittest.TestCase):
    '''
    Verify TestButtonWithLed functionality
    '''

    clicks = 0

    def setUp(self):
        self.button = ButtonWithLed(self.callback)
        return

    def tearDown(self):
        self.button = None
        return

    def callback(self, button: Button) -> None:
        '''
        Button callback
        '''
        self.clicks += 1
        self.assertEqual(button, self.button)
        return

    def test_all(self):
        '''
        Test TestButtonWithLed functionality
        '''
        self.assertFalse(self.button.is_on())
        self.button.click()
        self.assertTrue(self.button.is_on())
        return


if __name__ == '__main__':
    unittest.main()
