#!/bin/sh
#laucher.sh
# navigate to home directory, 
# then to this directory, then execute python script, then back home
workon deepdive
cd /
cd /home/trex/workspace/liveplant_updates/rack_detector/
./run_rack_counter.py
cd /