# Python-Minesweeper
This is a Minesweeper clone developed in Python using the Pygame library.

It utilizes Pygame's display functionality as well as object-oriented practices and data structures

The assets folder contains all sprites used, all created by Landon Beckley

behavior.py contains all static methods that deal with the behavior of the game. One to note in particular is the method revealAllEmpty(), which reveals all adjacent empty tiles when an empty one is clicked. This is of note because it utilizes an altered version of the famous Depth-First Search algorithm

board.py generates the backend 2d array that determines where the mines are located

constants.py contains constant values like display size, array size, and scaling data.

display.py contains all methods dealing with the game's display

main.py is where the main game loop occurs

tile.py contains methods for each individual tile object, as the display is actually a 2d array of these.

spritesheet.py is a spritesheet class found at https://www.pygame.org/wiki/Spritesheet
