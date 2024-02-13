# from raylib import *
from pyray import *
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['image.cmap'] = 'binary'


width = 800
height = 800
i = 0
j = 0
cell_size = 4
arr_size = int(width/cell_size)

arr1 = np.zeros(int(arr_size))
arr2 = np.zeros(int(arr_size))
draw_arr = np.zeros((cell_size,cell_size))

arule = 101
mode = "plot_all" #either draw or plot_all.

def init_ca(arr1,arr2):
    arr1[int(len(arr1)/2)] = 1
    arr2 = arr1
    return(arr1,arr2)

def eval_rule(rule,a1,a2):
    arr1 = a1
    arr2 = a2
    bin_rule = np.binary_repr(rule,width=8)
    for i in range(0,arr_size-1):
        if(i == 0):
            pval = 0
            cval = int(arr1[i])
            nval = int(arr1[i+1])
        elif(i == arr_size):
            nval = 0
            pval = int(arr1[i-1])
            cval = int(arr1[i])
        else:
            pval = int(arr1[i-1])
            cval = int(arr1[i])
            nval = int(arr1[i+1])

        eval_str = str(pval)+str(cval)+str(nval)
        match eval_str:
            case '111':
                arr2[i] = bin_rule[0]
            case '110':
                arr2[i] = bin_rule[1]
            case '101':
                arr2[i] = bin_rule[2]
            case '100':
                arr2[i] = bin_rule[3]
            case '011':
                arr2[i] = bin_rule[4]
            case '010':
                arr2[i] = bin_rule[5]
            case '001':
                arr2[i] = bin_rule[6]
            case '000':
                arr2[i] = bin_rule[7]
    return(arr1,arr2)

def run_ca(rule):
    a1 = np.zeros(int(arr_size))
    a2 = np.zeros(int(arr_size))
    darr = []
    for i in range(0,arr_size):
        if(i==0):
            a1[int(arr_size/2)] = 1
            darr.append(a1)
        else:
            a1,a2 = eval_rule(rule,a1,a2)
            darr.append(a2)
            a1 = a2
            a2 = np.zeros(int(arr_size))
    return darr

def plot_all():
    arr1 = np.zeros(int(arr_size))
    arr2 = np.zeros(int(arr_size))

    for i in range(256):
        arr1,arr2 = init_ca(arr1,arr2)
        draw_arr = run_ca(i)
        fig, ax = plt.subplots(figsize=(16, 9))
        ax.matshow(draw_arr)
        ax.axis(False);
        fname = "rules/" + str(i) + ".png"
        title = "Rule: " + str(i)
        plt.title(title)
        plt.savefig(fname)
        plt.close()
    
init_window(width, height, b'Wolfram CA 1D')
set_target_fps(60)
if(mode == "draw"):
    arr1,arr2 = init_ca(arr1,arr2)
    draw_arr = run_ca(arule)
    while not window_should_close():
        clear_background(BLACK)
        begin_drawing()
        ptri = 0
        for i in range(0,height,cell_size):
            ptr = 0
            for j in range(0,width,cell_size):
                if(draw_arr[ptri][ptr] == 0):
                    draw_rectangle_lines(i,j,cell_size,cell_size,YELLOW)
                else:
                    draw_rectangle(i,j,cell_size,cell_size,YELLOW)
                ptr += 1
            ptri += 1
        end_drawing()
    close_window()
elif(mode=="plot_all"):
    plot_all()