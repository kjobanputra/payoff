# mainScreen.py
from tkinter import *

# This is the main screen where the user can buy more stocks, go to their 
# respective stock page, see their cash amount, and see how many days it has
# been. 

class MainScreen(object):
    def __init__(self, width, height, portfolio):
        self.width = width
        self.height = height
        self.i = 0
        self.click = False
        self.menu = False
        self.portfolio = portfolio
        self.cash = 10000
        self.name = "mainScreen"

    def update(self):
        totalCounter = 1
        for i in self.portfolio:
            if i != None:
                self.cash = i.profit + 10000
            else:
                totalCounter += 1


    def mouse(self, event):
        for i in range(10):
            if event.x > self.width//30 and event.x < 10*self.width//30:
                if event.y > (7+i)*self.height//20 and event.y < (8+i)*self.height//20:
                    self.i = i
                    if self.portfolio[i] == None:
                        return "enterStock"
                    else:
                        return i

    def key(self, event):
        pass

    def timer(self):
        pass

    def draw(self, canvas, portfolio):
        self.portfolio = portfolio
        self.update()
        canvas.create_text(self.width//8, self.height//10,
                            text = "$%d" %self.cash, 
                            font = "Avenir 30 bold", fill = "white")
        canvas.create_text(self.width//30, 3*self.height//10,
                            text = "Portfolio:", anchor=W, 
                            font = "Avenir 30 bold", fill = "white")
        
        for i in range(10):
            canvas.create_rectangle(self.width//30, (7+i)*self.height//20,
                                10*self.width//30, (8+i)*self.height//20,
                                fill = "dark gray")
            if self.portfolio[i] == None:
                canvas.create_text(55*self.width//300, (15+2*i)*self.height//40,
                                text= "(Enter new stock)", font = "Avenir 15 bold")
            else:
                canvas.create_text(55*self.width//300, (15+2*i)*self.height//40,
                                text= self.portfolio[i].name, font = "Avenir 15 bold")