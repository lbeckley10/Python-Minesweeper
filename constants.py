#Author: Landon Beckley
#File containing all needed global constants

#Number of rows and columns for the game board matrices
rows, cols = (16,16)

#Size of display window
size = [640,640]

#Number of mines
noOfMines = 40

#Rectangle for game over sprite
gameOverSquare = (0,0,22,19)

#Hitbox for play button
playBox = (274, 366, 218, 262)

#Hitbox for quit button
quitBox = (274, 366, 282, 326)

#Maps the different sprite names to their rectangle locations in the spritesheet
spriteMap = {
    "1":(0,0,16,16), "2":(17,0,16,16), "3":(34,0,16,16), "4":(51,0,16,16), "5":(68,0,16,16),
    "6":(0,17,16,16), "7":(17,17,16,16), "8":(34,17,16,16), "Empty":(51,17,16,16), "Covered":(68,17,16,16),
    "Mine":(0,34,16,16), "Incorrect":(17,34,16,16), "Boom":(34,34,16,16), "Flag":(51,34,16,16)
}