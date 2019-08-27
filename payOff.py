# Kunal K. Jobanputra

# Main file where different modes are dispatched from. 
# Outline taken from the course website

from tkinter import *
from StockPrice import *
import string
from story import *
from startScreen import *
from mainScreen import *
from enterStock import *
from stock import *
from stockHome import *

def init(data):
    data.mode = "story"
    data.counter = 0
    data.portfolio = [ None for i in range(10)]
    data.stockHomeList = [ None for i in range(10)]
    data.dayCounter = 0
    data.day = 1
    data.i = 0
    data.background = PhotoImage(file = "moneyback.gif")
    data.storyScreen = Story(data.width, data.height)
    data.startScreen = StartScreen(data.width, data.height)
    data.mainScreen = MainScreen(data.width, data.height, data.portfolio)
    data.enterStock = EnterStock(data.width, data.height, data.day, data.portfolio, data.stockHomeList)
    data.list = [data.storyScreen, data.startScreen, data.mainScreen, data.enterStock]

####################################
# mode dispatcher
####################################
def keyPressed(event, data):
    if not(isinstance(data.mode, str)):
        result = data.mode.key(event)
        data.mode = result[0]
        data.portfolio = result[1]
    for i in (data.list):
        if data.mode == i.name:
            if data.mode == data.mainScreen:
                result = i.key(event)
                data.mode = data.stockHomeList[result]
            else:
                result = i.key(event)
                if isinstance(result, str):
                    data.mode = result
                elif isinstance(result, tuple):
                    data.mode = result[0]
                    data.portfolio = result[1]
                    data.stockHomeList = result[2]

def mousePressed(event, data):
    if not(isinstance(data.mode,str)) and data.mode != None:
        result = data.mode.mouse(event)
        data.mode = result[0]
        print("mode: ", data.mode)
        data.portfolio = result[1]
    for i in (data.list):
        if data.mode == i.name:
            result = i.mouse(event)
            if data.mode == "mainScreen" and result != "enterStock":
                try:
                    data.mode = data.stockHomeList[result]
                    data.stockHomeBool = True
                except:
                    pass
            else:
                if isinstance(result, str):
                    data.mode = result
                elif isinstance(result, tuple):
                    data.mode = result[0]
                    if isinstance(result[1], list):
                        data.portfolio = result[1]
                    else:
                        data.i = result[1]
                    data.stockHomeList = result[2]

def timerFired(data):
    if not(isinstance(data.mode,str)) and data.mode != None:
        result = data.mode.timer()
        data.mode = result
    for i in (data.list):
        if data.mode == i.name:
            result = i.timer()
    data.dayCounter += 1
    if data.mode != "story" and data.mode != "startScreen":
        if data.dayCounter % 600 == 0:
            data.day += 1
        
def redrawAll(canvas, data):
    canvas.create_image(0, 0, anchor=NW, image = data.background)
    for i in (data.list):
        if not(isinstance(data.mode,str)):
            data.mode.draw(canvas)
        if data.mode == "mainScreen":
            canvas.create_text(7*data.width//8, data.height//10,
                            text = "Day %d"%data.day, font = "Arial 30 bold", fill = "white")
            result = data.mainScreen.draw(canvas, data.portfolio)
        elif data.mode == i.name:
            result = i.draw(canvas)

#######################################
# Below code taken from course website
#######################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    root = Tk()
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(500, 500)