
"""
Raspberry Pi Fan Control Daemon
Controls a cooling fan based on CPU temperature using PID logic.
"""
# Author: Djamel Edine
import os
import time
import logging
import sys
from RPi import GPIO

# pylint: disable=no-member
class FanController:
    """Controls a Raspberry Pi fan using PID logic."""
    def __init__(self, fan_pin=17, desired_temp=45, p_temp=15, i_temp=0.4, pwm_freq=50):
        """
        Initialize the FanController.
        Args:
            fan_pin (int): GPIO pin for the fan.
            desired_temp (float): Temperature threshold in Celsius.
            p_temp (float): PID proportional constant.
            i_temp (float): PID integral constant.
            pwm_freq (int): PWM frequency.
        """
        self.fan_pin = fan_pin
        self.desired_temp = desired_temp
        self.p_temp = p_temp
        self.i_temp = i_temp
        self.sum = 0
        self.fan_speed = 0
        self.pwm_freq = pwm_freq
        self.my_pwm = None
        self.setup_gpio()

    def setup_gpio(self):
        """Set up GPIO and PWM for fan control."""
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.fan_pin, GPIO.OUT)
        self.my_pwm = GPIO.PWM(self.fan_pin, self.pwm_freq)
        self.my_pwm.start(0)
        self.fan_off()

    def get_cpu_temperature(self):
        """Get the current CPU temperature in Celsius."""
        try:
            res = os.popen('vcgencmd measure_temp').readline()
            temp = res.replace("temp=","").replace("'C\n","")
            return float(temp)
        except (ValueError, OSError) as err:
            logging.error("Error reading CPU temperature: %s", err)
            return 0.0

    def fan_off(self):
        """Turn the fan off."""
        self.my_pwm.ChangeDutyCycle(0)

    def handle_fan(self):
        """Calculate and set fan speed based on CPU temperature."""
        actual_temp = self.get_cpu_temperature()
        diff = actual_temp - self.desired_temp
        self.sum += diff
        p_diff = diff * self.p_temp
        i_diff = self.sum * self.i_temp
        self.fan_speed = p_diff + i_diff
        self.fan_speed = min(max(self.fan_speed, 0), 100)
        if self.fan_speed < 15:
            self.fan_speed = 0
        self.sum = min(self.sum, 100)
        self.sum = max(self.sum, -100)
        logging.info("Temp: %.2fC, FanSpeed: %.2f%%", actual_temp, self.fan_speed)
        self.my_pwm.ChangeDutyCycle(self.fan_speed)

    def run(self, interval=1):
        """Run the fan control loop."""
        logging.info("FanController started.")
        try:
            while True:
                self.handle_fan()
                time.sleep(interval)
        except KeyboardInterrupt:
            logging.info("FanController stopped by user.")
        except Exception as err:
            logging.error("Unexpected error: %s", err)
        finally:
            self.fan_off()
            GPIO.cleanup()
            logging.info("GPIO cleaned up.")

def main():
    """Main entry point for the fan control daemon."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s: %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    controller = FanController()
    controller.run()

if __name__ == "__main__":
    main()
