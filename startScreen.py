#startScreen.py
from tkinter import *
# This is a simple start screen that the user can press start or press enter to
# begin the game. 

class StartScreen(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.dollarCY = 0
        self.name = "startScreen"

    def mouse(self, event):
        if event.x > self.width//4 and event.x < 3*self.width//4:
            if event.y >  5*self.height//8 and event.y < 6*self.height//8:
                return "mainScreen"

    def key(self, event):
        if event.keysym == "Return":
            return "mainScreen"

    def timer(self):
        self.dollarCY += self.width//30
        self.dollarCY %= self.width

    def draw(self, canvas):
        canvas.create_text(self.width//15, self.dollarCY, text = "$", 
                                font = "Avenir 50 bold", fill = "white")
        
        canvas.create_text(14*self.width//15, self.dollarCY, text = "$", 
                                font = "Avenir 50 bold", fill = "white")
        
        canvas.create_text(self.width//2, self.height//2, 
                            text = "PayOff!", 
                            font = "Avenir 50 bold", fill = "white")
        
        canvas.create_rectangle(self.width//4, 5*self.height//8, 
                                3*self.width//4, 6*self.height//8, 
                                fill = "dark gray")
        
        canvas.create_text(self.width//2, 11*self.height//16, text = "Enter", 
                                font = "Avenir 40 bold")


