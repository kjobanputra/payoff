# enterStock.py

# This is for when a new stock needs to be entered. A user can buy, sell, and 
# predict prices. 
from stock import *
from stockHome import *
from StockPrice import *
from tkinter import *
import string

class EnterStock(object):
    def __init__(self, width, height, day, portfolio, stockHomeList):
        self.width = width
        self.height = height
        self.input = ""
        self.buyInput = ""
        self.sellInput = ""
        self.predictInput = ""
        self.mode = "graph"
        self.error = False
        self.name = "enterStock"
        self.amount = "Amount of shares?"
        self.modeList = ["buy", "sell", "predict"]
        self.i = 0
        self.buy = False
        self.sell = False
        self.predict = False
        self.image = PhotoImage(file = "backarrow.gif")
        self.count = 0
        self.predictedPrice = 0
        self.portfolio = portfolio
        self.stockHomeList = stockHomeList
        self.day = day
        self.sellError = False

    def instantiate(self, name, currentPrice, shares, calculatedProfit):
        notFound = True
        firstNoneIndex = -1
        for i in range(len(self.portfolio)):
            stockObject = self.portfolio[i]
            if stockObject != None:
                if(stockObject.name == name):
                    notFound = False
                    stockObject.shares += shares
                    stockObject.price = currentPrice
                    stockObject.profit += calculatedProfit
                    if stockObject.shares < 1:
                        if stockObject.shares == 0:
                            stockObject = None
                        else:
                            self.sellError = True
                            stockObject.shares -= shares
                    self.portfolio[i] = stockObject
                    self.stockHomeList[i] = StockHome(self.width, self.height, self.portfolio, i, self.day, self.stockHomeList)
                
            else:
                if(firstNoneIndex == -1):
                    firstNoneIndex = i

        if(notFound):
            if shares > 0:
                newStock = Stock(name, shares, currentPrice)
                newStock.profit = calculatedProfit
                self.portfolio[firstNoneIndex] = newStock
                self.stockHomeList[firstNoneIndex] = StockHome(self.width, self.height, self.portfolio, firstNoneIndex, self.day, self.stockHomeList)
            else:
                self.sellError = True

    def mouse(self, event):
        if event.x > self.width//15 and event.x < 14*self.width//15:
            if event.y > 4*self.height//10 and event.y < 5*self.height//10:
                self.mode = "graph"
        # Back arrow back to mainScreen
        if event.x > 0 and event.x < 2*self.width//30:
            if event.y > 0 and event.y < 2*self.height//30:
                self.input = ""
                self.buyInput = ""
                self.sellInput = ""
                self.predictInput = ""
                self.predictedPrice = 0
                return ("mainScreen", self.portfolio, self.stockHomeList)
        
        for i in range(3):
            if event.x > (10*i+1)*self.width//30 and event.x < (10*i+9)*self.width//30:
                if event.y > 6*self.height//10 and event.y < 7*self.height//10:
                    self.i = i
                    self.mode = self.modeList[self.i].lower()

    def graphKey(self, event):
        if event.keysym == "BackSpace":
            self.input = self.input[:-1]
            self.error = False
        if len(self.input) <= 20 and self.mode == "graph":
            if event.keysym in string.ascii_letters:
                self.input += event.keysym
            elif event.keysym == "minus":
                self.input += "-"
            elif event.keysym == "period":
                self.input += "."
            elif event.keysym == "space":
                self.input += " "
        if event.keysym == "Return":
            input = self.input
            self.input = ""
            if graph(input) == None:
                    self.error = True

    def buyKey(self, event):
        if event.keysym == "BackSpace":
            self.buyInput = self.buyInput[:-1]
            self.error = False
        if len(self.buyInput) < 3:
            if event.keysym.isdigit():
                self.buyInput += event.keysym
        if event.keysym == "Return":
            self.buy = True
            input = self.input
            name = checkCSV(input)
            
            buyInput = self.buyInput
            currentPrice = getCurrentPrice(name, self.day)
            calculatedProfit = currentPrice*(int(buyInput)*-1)

            self.instantiate(name, currentPrice, int(buyInput), calculatedProfit)

    def sellKey(self, event):
        if event.keysym == "BackSpace":
            self.sellInput = self.sellInput[:-1]
            self.error = False
        if len(self.sellInput) < 3:
            if event.keysym.isdigit():
                self.sellInput += event.keysym
        if event.keysym == "Return":
            self.sell = True
            input = self.input
            name = checkCSV(input)

            sellInput = self.sellInput
            currentPrice = getCurrentPrice(name, self.day)
            calculatedProfit = currentPrice*(int(sellInput))
            
            self.instantiate(name, currentPrice, (int(sellInput)*-1), calculatedProfit)

    def predictKey(self, event):
        if event.keysym == "BackSpace":
            self.predictInput = self.predictInput[:-1]
            self.error = False
        if len(self.predictInput) < 3:
            if event.keysym.isdigit():
                self.predictInput += event.keysym
        if event.keysym == "Return":
            self.predictPrice(self.input, int(self.predictInput))
            if self.predictedPrice == None:
                self.error = True
                self.input = ""
                self.predictInput = ""
            else:
                self.predict = True
                self.predictInput = ""

    def key(self, event):
        if self.mode == "graph":
            self.graphKey(event)
        elif self.mode == "buy":
            self.buyKey(event)
        elif self.mode == "sell":
            self.sellKey(event)
        elif self.mode == "predict":
            self.predictKey(event)
        if event.keysym == "Left":
            self.input = ""
            self.buyInput = ""
            self.sellInput = ""
            self.predictInput = ""
            self.predictedPrice = 0
            return ("mainScreen", self.portfolio, self.stockHomeList)

    def graphDraw(self, canvas):
        pass

    def buyDraw(self, canvas):
        canvas.create_rectangle((10*self.i+1)*self.width//30, 8*self.height//10,
                                    (10*self.i+9)*self.width//30, 9*self.height//10,
                                    fill = "light gray")
        # Instructions for user

        if self.buy:
            if self.buyInput == "1":
                canvas.create_text((10*self.i+5)*self.width//30, 85*self.height//100,
                        text = "Bought %s share"%self.buyInput, font = "Avenir 15 bold",
                        fill = "red") 
            else:
                canvas.create_text((10*self.i+5)*self.width//30, 85*self.height//100,
                        text = "Bought %s shares"%self.buyInput, font = "Avenir 15 bold",
                        fill = "red") 
        else:
            if self.buyInput == "":
                canvas.create_text((10*self.i+5)*self.width//30, 85*self.height//100,
                        text = self.amount, font = "Avenir 10")
            canvas.create_text((10*self.i+5)*self.width//30, 85*self.height//100,
                        text = self.buyInput, font = "Avenir 20 bold")
        
    def sellDraw(self, canvas):
        canvas.create_rectangle((10*self.i+1)*self.width//30,
                                8*self.height//10,
                                (10*self.i+9)*self.width//30, 
                                9*self.height//10,
                                fill = "light gray")
        # Instructions for user

        if self.sellError:
            canvas.create_text((10*self.i+5)*self.width//30,
                                93*self.height//100,
                                text = "Can't sell more than you have!",
                                font = "Avenir 10", fill = "red")

        elif self.sellInput == "" and not self.sell:
            canvas.create_text((10*self.i+5)*self.width//30, 
                                    85*self.height//100,
                                    text = self.amount, 
                                    font = "Avenir 10")  
        
        elif self.sell:
            if self.sellInput == "1":
                canvas.create_text((10*self.i+5)*self.width//30, 
                                85*self.height//100,
                                text = "Sold %s share" % (self.sellInput), 
                                font = "Avenir 15 bold", 
                                fill = "red") 
            else:
                canvas.create_text((10*self.i+5)*self.width//30, 
                                85*self.height//100,
                                text = "Sold %s shares" % (self.sellInput), 
                                font = "Avenir 15 bold", 
                                fill = "red") 
        else:
            self.sellError = False
            canvas.create_text((10*self.i+5)*self.width//30, 
                                85*self.height//100,
                                text = self.sellInput, 
                                font = "Avenir 20 bold")
    
        
        
    def predictDraw(self, canvas):
        canvas.create_rectangle((10*self.i+1)*self.width//30, 8*self.height//10,
                                    (10*self.i+9)*self.width//30, 9*self.height//10,
                                    fill = "light gray")
        # Instructions for user
        if self.predict:
            canvas.create_text((10*self.i+5)*self.width//30, 85*self.height//100,
                    text = "Predicted Price: \n%0.2f" % self.predictedPrice, 
                    font = "Avenir 15 bold", fill = "red")
        else:
            if self.predictInput == "":
                canvas.create_text((10*self.i+5)*self.width//30, 85*self.height//100,
                            text = "Amount of days?", font = "Avenir 10")

            canvas.create_text((10*self.i+5)*self.width//30, 85*self.height//100,
                    text = self.predictInput, font = "Avenir 20 bold")
        

    def draw(self, canvas):
        canvas.create_text(self.width//30, self.height//30,
                        text = "←", font = "Avenir 30 bold", fill = "white")

        canvas.create_text(self.width//2, 2*self.height//10, 
                    text = "Enter desired S&P 500 Stock here",
                    font = "Avenir 30 bold", fill = "white")
        
        canvas.create_rectangle(self.width//15, 4*self.height//10,
                        14*self.width//15, 5*self.height//10,
                        fill = "light gray")
        canvas.create_text(self.width//2, 45*self.height//100,
                            text = self.input, font = "Avenir 30 bold")
        # Instructions for user
        if self.input == "":
            canvas.create_text(75*self.width//150, 45*self.height//100,
                                text= "Press enter to graph")
        
        # If an invalid stock is entered
            if self.error:
                canvas.create_text(self.width//2, 53*self.height//100,
                                text = "Invalid stock", font = "Avenir 10", fill = "red")

        for i in range(3):
            if i == 0:
                button = "BUY"
            if i == 1:
                button = "SELL"
            if i == 2:
                button = "PREDICT"

            canvas.create_rectangle((10*i+1)*self.width//30, 6*self.height//10,
                                    (10*i+9)*self.width//30, 7*self.height//10,
                                    fill = "dark gray")
            canvas.create_text((10*i+5)*self.width//30, 65*self.height//100,
                                text = button, font = "Avenir 30 bold")
        if self.mode == "graph":
            self.graphDraw(canvas)
        elif self.mode == "buy":
            self.buyDraw(canvas)
        elif self.mode == "sell":
            self.sellDraw(canvas)
        elif self.mode == "predict":
            self.predictDraw(canvas)

    def timer(self):
        if self.buy or self.sell or self.predict:
            self.count += 1
            if self.count == 30:
                self.count = 0
                self.buy = False
                self.buyInput = ""
                self.sell = False
                self.sellInput = ""
                self.predictedPrice = 0
                self.predict = False
        elif self.sellError:
            self.count += 1
            if self.count == 20:
                self.count = 0
                self.sellError = False

    def predictPrice(self, stock, x):
        stock = checkCSV(stock)
        if stock != None:
            df = pd.read_csv("stocks/%s.csv"%stock)
            dates = df.index.values
            prices = df["Close"].values

            dates = np.reshape(dates,(len(dates), 1))
            svrRBF = SVR(kernel = "rbf", C = 1e3, gamma = 0.1)
            svrRBF.fit(dates, prices)
            plt.scatter(dates, prices, color = "black", label = "Data")
            plt.plot(dates, svrRBF.predict(dates), color  = "red", label = "RBF model")
            
            plt.xlabel("Number of days since 2014 for %s"%stock)
            plt.ylabel("Price")
            plt.title("Support Vector Regression")
            plt.legend()

            self.predictedPrice = svrRBF.predict(x)[0]

            plt.show(block = False)

            