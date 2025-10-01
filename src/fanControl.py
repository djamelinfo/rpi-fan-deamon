
#!/usr/bin/env python3
# Author: Djamel Edine
import os
import time
import logging
import sys
import RPi.GPIO as GPIO

class FanController:
    def __init__(self, fan_pin=17, desired_temp=45, p_temp=15, i_temp=0.4, pwm_freq=50):
        self.fan_pin = fan_pin
        self.desired_temp = desired_temp
        self.p_temp = p_temp
        self.i_temp = i_temp
        self.sum = 0
        self.fan_speed = 0
        self.pwm_freq = pwm_freq
        self.myPWM = None
        self.setup_gpio()

    def setup_gpio(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.fan_pin, GPIO.OUT)
        self.myPWM = GPIO.PWM(self.fan_pin, self.pwm_freq)
        self.myPWM.start(0)
        self.fan_off()

    def get_cpu_temperature(self):
        try:
            res = os.popen('vcgencmd measure_temp').readline()
            temp = res.replace("temp=","").replace("'C\n","")
            return float(temp)
        except Exception as e:
            logging.error(f"Error reading CPU temperature: {e}")
            return 0.0

    def fan_off(self):
        self.myPWM.ChangeDutyCycle(0)

    def handle_fan(self):
        actual_temp = self.get_cpu_temperature()
        diff = actual_temp - self.desired_temp
        self.sum += diff
        p_diff = diff * self.p_temp
        i_diff = self.sum * self.i_temp
        self.fan_speed = p_diff + i_diff
        if self.fan_speed > 100:
            self.fan_speed = 100
        if self.fan_speed < 15:
            self.fan_speed = 0
        if self.sum > 100:
            self.sum = 100
        if self.sum < -100:
            self.sum = -100
        logging.info(f"Temp: {actual_temp:.2f}C, FanSpeed: {self.fan_speed:.2f}%")
        self.myPWM.ChangeDutyCycle(self.fan_speed)

    def run(self, interval=1):
        logging.info("FanController started.")
        try:
            while True:
                self.handle_fan()
                time.sleep(interval)
        except KeyboardInterrupt:
            logging.info("FanController stopped by user.")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
        finally:
            self.fan_off()
            GPIO.cleanup()
            logging.info("GPIO cleaned up.")

def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s: %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    controller = FanController()
    controller.run()

if __name__ == "__main__":
    main()
