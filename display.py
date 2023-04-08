#Author: Landon Beckley
import pygame, sys
import constants
from spritesheet import *
from board import *
from tile import *

#Class that deals with creating and updating the sprites displayed
class Display:

    #Initializes the display to show all "Covered" sprites
    def __init__(self):
        pygame.init()
        pygame.display.init()

        self.inProgress = True

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
        for i in range(16):
            for j in range(16):
                xCoord = 40*xCount
                yCoord = 40*yCount
                self.spriteBoard[i][j].assign(constants.spriteMap.get("Covered"), (xCoord, yCoord))
                self.gameDisplay.blit(self.spriteBoard[i][j].getImage(), (xCoord, yCoord))
                xCount += 1
                if(xCount > 15):
                    xCount = 0
                    yCount += 1
        pygame.display.flip()
    
    #Count the adjacent mines for each tile and assign it to trueSprite attribute utilizing Depth-First Search Algorithm
    def revealAllEmpty(self, board, row, col):
        #Reveal current sprite
        self.getSpriteBoard()[row][col].setVisited(True)
        self.getSpriteBoard()[row][col].setRevealed(True)
        self.updateSprite(row,col, self.getSpriteBoard()[row][col].getTrueSprite())
        if(self.getSpriteBoard()[row][col].getTrueSprite() == "Empty"):

            #Set bounds for adjacent tile search
            rLowerBound = row - 1
            rUpperBound = row + 1
            cLowerBound = col - 1
            cUpperBound = col + 1
            if(row == 0):
                rLowerBound = 0
            if(row == 15):
                rUpperBound = 15
            if(col == 0):
                cLowerBound = 0
            if(col == 15):
                cUpperBound = 15
            for i in range(rLowerBound, rUpperBound+1):
                for j in range(cLowerBound, cUpperBound+1):
                    if(not self.getSpriteBoard()[i][j].getVisited()):
                        #Recursive call 
                        self.revealAllEmpty(board, i, j)
    
    #Assign each tiles adjacentMines and trueSprite attributes
    def setTrueSprites(self, board):
        for i in range(16):
            for j in range(16):
                 self.spriteBoard[i][j].countAdjacentMines(board)

    def updateDisplay(self, x, y):
        self.gameDisplay.blit(self.spriteBoard[x][y].getImage(), self.spriteBoard[x][y].getCoords())
        pygame.display.flip()
    
    #Gets mouse input data, returns a tuple of form (buttonType, xPos, yPos)
    def getMouseInput(self):
        button = ""
        x = 0
        y = 0
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicks = pygame.mouse.get_pressed()
                if clicks[0]:
                    button = "LEFT"
                elif clicks[1]:
                    button = "MIDDLE"
                else:
                    button = "RIGHT"
                x,y = pygame.mouse.get_pos()
        
        return (button, x,y)
    
    #Updates the sprite at the given position
    def updateSprite(self, x, y, image):
        self.spriteBoard[x][y].setImage(constants.spriteMap.get(image))
        self.spriteBoard[x][y].setCurrSprite(image)
        self.updateDisplay(x,y)

     #Process the users left click
    def click(self, clickX, clickY, board):
        if(self.inProgress):
            image = "Empty"
            xIndex = int(clickX/40)
            yIndex = int(clickY/40)
            if(not self.getSpriteBoard()[yIndex][xIndex].getCurrSprite() == "Flag"):
                if(not board.getGenerated()):
                    board.generate(yIndex,xIndex)
                    self.setTrueSprites(board)
                self.getSpriteBoard()[yIndex][xIndex].setRevealed(True)
                image = self.getSpriteBoard()[yIndex][xIndex].getTrueSprite()
                self.getSpriteBoard()[yIndex][xIndex].setCurrSprite(image)
                self.updateSprite(yIndex, xIndex, image)
                self.revealAllEmpty(board, yIndex, xIndex)
                if(self.getSpriteBoard()[yIndex][xIndex].getTrueSprite() == "Boom"):
                    self.inProgress = False
                    self.displayLose()
                if(self.checkWin(board)):
                    self.inProgress = False
                    self.displayWin()
                
                
    
    #Process the users attempt to place a flag
    def flag(self, clickX, clickY, board):
        xIndex = int(clickX/40)
        yIndex = int(clickY/40)
        image = ""
        if(self.getSpriteBoard()[yIndex][xIndex].getCurrSprite() == "Flag"):
            image = "Covered"
            self.getSpriteBoard()[yIndex][xIndex].setCurrSprite(image)
            self.updateSprite(yIndex, xIndex, image)
            self.noOfFlags = self.noOfFlags - 1
        elif(self.getSpriteBoard()[yIndex][xIndex].getCurrSprite() == "Covered" and self.noOfFlags < constants.noOfMines):
            image = "Flag"
            self.getSpriteBoard()[yIndex][xIndex].setCurrSprite(image)
            self.updateSprite(yIndex, xIndex, image)
            self.noOfFlags = self.noOfFlags + 1
        if(self.checkWin(board)):
                self.inProgress = False
                self.displayWin()
        
        
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

    #Checks if all mines have been flagged
    def checkWin(self, board):
        won = True
        for i in range (16):
           for j in range (16):
                #Game is not won is there exists a non-mine tile that has not yet been revealed
                if(self.getSpriteBoard()[i][j].getTrueSprite() != "Boom" and not self.getSpriteBoard()[i][j].getRevealed()):
                    won = False
        return won

    #Getter function for spriteBoard attribute
    def getSpriteBoard(self):
        return self.spriteBoard
    
    #Setter function for spriteBoard attribute
    def setSpriteBoard(self, tile, x, y):
        self.spriteBoard[x][y] = tile    

    #Getter function for gameDisplay attribute
    def getGameDisplay(self):
        return self.gameDisplay 