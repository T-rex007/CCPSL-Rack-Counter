#!/bin/sh
#laucher.sh
# navigate to home directory, 
# then to this directory, then execute python script, then back home

cd /
cd /home/trex/workspace/liveplant_updates/rack_detector/
sudo python3 run_rack_counter.py
cd /