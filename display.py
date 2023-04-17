#Author: Landon Beckley
import pygame, sys
import constants
from spritesheet import *
from board import *
from tile import *

#Class that deals with creating and updating the sprites displayed
class Display:
    
    def __init__(self):
        self.inProgress = True
        self.noOfFlags = 0
        self.spriteBoard = 0
        self.inMenu = True
        pygame.init()
        pygame.display.init()
        self.gameDisplay = pygame.display.set_mode(constants.size)
        pygame.display.set_caption("Minesweeper")
        self.displayMenu()
        
    #Displays the main menu
    def displayMenu(self):
        pygame.init()
        pygame.display.init()
        self.inProgress = True
        self.inMenu = True
        self.gameDisplay.fill((255,255,255))
        bg = SpriteSheet('assets/background.png').image_at((0,0,4,4))
        bg = pygame.transform.scale(bg, (640, 640))
        title = SpriteSheet('assets/Title.png').image_at((0,0,81,19))
        title = pygame.transform.scale(title, (324, 76))
        play = SpriteSheet('assets/Play.png').image_at((0,0,23,11))
        play = pygame.transform.scale(play, (92, 44))
        quit = SpriteSheet('assets/Quit.png').image_at((0,0,23,11))
        quit = pygame.transform.scale(quit, (92, 44))
        self.gameDisplay.blit(bg, (0,0))
        self.gameDisplay.blit(title, (158,122))
        self.gameDisplay.blit(play, (274,218))
        self.gameDisplay.blit(quit, (274,282))    
        pygame.display.flip()
    
    #Initializes the display to show all "Covered" sprites
    def initializeGame(self):
        pygame.init()
        pygame.display.init()
        self.gameDisplay.fill((255,255,255))
        self.inProgress = True
        self.inMenu = False
        self.noOfFlags = 0
        
        #Intialize window
        self.gameDisplay = pygame.display.set_mode(constants.size)
        pygame.display.set_caption("Minesweeper")
        
        #spriteBoard contains integers corresponding with sprites in the spritesheet
        xCount = 0
        yCount = 0

        #Initialize spriteBoard to contain initial tile objects
        self.spriteBoard = [[Tile() for i in range(constants.cols)] for j in range(constants.rows)]
        
        #loop to assign values to tile objects and display them appropriately
        for i in range(constants.cols):
            for j in range(constants.rows):
                xCoord = constants.xScale*xCount
                yCoord = constants.yScale*yCount
                self.spriteBoard[i][j].assign(constants.spriteMap.get("Covered"), (xCoord, yCoord))
                self.gameDisplay.blit(self.spriteBoard[i][j].getImage(), (xCoord, yCoord))
                xCount += 1
                if(xCount > 15):
                    xCount = 0
                    yCount += 1
        pygame.display.flip()
    
    #Assign each tiles adjacentMines and trueSprite attributes
    def setTrueSprites(self, board):
        for i in range(constants.cols):
            for j in range(constants.rows):
                 self.spriteBoard[i][j].countAdjacentMines(board)

    def updateDisplay(self, x, y):
        self.gameDisplay.blit(self.spriteBoard[x][y].getImage(), self.spriteBoard[x][y].getCoords())
        pygame.display.flip()
    
    #Updates the sprite at the given position
    def updateSprite(self, x, y, image):
        self.spriteBoard[x][y].setImage(constants.spriteMap.get(image))
        self.spriteBoard[x][y].setCurrSprite(image)
        self.updateDisplay(x,y)         
    
    #Reveal location of all mines if lost
    def revealAllMines(self):
        for i in range (constants.cols):
            for j in range (constants.rows):
                if(self.getSpriteBoard()[i][j].getValue() and self.getSpriteBoard()[i][j].getCurrSprite() != "Boom"):
                    self.getSpriteBoard()[i][j].setCurrSprite("Mine")
                    self.updateSprite(i, j, self.getSpriteBoard()[i][j].getCurrSprite())
                if(not self.getSpriteBoard()[i][j].getValue() and self.getSpriteBoard()[i][j].getCurrSprite() == "Flag"):
                    self.getSpriteBoard()[i][j].setCurrSprite("Incorrect")
                    self.updateSprite(i, j, self.getSpriteBoard()[i][j].getCurrSprite())

    #Displays the Lose Sprite
    def displayLose(self):
        image = SpriteSheet('assets/lose.png').image_at(constants.gameOverSquare)
        image = pygame.transform.scale(image, (230,200))
        self.gameDisplay.blit(image, (200,200))
        pygame.display.flip()

    #Displays the Win Sprite
    def displayWin(self):
        image = SpriteSheet('assets/win.png').image_at(constants.gameOverSquare)
        image = pygame.transform.scale(image, (230,200))
        self.gameDisplay.blit(image, (200,200))
        pygame.display.flip()

    #Getter function for spriteBoard attribute
    def getSpriteBoard(self):
        return self.spriteBoard
    
    #Setter function for inMenu attribute
    def setInMenu(self, inMenu):
        self.inMenu = inMenu
    
    #Getter function for inMenu attribute
    def getInMenu(self):
        return self.inMenu
    
    #Setter function for inProgress attribute
    def setInProgress(self, inProgress):
        self.inProgress = inProgress
    
    #Getter function for inProgress attribute
    def getInProgress(self):
        return self.inProgress
    
    #Setter function for inMenu attribute
    def setSpriteBoard(self, tile, x, y):
        self.spriteBoard[x][y] = tile  

    #Getter function for gameDisplay attribute
    def getGameDisplay(self):
        return self.gameDisplay 