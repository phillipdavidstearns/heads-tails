# TO DOs

1. Secure Raspberry Pi 4 Case
1. Replace Micro SD Card In Raspberry Pi 4
1. Visual Check of the Wiring
1. Electrical Check of the Wiring
1. Power Raspberry Pi and Observe LED indicators


## Securing the Raspberry Pi 4 Case

When assembled, the case for the Raspberry Pi 4 was secured to the board using self tapping wood screws. It seems like these may have been removed. In order to secure the case using screws, it will be necessary to remove the Raspberry Pi 4 from the case. 

1. Detach from power.
1. During the process, it may be necessary to disconnect jumper wires. Please note their color and location on either end.
1. Remove case parts in order to gain access to the Raspberry Pi, but do not fully remove it from the case.
1. Remove the sd card and store in a static free location where it will not be bent or crushed by accident.
1. Remove the Raspberry Pi 4 from the case.
1. Use self-tapping wood screws to secure the base of the case to the board.
1. Replace the Raspberry Pi 4
1. Replace the SD card (with new one if available)
1. Attach any additional case parts except for the cover
1. Reconnect any wires that may have been removed
1. Reconnect Power

## Replacing SD Card

This swap is pretty straight forward.

1. Remove the old card
2. Replace with new card
3. Insert old card in the SD adapter and return to Phil

## Visual/Physical inspection of the Wiring

Given the behavior of the code checks out fine, it's likely that the issue is a loose connection somewhere between the Raspberry Pi and the LED driver boards, likely between the Pi and the first shift register board.

1. Completely disconnect all power.
1. Check +5V and Ground connections between the Pi and the shift register board. If inserted into a screw terminal, give them a gentle tug to make sure they're secured.
1. Check the Data, Clock, and Strobe wires. Same story with the screw terminals. Use a precision screw driver and/or pliers if necessary to isolate and check each connection individually.

Note: Signals connect to the shift register board via male header pins into a 3.3v to 5v voltage level shifter. The Data, Clock and Strobe lines are daisy chained and presented at terminal blocks indicated in the images below by points 3.1, 3.2, and 3.3:

![](images/2_2_bus_connections.png)

## Electrical testing

The previous step should have either located and corrected the issue. Just to confirm, run continuity checks in a point to point fashion.

1. Check +5V from Pi to the first shift register board and then between terminals on the board (just in case), to the next board and so on.
1. Perform the same check as above for the Ground, Data, Clock and Strobe lines, but only between boards.

If everything checks out, move on.

## Power up and observe indicators

At this point, go ahead and give me a call and I'll be able to help run some scripts remotely and otherwise trouble shoot.

1. Connect power and wait.
1. After about 3 minutes, the routine should start running and you should be able to see the red indicator lights on the LED driver boards lighting up.
1. If so, then our work here is done, if not, we got more sleuthing to do.