#Author: Landon Beckley
import pygame, sys
from spritesheet import SpriteSheet

#Tile object for each individual tile on the board
class Tile:
    
    #Initializes the tile with initial values for all attributes
    def __init__(self):
        pygame.init()
        self.image = None
        self.coords = (0,0)
        self.currSprite = "Covered"
        self.trueSprite = "Empty"
        self.adjacentMines = 0
        self.visited = False
        self.revealed = False
    
    #Assign method to give attributes values (necessary because this occurs in a 2D array)
    def assign(self, square, coords):
        pygame.init()
        sprites = SpriteSheet('assets/minesweeper_spritesheet.png')
        im = sprites.image_at(square)
        self.image = pygame.transform.scale(im, (40,40))
        self.coords = coords

    #Count the adjacent mines for each tile and assign it to trueSprite attribute
    def countAdjacentMines(self, board):
        row = int(self.coords[0]/40)
        col = int(self.coords[1]/40)
        count = 0
        if(board.getGameBoard()[row][col] == 0):
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
                    if(board.getGameBoard()[i][j] == 1):
                        count = count + 1
            if(count != 0):
                self.trueSprite = str(count)
        else:
            self.trueSprite = "Boom"

    

    #returns image attribute
    def getImage(self):
        return self.image
    
    #Sets new image value
    def setImage(self, square):
        pygame.init()
        sprites = SpriteSheet('assets/minesweeper_spritesheet.png')
        im = sprites.image_at(square)
        self.image = pygame.transform.scale(im, (40,40))

    #returns coords attribute
    def getCoords(self):
        return self.coords
    
    #Sets new coords value
    def setCoords(self, coords):
        self.coords = coords
    
    #Function to return the value of currSprite attribute
    def getCurrSprite(self):
        return self.currSprite

    #Function to set the currSprite attribute
    def setCurrSprite(self, newSprite):
        self.currSprite = newSprite
    
    #Function to return the trueSprite attribute
    def  getTrueSprite(self):
        return self.trueSprite
    
    #Function to set the visited attribute
    def setVisited(self, visited):
        self.visited = visited
    
    #Function to return the visited attribute
    def  getVisited(self):
        return self.visited
    
    #Function to set the revealed attribute
    def setRevealed(self, revealed):
        self.revealed = revealed
    
    #Function to return the revealed attribute
    def  getRevealed(self):
        return self.revealed
