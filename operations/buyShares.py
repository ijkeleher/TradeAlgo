import sys, os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time
import requests
from bs4 import BeautifulSoup
from getData.brokerfunc import get_quote, get_cash_balance, buy_stock, sell_stock, getFloat, getVolume
from getData.getToken import getaccess
import schedule
    
print("\x1b[8;50;115t")
    
print('''
 $$$$$$\              $$\                $$$$$$\    $$\                         $$\       
$$  __$$\             $$ |              $$  __$$\   $$ |                        $$ |      
$$ /  $$ |$$\   $$\ $$$$$$\    $$$$$$\  $$ /  \__|$$$$$$\    $$$$$$\   $$$$$$$\ $$ |  $$\ 
$$$$$$$$ |$$ |  $$ |\_$$  _|  $$  __$$\ \$$$$$$\  \_$$  _|  $$  __$$\ $$  _____|$$ | $$  |
$$  __$$ |$$ |  $$ |  $$ |    $$ /  $$ | \____$$\   $$ |    $$ /  $$ |$$ /      $$$$$$  / 
$$ |  $$ |$$ |  $$ |  $$ |$$\ $$ |  $$ |$$\   $$ |  $$ |$$\ $$ |  $$ |$$ |      $$  _$$<  
$$ |  $$ |\$$$$$$  |  \$$$$  |\$$$$$$  |\$$$$$$  |  \$$$$  |\$$$$$$  |\$$$$$$$\ $$ | \$$\ 
\__|  \__| \______/    \____/  \______/  \______/    \____/  \______/  \_______|\__|  \__|
'''
)

STARTTIME = "07:14"
TOKENTIME = "07:05"
print(f"EXECUTING @ {STARTTIME}")

def buy():
    start = time.time()
    print("Starting...")
    url = "https://www.tradingview.com/markets/stocks-usa/market-movers-gainers/"
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

    doneList = []
    for z in goodlist:
        x = z.split("-")
        y = x[1].split("/")
        doneList.append(y[0])

    stockList = []

    for stock in doneList:
        try: #there are mischars in the stocks!
            quote = get_quote(stock)
            if quote[stock]['closePrice'] < 5.00 and quote[stock]['netChange'] >= 0.2 and quote[stock]['openPrice'] < quote[stock]['lastPrice'] and getVolume(stock) > 1000000 and float(getFloat(stock)) < 100000000.0:
                stockList.append(stock)
        except:
            pass

    length = len(stockList)
    balance = get_cash_balance()
    stockDiv = balance[0]['securitiesAccount']['projectedBalances']['cashAvailableForTrading'] / float(length)
    
    realStockAmt = []

    for stocky in stockList:
        quote1 = get_quote(stocky)
        stockCount = stockDiv / quote1[str(stocky)]['lastPrice']
        realStockAmt.append(round(stockCount))

    monkeyCount = 0
    for monkey in stockList:
        buy_stock(realStockAmt[monkeyCount], stockList[monkeyCount])
        print("Order Placed For: " + str(stockList[monkeyCount]) + " Number of Shares Bought: " + str(realStockAmt[monkeyCount]))
        sell_stock(realStockAmt[monkeyCount], stockList[monkeyCount])
        print("Order Placed For: " + str(stockList[monkeyCount]) + " Number of Shares Trailed: " + str(realStockAmt[monkeyCount]))
        monkeyCount += 1

    print("----------------------------------------------------------------------------------\nProgram Finished!")

schedule.every().day.at(TOKENTIME).do(getaccess)
schedule.every().day.at(STARTTIME).do(buy)

while True:
    schedule.run_pending()
    time.sleep(1)