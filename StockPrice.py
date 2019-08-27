#Kunal K. Jobanputra
#kjobanpu
# This file contains all of the backend methods. It has the webscraping for the
# SP500 stocks, the data gathering, the machine learning, fixing user input, and
# graphing using matplotlib. 

import datetime as dt# easy work with dates
import matplotlib# graphing 
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
from matplotlib import style
import pandas as pd # data manipulation
import pandas_datareader.data as web # get information of a given stock
import bs4 as bs # web scrape for S&P 500
import requests # to grab source code from Wikipedia page
import os
import sklearn
import multiprocessing as mp #make the csv checking funtionality quicker
import numpy as np
from sklearn.svm import SVR
import csv

def checkCSV(input):
    nameDict = SP500Companies()

    stock = case(input)

    for name in nameDict:
        caseName = case(name)
        letter = caseName[0]
        if stock.startswith(letter) and caseName.find(stock) > -1:
            return name
        

def graph(input):
    nameDict = SP500Companies()

    if checkCSV(input) != None:
        name = checkCSV(input)
        ticker = nameDict[name]

        # Choosing the plot style from matplotlib module
        plt.style.use("Solarize_Light2")

        # Using the datetime module to set the start and end dates
        start = dt.datetime(2014, 1, 1) 
        end = dt.datetime(2016, 12, 31)
        # Takes information from the internet and inputs it into the program
        df = web.DataReader(ticker, "yahoo", start, end)

        # The rolling averages are calculated. 
        fMA = "50 Day Moving Average"
        df[fMA] = df["Close"].rolling(window=50, min_periods = 0).mean()

        # Plots all of the closing prices and the 50-day moving average 
        # of the given stock
        plt.plot(df.index, df["Close"])
        plt.plot(df.index, df[fMA])
        plt.xlabel("Dates")
        plt.ylabel("Price")
        plt.title("%s Stock"%name)
        plt.legend()

        plt.show()

def SP500Companies():

    SP500 = "http://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    
    # Gets the source code using requests.
    # It is then converted to .text format, using LXML as a processor of HTML.
    # Using the find method, the table with the tickers and company names are 
    # found. 
    text = requests.get(SP500)
    soup = bs.BeautifulSoup(text.text, "lxml")
    table = soup.find("table", {"class": "wikitable sortable"})
    
    # A list of tickers and a dictionary with names mapped to the tickers are 
    # made. 
    nameDict = dict()
    for row in table.findAll("tr")[1:]:
        ticker = row.findAll("td")[0].text
        name = row.findAll("td")[1].text
        nameDict[name] = ticker

    return nameDict

def getData():
    
    nameDict = SP500Companies()

    if not os.path.exists('stocks'):
        os.makedirs('stocks')
    
    # try and except blocks with differnt APIs

    pool = mp.Pool(processes = 16)

    results = [pool.apply_async(makeCSV, args=(ticker, name)) for (name, ticker) in nameDict.items()]

def makeCSV(ticker, name, source = "yahoo"):
    # customize starting time
    start = dt.datetime(2014, 1, 1)
    end = dt.datetime(2016, 12, 31)

    if not os.path.exists("stocks/%s.csv"%name):
        print("Adding %s" %name)
        try:
            data = web.DataReader(ticker, source, start, end)

        except:
            try:
                print("Yahoo Failed")
                source = "google" 
                data = web.DataReader(ticker, source, start, end)
            except:
                pass
        data.to_csv("stocks/%s.csv"%name)
    else:
        print("Already have %s"%name)

def case(string):
    newString = string.replace(" ", "")
    returnString = newString.replace("-", "")
    return returnString.lower()

def checkFiles():
    newDict = SP500Companies()

    badFiles = []

    for name in newDict:
        file = pd.read_csv("stocks/%s.csv"%name)
        for i in file:
            if i == "<":
                badFiles.append(name)
                print("%s removed!" %name)
                os.remove("ChangedFile.csv")
                break
    if len(badFiles) > 0:
        getData()

def compileData():
    newDict = SP500Companies()

    mainDF = pd.DataFrame()

    for name in newDict:
        ticker = newDict[name]

        try:
            df = pd.read_csv("stocks/{}.csv".format(name))
            df.set_index("Date", inplace = True)

            df.rename(columns={"Close": name}, inplace= True)

            try:
                df.drop(["Open", "High", "Low", "Volume", "Adj Close"], 1, inplace= True)
            except:
                df.drop(["Open", "High", "Low", "Volume"], 1, inplace= True)

            if mainDF.empty:
                mainDF = df
            else:
                mainDF = mainDF.join(df, how= "outer")

            print(mainDF.head())

            mainDF.to_csv("stockscloseDF.csv")
        except:
            pass

def getCurrentPrice(stock, i):
    stock = checkCSV(stock)
    if stock != None:
        
        df = pd.read_csv("stocks/%s.csv"%stock)
        prices = df["Close"].values

        return prices[(len(prices)//2) +i -1]

def main():
    # graph()
    getData()
    # checkFiles()
    # compileData()
    pass

if __name__ == '__main__':
    main()
