#Author: Landon Beckley
import pygame, sys
from spritesheet import SpriteSheet
from board import *
from display import *
import constants
import time
from random import *

class behavior:

    #Checks main menu clicks
    @staticmethod
    def clickMenu(display, clickX, clickY):
        inGame = True
        playBox = constants.playBox
        quitBox = constants.quitBox
        if(clickX <= playBox[1] and clickX >= playBox[0] and clickY <= playBox[3] and clickY >= playBox[2]):
            display.setInMenu(False)
            display.initializeGame()
        if(clickX <= quitBox[1] and clickX >= quitBox[0] and clickY <= quitBox[3] and clickY >= quitBox[2]):
            inGame = False
        return inGame

    #Reveal all adjacent empty tiles utilizing Depth-First Search Algorithm
    @staticmethod
    def revealAllEmpty(display, board, row, col):
        #Reveal current sprite
        display.getSpriteBoard()[row][col].setVisited(True)
        display.getSpriteBoard()[row][col].setRevealed(True)
        display.updateSprite(row,col, display.getSpriteBoard()[row][col].getTrueSprite())
        if(behavior.checkWin(display)):
            display.setInProgress(False)
            display.displayWin()
        if(display.getSpriteBoard()[row][col].getTrueSprite() == "Empty"):

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
                    if(not display.getSpriteBoard()[i][j].getVisited()):
                        #Recursive call 
                        behavior.revealAllEmpty(display, board, i, j)

    #Reveal all adjacent tiles if all mines found at that location
    @staticmethod
    def revealIfFound(display, board, row, col):
        foundAll = True
        if(display.getSpriteBoard()[row][col].getRevealed()):
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
            count = 0
            for i in range(rLowerBound, rUpperBound+1):
                for j in range(cLowerBound, cUpperBound+1):
                    if(display.getSpriteBoard()[i][j].getCurrSprite() == "Flag"):
                        count = count + 1
                    if(display.getSpriteBoard()[i][j].getCurrSprite() == "Flag" and display.getSpriteBoard()[i][j].getValue() == 0):
                        foundAll = False
                    if(display.getSpriteBoard()[i][j].getCurrSprite() != "Flag" and display.getSpriteBoard()[i][j].getValue() == 1):
                        foundAll = False
            if(foundAll):
                for i in range(rLowerBound, rUpperBound+1):
                    for j in range(cLowerBound, cUpperBound+1):
                        if(display.getSpriteBoard()[i][j].getCurrSprite() != "Flag"):
                            display.getSpriteBoard()[i][j].setRevealed(True)
                            display.updateSprite(i,j, display.getSpriteBoard()[i][j].getTrueSprite())
                            if(not display.getSpriteBoard()[i][j].getValue()):
                                behavior.revealAllEmpty(display, board,i,j)
            else:
                if(count == display.getSpriteBoard()[row][col].getAdjacentMines()):
                    display.setInProgress(False)
                    display.revealAllMines()
                    display.displayLose()

    #Gets mouse input data, returns a tuple of form (buttonType, xPos, yPos)
    @staticmethod
    def getMouseInput():
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

    #Process the users left click
    @staticmethod
    def click(display, clickX, clickY, board):
        if(display.inProgress):
            image = "Empty"
            xIndex = int(clickX/constants.xScale)
            yIndex = int(clickY/constants.yScale)
            if(not display.getSpriteBoard()[yIndex][xIndex].getCurrSprite() == "Flag"):
                if(not board.getGenerated()):
                    board.generate(xIndex,yIndex)
                    display.setTrueSprites(board)
                display.getSpriteBoard()[yIndex][xIndex].setRevealed(True)
                image = display.getSpriteBoard()[yIndex][xIndex].getTrueSprite()
                display.getSpriteBoard()[yIndex][xIndex].setCurrSprite(image)
                display.updateSprite(yIndex, xIndex, image)
                behavior.revealAllEmpty(display, board, yIndex, xIndex)
                if(display.getSpriteBoard()[yIndex][xIndex].getTrueSprite() == "Boom"):
                    display.setInProgress(False)
                    display.revealAllMines()
                    display.displayLose()
                if(behavior.checkWin(display)):
                    display.setInProgress(False)
                    display.displayWin()
                behavior.revealIfFound(display, board,yIndex,xIndex)
        else:
            display.displayMenu()

    #Process the users attempt to place a flag
    @staticmethod
    def flag(display, clickX, clickY, board):
        if(display.getInProgress):
            xIndex = int(clickX/constants.xScale)
            yIndex = int(clickY/constants.yScale)
            image = ""
            if(display.getSpriteBoard()[yIndex][xIndex].getCurrSprite() == "Flag"):
                image = "Covered"
                display.getSpriteBoard()[yIndex][xIndex].setCurrSprite(image)
                display.updateSprite(yIndex, xIndex, image)
                display.noOfFlags = display.noOfFlags - 1
            elif(display.getSpriteBoard()[yIndex][xIndex].getCurrSprite() == "Covered" and display.noOfFlags < constants.noOfMines):
                image = "Flag"
                display.getSpriteBoard()[yIndex][xIndex].setCurrSprite(image)
                display.updateSprite(yIndex, xIndex, image)
                display.noOfFlags = display.noOfFlags + 1
            if(behavior.checkWin(display)):
                    display.inProgress = False
                    display.displayWin()

    #Checks if all mines have been flagged
    @staticmethod
    def checkWin(display):
        won = True
        for i in range (constants.cols):
            for j in range (constants.rows):
                #Game is not won is there exists a non-mine tile that has not yet been revealed
                if(display.getSpriteBoard()[i][j].getTrueSprite() != "Boom" and not display.getSpriteBoard()[i][j].getRevealed()):
                    won = False
        return won