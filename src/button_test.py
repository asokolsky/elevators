'''
Testing the button-related stuff
'''
import unittest
from typing import List

from .button import Button, ButtonWithLed, ButtonWithLedPanel # [relative-beyond-top-level]


class TestButton(unittest.TestCase):
    '''
    Verify Button functionality
    '''
    button_label = 'foo'
    clicks = 0

    def setUp(self):
        self.button = Button(self.button_label, self.callback)
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
        self.assertEqual(self.clicks,  clicks_old + 1)

        self.assertEqual(
            self.button.__repr__(),
            f"<Button '{self.button_label}' at {hex(id(self.button))}>")
        return


class TestButtonWithLed(unittest.TestCase):
    '''
    Verify ButtonWithLed functionality
    '''

    button_label = 'foo'
    clicks = 0

    def setUp(self):
        self.button = ButtonWithLed(self.button_label, self.callback)
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
        Test ButtonWithLed functionality
        '''
        self.assertFalse(self.button.is_on())
        self.assertEqual(
            self.button.__repr__(),
            f"<ButtonWithLed '{self.button_label}' at {hex(id(self.button))}>")

        self.button.click()
        self.assertTrue(self.button.is_on())
        self.assertEqual(
            self.button.__repr__(),
            f"<ButtonWithLed '*{self.button_label}*' at {hex(id(self.button))}>")
        return

class TestButtonWithLedPanel(unittest.TestCase):
    '''
    Verify ButtonWithLedPanel functionality
    '''
    labels =['1', '2', '3', '4', '5']

    def setUp(self):
        self.panel = ButtonWithLedPanel(
            self.labels, self.callback)
        return

    def tearDown(self):
        self.panel = None
        return

    def callback(self, panel: ButtonWithLedPanel, led_on: List[int]) -> None:
        '''
        callback
        '''
        self.assertEqual(panel, self.panel)
        return

    def test_all(self):
        '''
        Test ButtonWithLedPanel functionality
        '''
        self.assertEqual(self.panel.get_leds_on(), [])
        self.assertEqual(
            self.panel.get_annotated_labels(), self.labels)
        self.panel.click(2)
        self.assertEqual(self.panel.get_leds_on(), [2])
        self.assertEqual(
            self.panel.get_annotated_labels(),
            ['1', '2', '*3*', '4', '5'])
        self.panel.click(4)
        self.assertEqual(self.panel.get_leds_on(), [2, 4])
        self.assertEqual(
            self.panel.get_annotated_labels(),
            ['1', '2', '*3*', '4', '*5*'])
        self.panel.click(4)
        self.assertEqual(self.panel.get_leds_on(), [2])
        self.assertEqual(
            self.panel.get_annotated_labels(),
            ['1', '2', '*3*', '4', '5'])
        self.panel.click(2)
        self.assertEqual(self.panel.get_leds_on(), [])
        self.assertEqual(
            self.panel.get_annotated_labels(), self.labels)

        self.assertEqual(
            self.panel.__repr__(),
            f"<ButtonWithLedPanel {self.labels} at {hex(id(self.panel))}>")
        return


if __name__ == '__main__':
    unittest.main()
