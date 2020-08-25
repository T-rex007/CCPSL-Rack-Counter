### Automatic live plant updates for CCPSL

This Repo contains the development code for a Live Plant Update system, developed for a brick factory during an internship at CCPSL(Caribbean clay Processing Services Ltd).

### How it works?

### Setup

## Software

## Hardware

### Discussion
<br/>

## Known Bugs
- The model's confidence came very close to the thresshold value when workers are in the region the system looks at to count the racks the line (But still has low false positive rate)
- Racks that were half filled are also counted 

## Known Limitations
- Camera once Set can't be moved or performance of the system may degrade.
- Region need to be manually added once at first.
- System doesn't say how much bricks are on each rack i.e. whether its half of a rack of an entire rack


## Testing 
Test case 1: No disturbace
<br/>
<img src="ccpsl_test_snapshots/Screenshot from 2020-08-23 15-29-10.png" alt="Girl in a jacket" width="500" height="600">
All raacks were counted without Miscount
<br/>

Test case 2: Maintainence on the Line 
<br/>
<img src="ccpsl_test_snapshots/man1.png" alt="Maintainence on the line" width="500" height="600">
<br/>
During the entire maintaience video the system miscounted once.
<br/>

Test Case 3: Half Racks
<br/>
<img src="ccpsl_test_snapshots/half_racks_counted.png" alt="Half Racks" width="500" height="600">
<br/>
These racks were counted.
<br/>

Test Case 4: A few bricks
<br/>
<img src="ccpsl_test_snapshots/som1.png" alt="A few bricks" width="500" height="600">
<br/>
This Rack was ignored by the system 
<br/>

Test Case 5: Stationery Line (No Racks)
<br/>
<img src="ccpsl_test_snapshots/Screenshot from 2020-08-23 15-31-23.png" alt="Stationery Line" width="500" height="600">
<br/>

Test Case 6: Stationery Line (Racks)
<br/>
<img src="ccpsl_test_snapshots/Screenshot from 2020-08-23 15-29-10.png" alt="Stationery Line" width="500" height="600">
<br/>

Test Case 7: Bricks Missing 
Video: testing_clips/bricks_missing.mp4
<br/>
<img src="ccpsl_test_snapshots/Bricks_missing.png" alt="Bricks Missing" width="500" height="600">
<br/>
Rack was counted even though bricks were missing from the Rack




