#import tkinter as tk
import tkinter
from tkinter import *
from tkinter import messagebox
import numpy as np
import random

master = tkinter.Tk()

master.title("MineFind")

#prepare default values

rows = 20
cols = 20
mines = 10

pattern = 0
buttons = []

colors = ['#FFFFFF', '#0000FF', '#008200', '#FF0000', '#000084', '#840000', '#008284', '#840084', '#000000']

gameover = False
customsizes = []

#prepare menu
def createMenu():
    menubar = tkinter.Menu(master)
    filemenu = tkinter.Menu(master, tearoff=0)
    filemenu.add_command(label="9*9", command=lambda: setSize(9, 9, 10))
    filemenu.add_command(label="16*16", command=lambda: setSize(16, 16, 40))
    filemenu.add_command(label="30*16", command=lambda: setSize(16, 30, 99))
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=lambda: master.destroy())
    menubar.add_cascade(label="File", menu=filemenu)
    master.config(menu=menubar)

#set global variables-rows, cols, mines
def setSize(r,c,m):
    global rows, cols, mines
    rows = r
    cols = c
    mines = m
    restartGame()

#detect region(mine) by using recursion and count the number of neighbor mines
def detect_region(p,x,y):
    global rows, cols
    for yy in range(-1,2):
        for xx in range(-1,2):
            if x+xx<0:continue
            if x+xx>=rows:continue
            if y+yy<0:continue
            if y+yy>=cols:continue
            if p[0][x+xx][y+yy]==-1 and p[0][x][y]!=-1:
                p[0][x][y] += 1
            p[1][x][y] = 1
            if(p[1][x+xx][y+yy] != 1):
                detect_region(p,x+xx,y+yy)

#Get ready for game: Generate mines, set the global variable-pattern
def makeGame():
    global rows, cols, mines, pattern
    b = np.arange(4*rows*cols).reshape(4,rows,cols)# numberoftype  width height
    pattern = b
    for i in range(0,4):
        for j in range(0,rows):
            for k in range(0,cols):
                pattern[i][j][k] = 0
    #generate mines
    m = 0
    while(m<mines):
        w = random.randint(0,rows-1)
        h = random.randint(0,cols-1)
        if pattern[0][w][h] == 0:
            pattern[0][w][h] = -1
            m+=1
    detect_region(pattern,0,0)

#Get ready for game: Generate buttons for mine, flag and non-tile, bind the right, left click buttons by using bind
#set the size of gird, set the global variable-buttons
def makewindow():
    global rows, cols, buttons
    buttons = []
    for x in range(0, rows):
        buttons.append([])
        for y in range(0, cols):
            b = tkinter.Button(master, text=" ", width=2, command=lambda x=x,y=y: clickOn(x,y))
            b.bind("<Button-3>", lambda e,  x=x, y=y:onRightClick(x, y))
            b.grid(row=x+1, column=y, sticky=tkinter.N+tkinter.W+tkinter.S+tkinter.E)
            buttons[x].append(b)

#To restart game, destroy objects except for 'Menu'
def restartGame():
    global gameover
    gameover = False
    #destroy all - prevent memory leak
    for x in master.winfo_children():
        if type(x) != tkinter.Menu:
            x.destroy()
    makewindow()
    makeGame()

#Make the function when user clicks the left mouse
#Make decision depend on pattern and reveal the mines if user clicks mine
#If player lose, show up the message box
def clickOn(x,y):
    global pattern, buttons, colors, gameover, rows, cols
    if gameover:
        return 
    buttons[x][y]["text"] = str(pattern[0][x][y])
    if pattern[0][x][y] == -1:
        buttons[x][y]["text"] = "*"
        buttons[x][y].config(background='red', disabledforeground='black')
        gameover = True
        tkinter.messagebox.showinfo("Game Over", "You lost.")
        #now show all other mines
        for _x in range(0, rows):
            for _y in range(cols):
                if pattern[0][_x][_y] == -1:
                    buttons[_x][_y]["text"] = "*"
    else:
        buttons[x][y].config(disabledforeground=colors[pattern[0][x][y]])
    if pattern[0][x][y] == 0:
        buttons[x][y]["text"] = " "
        #now repeat for all buttons nearby which are 0... kek
        autoClickOn(x,y)
    buttons[x][y]['state'] = 'disabled'
    buttons[x][y].config(relief=tkinter.SUNKEN)
    checkWin()

#When the user clicks non-mine button, the neighbor tiles show up if the neighbors have no mine
#This gonna be on 'autoClickOn'
def autoClickOn(x,y):
    global pattern, buttons, colors, rows, cols
    if buttons[x][y]["state"] == "disabled":
        return
    if pattern[0][x][y] != 0:
        buttons[x][y]["text"] = str(pattern[0][x][y])
    else:
        buttons[x][y]["text"] = " "
    buttons[x][y].config(disabledforeground=colors[pattern[0][x][y]])
    buttons[x][y].config(relief=tkinter.SUNKEN)
    buttons[x][y]['state'] = 'disabled'
    if pattern[0][x][y] == 0:
        #autoClickOn by recursion
        if x != 0 and y != 0:
            autoClickOn(x-1,y-1)
        if x != 0:
            autoClickOn(x-1,y)
        if x != 0 and y != cols-1:
            autoClickOn(x-1,y+1)
        if y != 0:
            autoClickOn(x,y-1)
        if y != cols-1:
            autoClickOn(x,y+1)
        if x != rows-1 and y != 0:
            autoClickOn(x+1,y-1)
        if x != rows-1:
            autoClickOn(x+1,y)
        if x != rows-1 and y != cols-1:
            autoClickOn(x+1,y+1)

#User can mark mine sign for 'M' if the tile supposed to be mine tile
def onRightClick(x,y):
    global buttons
    if gameover:
        return
    if buttons[x][y]["text"] == "M":
        buttons[x][y]["text"] = " "
        buttons[x][y]["state"] = "normal"
    elif buttons[x][y]["text"] == " " and buttons[x][y]["state"] == "normal":
        buttons[x][y]["text"] = "M"
        buttons[x][y]["state"] = "disabled"

#User gonna win if there's no left over non-mine tiles
#This function should executed during mainloop
#If user wins, messagebox gonna pop up
def checkWin():
    global buttons, pattern, rows, cols
    win = True
    for x in range(0, rows):
        for y in range(0, cols):
            if pattern[0][x][y] != -1 and buttons[x][y]["state"] == "normal":
                win = False
    if win:
        tkinter.messagebox.showinfo("Game over","You win.")


createMenu()

makewindow()
makeGame()
master.mainloop()


