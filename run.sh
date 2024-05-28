#!/bin/bash

# Start the pigpio daemon and Wait to ensure pigpiod starts
sudo pigpiod
sleep 1

# Start the system
python src/main.py
