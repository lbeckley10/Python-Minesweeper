#Author: Landon Beckley
import pygame, sys
from spritesheet import SpriteSheet
from board import *
from display import *
import constants
import time
from random import *

pygame.init()
pygame.display.init()

class game:  
    def playGame():
        inProgress = True
        gameBoard = Board()
        gameDisplay = Display()
        
        while(inProgress):
            mouseButton, clickX, clickY = gameDisplay.getMouseInput()
            if(mouseButton == "LEFT"):
                gameDisplay.click(clickX, clickY, gameBoard)
            if(mouseButton == "RIGHT"):
                gameDisplay.flag(clickX, clickY, gameBoard)
    
    if __name__ == '__main__':
        playing = True
        while(playing):
            playGame()
        