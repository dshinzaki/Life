# Dylan Shinzaki
# 9/10/13
# Basic interface to play Conway's Game of Life 
# Based upon neighborLife implementation of life
# Execution:
# python interfaceLife.py

import pygame, sys, os
import time
from pygame.locals import * 
from neighborLife import NeighborLife

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
SQUARE_SIZE = 10
WINDOW_SIZE = 500
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 30
LINE_WEIGHT = 1
GAP = 10
FONT_SIZE = 15
GRID_SIZE = int(WINDOW_SIZE / SQUARE_SIZE)

RESET_BUTTON = ((WINDOW_SIZE + GAP, GAP), (BUTTON_WIDTH-2*GAP, \
    BUTTON_HEIGHT))
ANIMATE_BUTTON = ((WINDOW_SIZE + GAP, BUTTON_HEIGHT + 2*GAP), \
    (BUTTON_WIDTH-2*GAP, BUTTON_HEIGHT))
NEXT_BUTTON = ((WINDOW_SIZE + GAP, 2*BUTTON_HEIGHT + 3*GAP), \
    (BUTTON_WIDTH-2*GAP, BUTTON_HEIGHT))
RESET_TEXT = "RESET"
ANIMATE_TEXT = "ANIMATE"
NEXT_TEXT = "NEXT"

GLIDER_BUTTON = ((WINDOW_SIZE + GAP, 3*BUTTON_HEIGHT + 4*GAP), \
    (BUTTON_WIDTH-2*GAP, BUTTON_HEIGHT))
PENTADECATHALON_BUTTON = ((WINDOW_SIZE + GAP, 4*BUTTON_HEIGHT + 5*GAP),\
    (BUTTON_WIDTH-2*GAP, BUTTON_HEIGHT))
BLINKER_BUTTON = ((WINDOW_SIZE + GAP, 5*BUTTON_HEIGHT + 6*GAP), \
    (BUTTON_WIDTH-2*GAP, BUTTON_HEIGHT))
GLIDER_TEXT = "GLIDER"
PENTADECATHALON_TEXT = "PENTA..."
BLINKER_TEXT = "BLINKER"

# creates button at given set of coordinates with a given size
# sets button to be red if the state is true
def renderButton(coordinates, text, state):
    if state:
        rect = pygame.draw.rect(screen, RED, coordinates)
    else:
        rect = pygame.draw.rect(screen, WHITE, coordinates)
    rect = pygame.draw.rect(screen, BLACK, coordinates, LINE_WEIGHT)
    font = pygame.font.Font(None, FONT_SIZE )
    text = font.render(text, LINE_WEIGHT , BLACK)
    
    textpos = text.get_rect()
    textpos.centerx = rect.centerx
    textpos.centery = rect.centery 
    screen.blit(text, textpos)

# creates button at given set of coordinates with a given size
# makes cell darkened if state is true 
def setCell(i, j, state):
    coordinates = ((i*SQUARE_SIZE,j*SQUARE_SIZE), \
        (SQUARE_SIZE, SQUARE_SIZE))
    if not state:
        pygame.draw.rect(screen, WHITE, coordinates)
        pygame.draw.rect(screen, BLACK, coordinates, LINE_WEIGHT)
    else:
        pygame.draw.rect(screen, BLACK, coordinates)

# Returns true if the pixel positions (i, j) are in the
# rectangle given by coordinates
def intersectsWith(i, j, coordinates):
    coord, size = coordinates
    if i < coord[0]:
        return False
    if i > coord[0] + size[0]:
        return False
    if j < coord[1]:
        return False
    if j > coord[1] + size[1]:
        return False   
    return True

def renderBoard(life):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            setCell(i, j, life.getState(i, j)) 

def resetBoard(life):
     for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
           setCell(i, j, False)
           life.setDead(i, j)

def buildGlider(life):
    resetBoard(life)
    OFFSET = int(GRID_SIZE / 2)
    life.setLive(OFFSET,OFFSET)
    life.setLive(OFFSET,OFFSET+1)
    life.setLive(OFFSET,OFFSET+2)
    life.setLive(OFFSET+1,OFFSET+2)
    life.setLive(OFFSET+2,OFFSET+1)
    renderBoard(life)
    
def buildBlinker(life):
    resetBoard(life)
    OFFSET = int(GRID_SIZE / 2)
    life.setLive(OFFSET-1,OFFSET)
    life.setLive(OFFSET,OFFSET)
    life.setLive(OFFSET+1,OFFSET)
    renderBoard(life)
    
def buildPenta(life):
    resetBoard(life)
    OFFSET = int(GRID_SIZE / 2)
    life.setLive(OFFSET,OFFSET)
    life.setLive(OFFSET+1,OFFSET)
    life.setLive(OFFSET+2,OFFSET-1)
    life.setLive(OFFSET+2,OFFSET+1)
    life.setLive(OFFSET+3,OFFSET)
    life.setLive(OFFSET+4,OFFSET)
    
    life.setLive(OFFSET-1,OFFSET)
    life.setLive(OFFSET-2,OFFSET)
    life.setLive(OFFSET-3,OFFSET+1)
    life.setLive(OFFSET-3,OFFSET-1)
    life.setLive(OFFSET-4,OFFSET)
    life.setLive(OFFSET-5,OFFSET)
    renderBoard(life)
    
        
pygame.init()  
window = pygame.display.set_mode((WINDOW_SIZE + BUTTON_WIDTH, \
    WINDOW_SIZE)) 
pygame.display.set_caption('Life') 
screen = pygame.display.get_surface() 
window.fill(WHITE)

# Initialize the board
renderButton(RESET_BUTTON, RESET_TEXT, False)
renderButton(ANIMATE_BUTTON, ANIMATE_TEXT, False)
renderButton(NEXT_BUTTON, NEXT_TEXT, False)
renderButton(GLIDER_BUTTON, GLIDER_TEXT, False)
renderButton(PENTADECATHALON_BUTTON, PENTADECATHALON_TEXT, False)
renderButton(BLINKER_BUTTON, BLINKER_TEXT, False)
            
isAnimate = False
life = NeighborLife(GRID_SIZE)
renderBoard(life)

while True:
    if isAnimate: 
        life.nextGeneration()
        renderBoard(life) 
        time.sleep(.5)
         
    events = pygame.event.get()
    for event in events:  
        if event.type == QUIT:
            pygame.quit()
      	    sys.exit()
      	if event.type == MOUSEBUTTONDOWN:	
            x, y = event.pos
            if x < WINDOW_SIZE and y < WINDOW_SIZE:
                i = int(x / SQUARE_SIZE)
                j = int(y / SQUARE_SIZE)
                life.toggle(i, j)
                setCell(i, j, life.getState(i, j))
            elif intersectsWith(x, y, ANIMATE_BUTTON):
                isAnimate = not isAnimate
                renderButton(ANIMATE_BUTTON, ANIMATE_TEXT, isAnimate)
            elif intersectsWith(x, y, RESET_BUTTON):
                resetBoard(life)
            elif intersectsWith(x, y, NEXT_BUTTON):
                life.nextGeneration()
                renderBoard(life)   
            elif intersectsWith(x, y, GLIDER_BUTTON):
                buildGlider(life)
            elif intersectsWith(x, y, PENTADECATHALON_BUTTON):
                buildPenta(life)
            elif intersectsWith(x, y, BLINKER_BUTTON):
                buildBlinker(life)
                 
    pygame.display.update()    

