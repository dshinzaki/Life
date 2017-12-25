# Dylan Shinzaki
# 9/10/13
# Improved implementation of Conway's game of life.
# Stores universe as a hashmap to allow for efficient
# storage of arbitrarily large universes.

# Uses a change list to only consider changed cells and 
# neighbors of changed cells when calculating the next
# generation.

# BasicLife(n): constructs nxn universe indexed from 0 to n-1
# toggle(i,j): changes the state of (i, j) to the opposite
# getState(i, j): Returns true if (i, j) is live and false otherwise
# setLive(i, j): Sets (i, j) to be alive
# setDead(i, j): Sets (i, j) to be dead
# nextGeneration(): Simulates the next generation based game of 
#   life rules
# printGrid(xmin = -10, xmax = 10, ymin = -10, ymax = 10):
#   Prints universe from [xmin, xmax] and [ymin, ymax] in 
#   human readable format
# listCells(): Prints current live cells
# listChangeList(): Prints current list of changed cells

# Execution:
# python hashmapLife.py
# Executes a test script

from sets import Set

class HashmapLife(object):
    def __init__(self):
        self.liveCells = {}
        self.changeList = Set()
        self.DEAD = 0
        self.LIVE = 1
                
    def __getNeighbors(self, i, j):
        assert type(i) is int,  "i is not an integer: %r" % i
        assert type(j) is int,  "j is not an integer: %r" % j
        
        neighbors = list()
        for x in (i-1, i, i+1):
            for y in (j-1, j, j+1):
                if x != i or y != j:
                    neighbors.append((x, y))
        return neighbors
        
    def __liveNeighborCount(self, i, j):
        assert type(i) is int,  "i is not an integer: %r" % i
        assert type(j) is int,  "j is not an integer: %r" % j
    
        val = 0
        for point in self.__getNeighbors(i, j):
            if point in self.liveCells:
                val = val + 1
        return val
   
    def getState(self, i, j):
        return (i, j) in self.liveCells
        
    def toggle(self, i, j):
        if self.getState(i, j):
            self.setDead(i, j)
        else:
            self.setLive(i, j)        
   
    def listCells(self):
        for i in self.liveCells.keys():
            print str(i)

    def listChangeList(self):
        for i in self.changeList:
            print i
            
    def setLive(self, i, j):
        assert type(i) is int,  "i is not an integer: %r" % i
        assert type(j) is int,  "j is not an integer: %r" % j
    
        if (i, j) in self.liveCells:
            return
        for point in self.__getNeighbors(i, j):
            self.changeList.add(point)
            if point in self.liveCells:
                self.liveCells[point] = self.liveCells[point] + 1 
        self.liveCells[(i, j)] = self.__liveNeighborCount(i, j)
        self.changeList.add((i, j))
            
    def setDead(self, i , j):
        assert type(i) is int,  "i is not an integer: %r" % i
        assert type(j) is int,  "j is not an integer: %r" % j
    
        if (i, j) in self.liveCells:
            for point in self.__getNeighbors(i, j):
                self.changeList.add(point)  
                if point in self.liveCells:
                    self.liveCells[point] = self.liveCells[point] - 1
            del self.liveCells[(i, j)]
            self.changeList.add((i, j))
              
    def nextGeneration(self):
        currList = self.changeList
        toToggle = Set()
        self.changeList = Set()
        
        for point in currList:
            if point in self.liveCells:
                val = self.liveCells[point]
                if val != 2 and val != 3:
                    toToggle.add(point)               
            else:
                if self.__liveNeighborCount(point[0], point[1]) == 3:
                    toToggle.add(point)
        
        for point in toToggle:
            self.toggle(point[0], point[1])

                
    def printGrid(self, xmin = -10, xmax = 10, ymin = -10, ymax = 10):
        assert type(xmin) is int,  "xmin is not an integer: %r" % xmin
        assert type(xmax) is int,  "xmax is not an integer: %r" % xmax
        assert type(ymin) is int,  "ymin is not an integer: %r" % ymin
        assert type(ymax) is int,  "ymax is not an integer: %r" % ymax
    
        if xmin >= xmax:
            print "Error: x range invalid"
        if ymin >= ymax: 
            print "Error: y range invalid"
        
        for i in range(xmin, xmax+1):
            curr = ""
            for j in range(ymin, ymax+1):
                if (i, j) in self.liveCells:
                    curr = curr + "X"
                else:
                    curr = curr + "."
            print curr 

if __name__=="__main__":
    print "Testing possibly infinite universe"
    life = HashmapLife()
    life.setLive(0, 0)
    life.setLive(0, 1)
    life.setLive(0, 2)
    
    life.listCells()
    life.printGrid()
    
    print "*"*10
    life.nextGeneration()
    life.listCells()
    life.printGrid()
    
    print "*"*10
    life.nextGeneration()
    life.listCells()
    life.printGrid()
    
    print "*"*10
    life.nextGeneration()
    life.listCells()
    life.printGrid()    
    
        