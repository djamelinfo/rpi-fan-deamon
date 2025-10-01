import sys
import unittest
from unittest.mock import patch, MagicMock
# Mock RPi.GPIO if not running on a Pi
sys.modules['RPi'] = MagicMock()
sys.modules['RPi.GPIO'] = MagicMock()
from src.fanControl import FanController

class TestFanController(unittest.TestCase):
    def setUp(self):
        # Patch GPIO and PWM for all tests
        patcher_gpio = patch('src.fanControl.GPIO')
        self.mock_gpio = patcher_gpio.start()
        self.addCleanup(patcher_gpio.stop)
        self.mock_pwm = MagicMock()
        self.mock_gpio.PWM.return_value = self.mock_pwm
        # Create controller instance
        self.controller = FanController()

    @patch('src.fanControl.FanController.get_cpu_temperature')
    def test_handle_fan_high_temp(self, mock_temp):
        mock_temp.return_value = 60.0  # Simulate high temperature
        self.controller.handle_fan()
        self.mock_pwm.ChangeDutyCycle.assert_called()
        self.assertGreaterEqual(self.controller.fan_speed, 0)
        self.assertLessEqual(self.controller.fan_speed, 100)

    @patch('src.fanControl.FanController.get_cpu_temperature')
    def test_handle_fan_low_temp(self, mock_temp):
        mock_temp.return_value = 30.0  # Simulate low temperature
        self.controller.handle_fan()
        self.mock_pwm.ChangeDutyCycle.assert_called()
        self.assertEqual(self.controller.fan_speed, 0)

    def test_fan_off(self):
        self.controller.fan_off()
        self.mock_pwm.ChangeDutyCycle.assert_called_with(0)

if __name__ == '__main__':
    unittest.main()
