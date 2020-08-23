### Automatic live plant updates for CCPSL

This Repo contains the development code for a Live Plant Update system, developed for a brick factory during an intership at CCPSL(Caribbean clay Processing Services Ltd).


## Known Bugs
- The models confidence comes very close to to thresshold when workers are in the counting on the line (But still has low false positive rate)
- Half rack are counted 

## Known Limitations
- Camera once Set can't be moved or performance of the system may degrade.
- Region need to be manually added once at first.




## Testing 
Test case 1: No disturbace
<img src="img_girl.jpg" alt="Girl in a jacket" width="500" height="600">
All raacks were counted without Miscount

Test case 2: Maintainence on the Line 
<img src="ccpsl_test_snapshots/man1.png" alt="Maintainence on the line" width="500" height="600">
During the entire maintaience video the system miscounted once.

Test Case 3: Half Racks
<img src="ccpsl_test_snapshots/half_racks_counted.png" alt="Half Racks" width="500" height="600">
These racks were counted.

Test Case 4: A few bricks
<img src="ccpsl_test_snapshots/som1.png" alt="A few bricks" width="500" height="600">
This Rack was ignored by the system 

Test Case 5: Stationery Line (No Racks)
<img src="ccpsl_test_snapshots/Screenshot from 2020-08-23 15-31-23.png" alt="Stationery Line" width="500" height="600">

Test Case 6: Stationery Line (Racks)
<img src="ccpsl_test_snapshots/Screenshot from 2020-08-23 15-29-10.png" alt="Stationery Line" width="500" height="600">

Test Case 7: Bricks Missing 
Video: testing_clips/bricks_missing.mp4
<img src="ccpsl_test_snapshots/Bricks_missing.png" alt="Bricks Missing" width="500" height="600">





