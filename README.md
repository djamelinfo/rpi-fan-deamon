# rpi-fan-deamon

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

### Prerequisites
- Raspberry Pi with Raspbian OS
- Python 3
- `RPi.GPIO` library

### Steps
1. Clone or copy the repository to your Raspberry Pi:
	```sh
	git clone https://github.com/yourusername/rpi-fan-deamon.git
	```
2. Install required Python packages:
	```sh
	pip3 install RPi.GPIO
	```
3. Copy the files to `/opt/rpi-fan-deamon` (or your preferred directory):
	```sh
	sudo mkdir -p /opt/rpi-fan-deamon
	sudo cp fanControl.py /opt/rpi-fan-deamon/
	sudo cp fancontrol.service /etc/systemd/system/
	```
4. Enable and start the systemd service:
	```sh
	sudo systemctl daemon-reload
	sudo systemctl enable fancontrol
	sudo systemctl start fancontrol
	```

## Usage
The daemon will automatically start on boot and control the fan based on CPU temperature. You can check the status with:
```sh
sudo systemctl status fancontrol
```

## Configuration
Edit `fanControl.py` to change the GPIO pin, temperature threshold, or PID parameters as needed.

## License
MIT License

