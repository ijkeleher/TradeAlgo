import time
import urllib
import requests
from splinter import Browser
from bs4 import BeautifulSoup
from lowHigh import get_quote, get_cash_balance, buy_stock, place_saved_order, sell_stock
#from stocklist import stockList, realStockAmt

i = 0
for stock in stockList:
    quote = get_quote(stock)
    if quote[stock]['netChange'] < 0:
        sell_stock(realStockAmt[i], stock)
        print(stock + " sold!")
        i += 1
    print("hello")