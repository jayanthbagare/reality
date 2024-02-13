import time
import random
import numpy as np
from pandas import *
from pyray import *



windowWidth = 800
windowHeight = 800

rows,cols = (112,112)
cell_size = int(windowWidth/cols)

total_movements = 0

currarr = np.zeros(shape=(rows,cols))
newarr = np.zeros(shape=(rows,cols))

#Define the initial conditions
vacant = 0.008 # 10% of the grid id vacant
sim_threshold = 0.4 #(1-Tau) the number of neighbours equal and below warrants a move
pop_split = 0.5 # 1:1 Equal population split, must implement further

def init_grid(currarr,newarr,rows,cols):
    currarr = np.zeros(shape=(rows,cols))
    newarr = np.zeros(shape=(rows,cols))
    return currarr,newarr

def set_vacant(currarr,newarr,vacant,rows,cols):
    empty_val = int(vacant * (rows * cols))
    for i in range(empty_val):
        r = random.randint(0,rows - 1)
        c = random.randint(0,cols - 1)

        if(currarr[r][c] == 0):
            currarr[r][c] = 5
        else:
            r = random.randint(0,rows - 1)
            c = random.randint(0,cols - 1)
            currarr[r][c] = 5

    newarr = currarr
    return currarr,newarr

def populate_grid(currarr,newarr):
    for j in range(cols):
        for i in range(rows):
            if(currarr[i][j] != 5):
                r = random.random()
                if(r <= vacant):
                    currarr[i][j] = 5
                else:
                    if(random.random() <=0.5):
                        currarr[i][j] = 1
                    else:
                        currarr[i][j] = 2
    newarr = currarr
    return currarr,newarr

def segregate(currarr,newarr,sim_threshold,total_movements):
    for i in range(rows):
        for j in range(cols):        
            if(j+1<cols):
                east = 1 if currarr[i][j] == currarr[i][j+1] else 0
            else:
                east = 0

            if(i-1>=0 and j+1<cols):
                neast = 1 if currarr[i][j] == currarr[i-1][j+1] else 0
            else:
                neast = 0

            if(i-1>=0):
                north = 1 if currarr[i][j] == currarr[i-1][j] else 0
            else:
                north = 0
            
            if(i-1 >=0 and j-1>=0):
                nwest = 1 if currarr[i][j] == currarr[i-1][j-1] else 0
            else:
                nwest = 0
            
            if(j-1>=0):
                west = 1 if currarr[i][j] == currarr[i][j-1] else 0
            else:
                west = 0
            
            if(i+1 < rows and j-1>=0):
                swest = 1 if currarr[i][j] == currarr[i+1][j-1] else 0
            else:
                swest = 0
            
            if(i+1 < rows):
                south = 1 if currarr[i][j] == currarr[i+1][j] else 0
            else:
                south = 0
            
            if(i+1 < rows and j+1 < cols):
                seast = 1 if currarr[i][j] == currarr[i+1][j+1] else 0
            else:
                seast = 0

            total_count = east + neast + north + nwest + west + swest + south + seast
            if(total_count/8 < sim_threshold):
                #get the first possible vacant location
                vacant_slots = np.argwhere(newarr == 5)[0]
                newarr[vacant_slots[0]][vacant_slots[1]] = currarr[i][j]
                newarr[i][j] = 5
                total_movements += 1
    currarr = newarr
    return currarr,newarr,total_movements

init_window(windowWidth,windowHeight,"Schelling Segregation Simulation")
currarr,newarr = init_grid(currarr,newarr,rows,cols)
# currarr,newarr = set_vacant(currarr,newarr,vacant,rows,cols)
currarr,newarr = populate_grid(currarr,newarr)

while not window_should_close():
    begin_drawing()
    total_movements = 0
    currarr,newarr,total_movements = segregate(currarr,newarr,sim_threshold,total_movements)
    for i in range(rows):
        for j in range(cols):
            draw_rectangle_lines(i*cell_size,j*cell_size,cell_size,cell_size,VIOLET)
            if(currarr[i][j] == 1):
                draw_circle(int(i*cell_size + cell_size/2),int(j*cell_size + cell_size/2),cell_size/4,YELLOW)
            if(currarr[i][j] == 2):
                draw_circle(int(i*cell_size + cell_size/2),int(j*cell_size + cell_size/2),cell_size/4,GREEN)
    # wait_time(0.2)
    end_drawing()
close_window()