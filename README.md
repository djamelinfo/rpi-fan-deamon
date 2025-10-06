# rpi-fan-deamon

[![GitHub release (latest by date)](https://img.shields.io/github/v/release/djamelinfo/rpi-fan-deamon)](https://github.com/djamelinfo/rpi-fan-deamon/releases)
[![View Changelog](https://img.shields.io/badge/changelog-view-blue)](CHANGELOG.md)
![GitHub top language](https://img.shields.io/github/languages/top/djamelinfo/rpi-fan-deamon)
![GitHub language count](https://img.shields.io/github/languages/count/djamelinfo/rpi-fan-deamon)
![GitHub repo size](https://img.shields.io/github/repo-size/djamelinfo/rpi-fan-deamon)


## Introduction
rpi-fan-deamon is a Python-based daemon for Raspberry Pi that automatically controls a cooling fan based on CPU temperature. It helps maintain optimal operating conditions and prolongs hardware lifespan by adjusting fan speed dynamically.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [License](#license)

## Features
- Automatic fan speed control based on CPU temperature
- PID control for smooth fan operation
- Runs as a background daemon using systemd
- Easy installation and setup
- Logging for monitoring and troubleshooting

## Installation

### Packages for Ubuntu, Raspberry pi OS, and the like
   ```sh
   sudo apt-get install git python3 python3-pip RPi.GPIO
   ```

### Steps
1. Get a copy of the repository:
	```sh
	git clone https://gitea.yagoubi.work/djamel/rpi-fan-deamon.git /opt/rpi-fan-deamon
	```
2. move into your new local repository:
	```sh
	cd /opt/rpi-fan-deamon
	```
3. Move to the latest official release::
	```sh
	sudo git checkout v1.0.0 # (you want to replace v1.8.5 with the latest if this isn't)
	```
4. Enable and start the systemd service:
	```sh
	sudo ln -s /opt/rpi-fan-deamon/systemd/fancontrol.service /etc/systemd/system/fancontrol.service
	
    sudo systemctl daemon-reload
    
    # tell system that it can start our script at system startup during boot
	sudo systemctl enable fancontrol.service
    
    # start the script running
	sudo systemctl start fancontrol.service
	```


## How It Works

This project is inspired by the approach described in [Variable Speed Cooling Fan for Raspberry Pi Using PWM](https://www.sensorsiot.org/variable-speed-cooling-fan-for-raspberry-pi-using-pwm-video138/). The script uses PWM (Pulse Width Modulation) to control the speed of a connected fan, allowing for variable cooling based on the CPU temperature.

- **PWM Control:** The Raspberry Pi’s GPIO pin outputs a PWM signal to the fan, adjusting its speed smoothly rather than just turning it on or off.
- **Temperature Monitoring:** The script reads the CPU temperature using the `vcgencmd measure_temp` command.
- **PID Logic:** The fan speed is calculated using a simple PID (Proportional-Integral-Derivative) algorithm, which helps maintain a stable temperature and prevents rapid fan speed changes.
- **Automatic Operation:** When the CPU temperature exceeds a set threshold, the fan speed increases. As the temperature drops, the fan slows down or turns off, reducing noise and power consumption.
- **Systemd Integration:** The script runs as a background service, ensuring the fan control starts automatically on boot and runs reliably.

### Hardware Setup

- Connect a 5V PWM-capable fan to the Raspberry Pi’s GPIO pin (default is GPIO 17).
- Make sure the fan’s ground and power are connected appropriately.
- No additional hardware is required if your fan supports PWM directly; otherwise, you may need a transistor or MOSFET to drive the fan.

## Usage
The daemon will automatically start on boot and control the fan based on CPU temperature. You can check the status with:
```sh
sudo systemctl status fancontrol
```

## Configuration
Edit `fanControl.py` to change the GPIO pin, temperature threshold, or PID parameters as needed.

## License
MIT License

