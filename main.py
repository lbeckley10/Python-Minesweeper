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
    def __init__(self):
        self.playing = True
    
    def playGame():
        inProgress = True
        gameBoard = Board()
        gameDisplay = Display()
        
        while(inProgress):
            mouseButton, clickX, clickY = gameDisplay.getMouseInput()
            if(gameDisplay.getInMenu()):
                gameBoard.setGenerated(False)
                inProgress = gameDisplay.clickMenu(clickX, clickY)
            else:
                if(mouseButton == "LEFT"):
                    gameDisplay.click(clickX, clickY, gameBoard)
                if(mouseButton == "RIGHT"):
                    gameDisplay.flag(clickX, clickY, gameBoard)
        return inProgress
    
    if __name__ == '__main__':
        playing = True
        while(playing):
            playing = playGame()
        