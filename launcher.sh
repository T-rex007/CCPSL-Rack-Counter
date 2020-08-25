#!/bin/sh
#laucher.sh
# navigate to home directory, 
# then to this directory, then execute python script, then back home

cd /
cd /home/pi/workspace/CCPSL-Rack-Counter/
sudo python3 run_rack_counter.py
cd /