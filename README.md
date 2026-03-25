# Tick Tock Boom

Tick Tock Boom is an electronic game that has a series of buttons, switches, and wires with an LCD screen and a row of LED lights to mimic a "bomb" that the players must quickly "defuse" using the included instruction manual.

## Start of the Game

When the game starts, it creates a randomized set of win conditions - the switches, buttons, wires, etc. that must be changed in order to "defuse the bomb". This set of conditions determines the color sequence that the LED lights flash, as well as printing a "serial number" on the LCD screen below the countdown timer, giving the players information they need to solve the puzzle.
* Normal Mode: Standard startup gives a timer of 5 minutes
* Expert Mode: Flipping the red switch before turning on will initiate Expert Mode - timer is reduced to 3 minutes.
* Novice Mode: Flipping the green switch before turning on will initiate Novice Mode - timer is increased to 7 minutes. Note: Game will ignore Novice mode if Expert mode is also intiated.
* Silent Mode: Flipping the white toggle before turning on will disable sound. 
* Debug Mode: Pressing all five buttons before turning on the power will initiate Debug mode:
	- Game will ask you to flip all switches and then it will report any that are reading as un-flipped still. Useful for diagnosing switches that are not properly grounding.
	- Screen will display additional information during play: the number of buttons, toggles, rockers, and wires that have been changed to their "correct" position, as well as a total count of how many have been switched from default, to assist in debugging connection issues. 
		- B0/5T0/5R0/4W0/4 N = Buttons 0/5 Correct, Toggles 0/5 Correct, Rockers 0/4 Correct, W 0/4 Correct, N switches changed from "default".
		
## Winning and Losing

If the timer runs out or the players flip 2+ incorrect switches, a losing sound effect is played, the LEDs turn red, and the screen displays a losing message along with the encoded solution to compare:
	- BXXXXX-TXXXXX-RXXXX-WXXXX displays the solution: B for buttons with the first letter of each correct button, followed by Toggles, Rockers, and Wires. Note that Black is encoded as 'K' since Blue is already using B. 
	- It also displays the serial number and the three flashing colors of the LEDs so you can compare the correct solution and serial number/LED sequence with the manual.
	
If the players figure out the correct solution, they are given a "Congratulations! Bomb Defused!" message and the LEDs all turn green. A winning jingle is played, and the remaining time is shown. 

## Building Your Own

You will need the following hardware:

* Raspberry Pi Pico
* Power Supply
* LCD Screen that supports I2C
* Five latching buttons in different colors (blue, green, red, white, and yellow)
* Five 'toggle' switches in different colors (blue, green, orange, red, and white)
* Four 'rocker' switches in different colors (blue, green, orange, and red)
* Four wires in different colors (black, blue, green, yellow), along with four speaker terminals to clip the ends into
* Soldering iron and wire to connect everything

1. Install MicroPython on the Raspberry Pi Pico.
2. Connect each of the buttons, toggles, rockers, etc. to the Pico's GPIO pins, making note of the pins used. Each of them uses a GPIO and common ground. Each GPIO is set as a "pull up" pin, and grounding it lets the game read the change in state. Wires are configured to be opposite: when connected they are treated as "default".  
3. Connect the LCD to the I2C pins and the LEDs to their respective pins, using resistors where necessary.
4. Edit the `variables.py` file with the GPIOs used for each connection if they differ from mine. 
5. Copy the contents of the "MicroPython" folder to the root of your Pico. 