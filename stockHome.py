# stockHome.py
# If a stock has already been entered, they are taken to its repective stockHome
# page. A user can buy, sell, or predict prices. They have stock information in 
# this page. 
from StockPrice import *

class StockHome(object):
    def __init__(self, width, height, portfolio, i, day, stockHomeList):
        self.width = width
        self.height = height
        self.portfolio = portfolio
        self.i = i
        self.name = self.portfolio[self.i].name
        self.shares = self.portfolio[self.i].shares
        self.price = self.portfolio[self.i].price
        self.profit = self.portfolio[self.i].profit
        self.buyInput = ""
        self.sellInput = ""
        self.predictInput = ""
        self.mode = ""
        self.amount = "Amount of shares?"
        self.modeList = ["buy", "sell", "predict"]
        self.j = 0
        self.buy = False
        self.sell = False
        self.predict = False
        self.count = 0
        self.predictedPrice = 0
        self.stockHomeList = stockHomeList
        self.portfolio = portfolio
        self.day = day
        self.sellError = False

    def update(self, currentPrice, shares, profit):
        self.price = getCurrentPrice(self.name, self.day)
        self.shares += shares
        self.profit += profit

        if self.shares < 1:
            self.portfolio[self.i] = None
        else:
            self.portfolio[self.i].price = self.price
            self.portfolio[self.i].shares = self.shares
            self.portfolio[self.i].profit = self.profit
        return self.portfolio


    def key(self, event):
        if event.keysym == "Left":
            return "mainScreen"
        elif self.mode == "buy":
            return (self.stockHomeList[self.i], self.buyKey(event))
        elif self.mode == "sell":
            return (self.stockHomeList[self.i], self.sellKey(event))
        elif self.mode == "predict":
            self.predictKey(event)
        return (self.stockHomeList[self.i], self.portfolio)

    def buyKey(self, event):
        if event.keysym == "BackSpace":
            self.buyInput = self.buyInput[:-1]
        if len(self.buyInput) < 3:
            if event.keysym.isdigit():
                self.buyInput += event.keysym
        if event.keysym == "Return":
            self.buy = True

            buyInput = self.buyInput
            currentPrice = getCurrentPrice(self.name, self.day)
            calculatedProfit = currentPrice*(int(buyInput)*-1)

            return self.update(currentPrice, int(buyInput), calculatedProfit)

    def sellKey(self, event):
        if event.keysym == "BackSpace":
            self.sellInput = self.sellInput[:-1]
        if len(self.sellInput) < 3:
            if event.keysym.isdigit():
                self.sellInput += event.keysym
        if event.keysym == "Return":
            self.sell = True

            sellInput = self.sellInput
            currentPrice = getCurrentPrice(self.name, self.day)
            calculatedProfit = currentPrice*(int(sellInput))
            
            return self.update(currentPrice, (int(sellInput)*-1), calculatedProfit)

    def predictKey(self, event):
        if event.keysym == "BackSpace":
            self.predictInput = self.predictInput[:-1]
        if len(self.predictInput) < 3:
            if event.keysym.isdigit():
                self.predictInput += event.keysym
        if event.keysym == "Return":
            self.predictPrice(self.name, int(self.predictInput))
            self.predict = True
            self.predictInput = ""

    def mouse(self, event):
        if event.x > 0 and event.x < 2*self.width//30:
            if event.y > 0 and event.y < 2*self.height//30:
                return ("mainScreen", self.portfolio)
        for i in range(3):
            if event.x > (10*i+1)*self.width//30 and event.x < (10*i+9)*self.width//30:
                if event.y > 6*self.height//10 and event.y < 7*self.height//10:
                    self.j = i
                    self.mode = self.modeList[self.j].lower()
        return (self.stockHomeList[self.i], self.portfolio)


    def draw(self, canvas):
        canvas.create_text(self.width//2, self.height//10, 
                            text = "Stock Home", font= "Avenir 30 bold", fill = "white")
        canvas.create_text(self.width//2, 2*self.height//10, 
                            text = self.name, font = "Avenir 20", fill = "white")
        canvas.create_text(self.width//2, 4*self.height//10, 
                            text = "Shares: %d"%self.shares, font = "Avenir 20 bold", fill = "white")
        canvas.create_text(self.width//2, 5*self.height//10, 
                            text = "Price: %0.2f"%self.price, font = "Avenir 20 bold", fill = "white")
        canvas.create_text(28*self.width//30, self.height//10,
                            text = "Profit:", font = "Avenir 20 bold", fill = "white")
        canvas.create_text(28*self.width//30, 15*self.height//100,
                            text = "%0.2f"%self.profit, font = "Avenir 20 bold", fill = "white")
        canvas.create_text(self.width//30, self.height//30,
                        text = "←", font = "Avenir 30 bold", fill = "white")
        canvas.create_rectangle((10*self.j+1)*self.width//30, 8*self.height//10,
                                    (10*self.j+9)*self.width//30, 9*self.height//10,
                                    fill = "light gray")
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
        if self.mode == "buy":
            self.buyDraw(canvas)
        elif self.mode == "sell":
            self.sellDraw(canvas)
        elif self.mode == "predict":
            self.predictDraw(canvas)

    def buyDraw(self, canvas):
        canvas.create_rectangle((10*self.j+1)*self.width//30, 8*self.height//10,
                                    (10*self.j+9)*self.width//30, 9*self.height//10,
                                    fill = "light gray")
        # Instructions for user

        if self.buy:
            if self.buyInput == "1":
                canvas.create_text((10*self.j+5)*self.width//30, 85*self.height//100,
                        text = "Bought %s share"%self.buyInput, font = "Avenir 15 bold",
                        fill = "red") 
            else:
                canvas.create_text((10*self.j+5)*self.width//30, 85*self.height//100,
                        text = "Bought %s shares"%self.buyInput, font = "Avenir 15 bold",
                        fill = "red") 
        else:
            if self.buyInput == "":
                canvas.create_text((10*self.j+5)*self.width//30, 85*self.height//100,
                        text = self.amount, font = "Avenir 10")
            canvas.create_text((10*self.j+5)*self.width//30, 85*self.height//100,
                        text = self.buyInput, font = "Avenir 20 bold")
        
    def sellDraw(self, canvas):
        canvas.create_rectangle((10*self.j+1)*self.width//30,
                                8*self.height//10,
                                (10*self.j+9)*self.width//30, 
                                9*self.height//10,
                                fill = "light gray")
        # Instructions for user

        if self.sellError:
            canvas.create_text((10*self.j+5)*self.width//30,
                                93*self.height//100,
                                text = "Can't sell more than you have!",
                                font = "Avenir 10", fill = "red")

        elif self.sellInput == "" and not self.sell:
            canvas.create_text((10*self.j+5)*self.width//30, 
                                    85*self.height//100,
                                    text = self.amount, 
                                    font = "Avenir 10")  
        
        elif self.sell:
            if self.sellInput == "1":
                canvas.create_text((10*self.j+5)*self.width//30, 
                                85*self.height//100,
                                text = "Sold %s share" % (self.sellInput), 
                                font = "Avenir 15 bold", 
                                fill = "red") 
            else:
                canvas.create_text((10*self.j+5)*self.width//30, 
                                85*self.height//100,
                                text = "Sold %s shares" % (self.sellInput), 
                                font = "Avenir 15 bold", 
                                fill = "red") 
        else:
            self.sellError = False
            canvas.create_text((10*self.j+5)*self.width//30, 
                                85*self.height//100,
                                text = self.sellInput, 
                                font = "Avenir 20 bold")
    
        
        
    def predictDraw(self, canvas):
        canvas.create_rectangle((10*self.j+1)*self.width//30, 8*self.height//10,
                                    (10*self.j+9)*self.width//30, 9*self.height//10,
                                    fill = "light gray")
        # Instructions for user
        if self.predict:
            canvas.create_text((10*self.j+5)*self.width//30, 85*self.height//100,
                    text = "Predicted Price: \n%0.2f" % self.predictedPrice, 
                    font = "Avenir 15 bold", fill = "red")
        else:
            if self.predictInput == "":
                canvas.create_text((10*self.j+5)*self.width//30, 85*self.height//100,
                            text = "Amount of days?", font = "Avenir 10")

            canvas.create_text((10*self.j+5)*self.width//30, 85*self.height//100,
                    text = self.predictInput, font = "Avenir 20 bold")

    def timer(self):
        if self.buy or self.sell or self.predict:
            self.count += 1
            if self.count == 20:
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
        return self.stockHomeList[self.i]

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