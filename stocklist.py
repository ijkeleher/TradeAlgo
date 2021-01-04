import time
import urllib
import requests
from splinter import Browser
from bs4 import BeautifulSoup
from lowHigh import get_quote, get_cash_balance, buy_stock, place_saved_order, sell_stock

url = "https://www.tradingview.com/markets/stocks-usa/market-movers-most-volatile/"
siteinfo = requests.get(url)
    
i = 0
content = siteinfo.content
html = content
parsed_html = BeautifulSoup(html, features="lxml")
badlist = []
goodlist = []
for link in parsed_html.find_all('a'):
    a = link.get('href')
    if "symbol" in str(a) and "-" in str(a):
        if i < 25:
            badlist.append(a)
            i += 1
        else:
            goodlist.append(a)
            i += 1

finallist = []
doneList = []
for z in goodlist:
    x = z.split("-")
    finallist.append(x[1])
for item in finallist:
    y = item.split("/")
    doneList.append(y[0])

stockList = []
stockPrice_total = 0

count = 0
for stock in doneList:
    try:
        count += 1
        quote = get_quote(stock)
        value = quote[stock]['lastPrice']
        stockPrice_total += value
        change = get_quote(stock)
        if value < 3.00 and change[stock]['netChange'] > 0:
            stockList.append(stock)
    except:
        pass

length = len(stockList)
balance = get_cash_balance()
stockDiv = balance[0]['securitiesAccount']['projectedBalances']['cashAvailableForTrading'] / float(length)
realStockAmt = []
stockAmt = []
for stocky in stockList:
    quote1 = get_quote(stocky)
    stockCount = stockDiv / quote1[stocky]['lastPrice']
    stockAmt.append(stockCount)

for thing in stockAmt:
    xy = round(thing)
    realStockAmt.append(xy)

#print(stockList)
#print(realStockAmt)
print("Each stock gets: $" + str(stockDiv))

monkeyCount = 0
for monkey in stockList:
    buy_stock(realStockAmt[monkeyCount], stockList[monkeyCount])
    getQuote = get_quote(stockList[monkeyCount])
    currentPrice = getQuote[stockList[monkeyCount]['lastPrice']]
    print("Order Placed For: " + str(stockList[monkeyCount]) + " Number of Shares Bought: " + str(realStockAmt[monkeyCount]))
    sell_stock(realStockAmt[monkeyCount], stockList[monkeyCount], currentPrice)
    print("Order Placed For: " + str(stockList[monkeyCount]) + " Number of Shares Trailed: " + str(realStockAmt[monkeyCount]))
    monkeyCount += 1

print("----------------------------------------------------------------------------------\nProgram Finished!")