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

    #Checks main menu clicks
    def clickMenu(self, clickX, clickY):
        inGame = True
        playBox = constants.playBox
        quitBox = constants.quitBox
        if(clickX <= playBox[1] and clickX >= playBox[0] and clickY <= playBox[3] and clickY >= playBox[2]):
            self.inMenu = False
            self.initializeGame()
        if(clickX <= quitBox[1] and clickX >= quitBox[0] and clickY <= quitBox[3] and clickY >= quitBox[2]):
            inGame = False
        return inGame
    
    #Initializes the display to show all "Covered" sprites
    def initializeGame(self):
        pygame.init()
        pygame.display.init()
        self.gameDisplay.fill((255,255,255))
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
    
    #Reveal all adjacent empty tiles utilizing Depth-First Search Algorithm
    def revealAllEmpty(self, board, row, col):
        #Reveal current sprite
        self.getSpriteBoard()[row][col].setVisited(True)
        self.getSpriteBoard()[row][col].setRevealed(True)
        self.updateSprite(row,col, self.getSpriteBoard()[row][col].getTrueSprite())
        if(self.checkWin(board)):
            self.inProgress = False
            self.displayWin()
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

    #Reveal all adjacent tiles if all mines found at that location
    def revealIfFound(self, board, row, col):
        foundAll = True
        if(self.getSpriteBoard()[row][col].getRevealed()):
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
                    if(self.getSpriteBoard()[i][j].getCurrSprite() == "Flag" and self.getSpriteBoard()[i][j].getValue() == 0):
                        foundAll = False
                    if(self.getSpriteBoard()[i][j].getCurrSprite() != "Flag" and self.getSpriteBoard()[i][j].getValue() == 1):
                        foundAll = False
            if(foundAll):
                for i in range(rLowerBound, rUpperBound+1):
                    for j in range(cLowerBound, cUpperBound+1):
                        if(self.getSpriteBoard()[i][j].getCurrSprite() != "Flag"):
                            self.getSpriteBoard()[i][j].setRevealed(True)
                            self.updateSprite(i,j, self.getSpriteBoard()[i][j].getTrueSprite())
                            if(not self.getSpriteBoard()[i][j].getValue()):
                                self.revealAllEmpty(board,i,j)
    
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
                    board.generate(xIndex,yIndex)
                    self.setTrueSprites(board)
                self.getSpriteBoard()[yIndex][xIndex].setRevealed(True)
                image = self.getSpriteBoard()[yIndex][xIndex].getTrueSprite()
                self.getSpriteBoard()[yIndex][xIndex].setCurrSprite(image)
                self.updateSprite(yIndex, xIndex, image)
                self.revealAllEmpty(board, yIndex, xIndex)
                if(self.getSpriteBoard()[yIndex][xIndex].getTrueSprite() == "Boom"):
                    self.inProgress = False
                    self.revealAllMines()
                    self.displayLose()
                if(self.checkWin(board)):
                    self.inProgress = False
                    self.displayWin()
                self.revealIfFound(board,yIndex,xIndex)
        else:
            self.displayMenu()

                
                
    
    #Process the users attempt to place a flag
    def flag(self, clickX, clickY, board):
        if(self.inProgress):
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
    
    #Getter function for inMenu attribute
    def getInMenu(self):
        return self.inMenu
    #Setter function for inMenu attribute
    def setSpriteBoard(self, tile, x, y):
        self.spriteBoard[x][y] = tile  

    #Getter function for gameDisplay attribute
    def getGameDisplay(self):
        return self.gameDisplay 