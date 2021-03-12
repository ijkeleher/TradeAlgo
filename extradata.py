import requests, json
from bs4 import BeautifulSoup
import yfinance as yf


def getFloat(symbol):
    url = "https://www.marketwatch.com/investing/stock"

    updatedurl = f"{url}/{symbol}?mod=quote_search"
    quote = requests.get(updatedurl)
    soup = BeautifulSoup(quote.content, 'html.parser')
    list_tags = soup.find_all(class_="primary")
    final = str(list_tags[21])
    final = final.split('<span class="primary">')
    final = final[1].split("</span>")
    final = final[0]
    if "M" in final:
        final = final.split("M")
        final = final[0]
        final = float(final) * 10**6
        final = str(final)
    elif "B" in final:
        final = final.split("B")
        final = final[0]
        final = float(final) * 10**9
        final = str(final)
    elif "K" in final:
        final = final.split("K")
        final = final[0]
        final = float(final) * 10**3
        final = str(final)

    return final

#print(getFloat("ATOS"))

def getVolume(symbol):
    key = "ce4e7efb80a707ca2b1edcec4ed54ffd"
    url = "https://financialmodelingprep.com"
    endpoint = f"{url}/api/v3/quote/{symbol}?apikey={key}"

    data = requests.get(endpoint).json()

    return data[0]['avgVolume']

#print(json.dumps(getVolume("AAPL"), indent = 4))

def get15(symbol):

    data = yf.download(tickers=symbol, period="1d", interval = "15m")
    
    return data.tail()


#print(get15("CCIV"))