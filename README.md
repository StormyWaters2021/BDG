# Tick Tock Boom

Tick Tock Boom is an electronic game that has a series of buttons, switches, and wires with an LCD screen and a row of LED lights to mimic a "bomb" that the players must quickly "defuse" using the included instruction manual. 
## Start of the Game

When the game starts, it creates a randomized set of win conditions - the switches, buttons, wires, etc. that must be changed in order to "defuse the bomb". This set of conditions determines the color sequence that the LED lights flash, as well as printing a "serial number" on the LCD screen below the countdown timer, giving the players information they need to solve the puzzle. 
## Winning and Losing

The countdown timer provides 5 minutes before the players fail the game. If the players flip 2 incorrect buttons, switches, etc. they also fail. The screen changes to a "BOOM" message and the LEDs turn solid red. 

If the players figure out the correct solution, they are given a "Congratulations! Bomb Defused!" message and the LEDs all turn green.
## Building Your Own

You will need the following hardware:

- Raspberry Pi Pico
- Power Supply
- LCD Screen that supports I2C
- Five switching buttons in different colors (blue, green, red, white, and yellow)
- Five 'toggle' switches in different colors (blue, green, orange, red, and white)
- Four 'rocker' switches in different colors (blue, green, orange, and red)
- Four wires in different colors (black, blue, green, red), along with four speaker terminals to clip the ends into
- 
