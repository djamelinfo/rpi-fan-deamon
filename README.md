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

### Packages for Ubuntu, Raspberry pi OS, and the like
   ```sh
   sudo apt-get install git python3 python3-pip RPi.GPIO
   ```

### Steps
1. Get a copy of the repository:
	```sh
	git clone https://github.com/yourusername/rpi-fan-deamon.git /opt/rpi-fan-deamon
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

## Usage
The daemon will automatically start on boot and control the fan based on CPU temperature. You can check the status with:
```sh
sudo systemctl status fancontrol
```

## Configuration
Edit `fanControl.py` to change the GPIO pin, temperature threshold, or PID parameters as needed.

## License
MIT License

