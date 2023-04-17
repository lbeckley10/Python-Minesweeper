#Author: Landon Beckley
import pygame, sys
from spritesheet import SpriteSheet
from board import *
from display import *
import constants
import time
from random import *
from behavior import *

pygame.init()
pygame.display.init()

class game:
    def __init__(self):
        self.playing = True
    
    def playGame():
        inProgress = True
        gameBoard = Board()
        gameDisplay = Display()
        
        while(inProgress):
            mouseButton, clickX, clickY = behavior.getMouseInput()
            if(gameDisplay.getInMenu()):
                gameBoard.setGenerated(False)
                inProgress = behavior.clickMenu(gameDisplay, clickX, clickY)
            else:
                if(mouseButton == "LEFT"):
                    behavior.click(gameDisplay, clickX, clickY, gameBoard)
                if(mouseButton == "RIGHT"):
                    behavior.flag(gameDisplay, clickX, clickY, gameBoard)
        return inProgress
    
    if __name__ == '__main__':
        playing = True
        while(playing):
            playing = playGame()
        