# Wiring of the Raspberry Pi

A brief guide to wiring the Raspberry Pi 4 for Heads-Tails with instructions for replacing.

## Pinouts

### Raspberry Pi GPIO 40-pin header diagram:

GPIO 40-pin header numbering:
![](images/pinout.jpg)

## Wiring

### Wiring of the Raspberry Pi in Heads-Tails control board:

![](images/pi_wiring.jpg)

## Connections

```
GPIO HEADER PIN		COLOR	DESCRIPTION		DESTINATION
---------------		-----	-----------		-----------
1					RED		+3.3V			ShiftRegisterBoard 1, Voltage Shifter VIN PIN
2					RED		+5.0V			Fan +V
4					WHITE	+5.0V			ShiftRegisterBoard 1, + Terminal Block
6					BROWN	GND				ShiftRegisterBoard 1, - Terminal Block
9					BLACK	GND 			ShiftRegisterBoard 1, Voltage Shifter GND IN PIN
11					BLUE	STROBE			ShiftRegisterBoard 1, STROBE Terminal Block
13					GREEN	DATA			ShiftRegisterBoard 1, DATA Terminal Block
14					BLACK	GND 			Fan GND
15					YELLOW	CLOCK			ShiftRegisterBoard 1, CLOCK Terminal Block
16					WHITE	INTERRUPT		ShiftRegisterBoard 1, ZERO CROSSING Terminal Block
32					ORANGE	PWM				ShiftRegisterBoard 1, HEADLIGHT Terminal Block
```

## Replacing the Raspberry Pi 4

1. Power off the Raspberry Pi
1. Remove the power cable and any other cables or dongles attached to the other ports
1. Label the wires as above as you disconnect them
1. Remove the Micro SD Card
1. Remove the portion of the case covering the USB and ethernet ports
1. Remove the Raspberry Pi
1. Install the replacement Raspberry Pi
1. Replace the portion of the case covering the USB and ethernet ports 
1. Insert the SD card
1. Reconnect the wiring as labelled according to the chart above
1. Reconnect the power