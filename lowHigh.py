import requests
from config import key, password, user_id, account_number, refresh_token
import json

def get_price_history(symbol):
    symbol = str(symbol)
    url = f"https://api.tdameritrade.com/v1/marketdata/{symbol}/pricehistory"

    payload = {
        'apikey': key,
        'periodType': 'day',
        'frequencyType': 'minute',
        'frequency': '1',
        'period': '1'
    }

    history =  requests.get(url, params=payload).json()

    return history

#print(get_price_history("CTRM"))


def get_quote(symbol):
    symbol = str(symbol)
    url = f"https://api.tdameritrade.com/v1/marketdata/{symbol}/quotes"

    payload = {
        'apikey': key,
    }

    quote = requests.get(url, params=payload).json()

    return quote

#print(get_quote("OEG"))

def get_quotes():
    url = f"https://api.tdameritrade.com/v1/marketdata/quotes"

    payload = {
        'apikey': key,
        'symbol': 'HOTH,SGRP,PED,TGC,CHEK,HSTO,OEG,NTN,RCON,AVGR,ASRT,DVD'
    }

    quotes = requests.get(url, params=payload).json()

    return quotes

#print(get_quotes())

'''
def get_access_token():
    url = "https://api.tdameritrade.com/v1/oauth2/token"

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    payload = {
        'grant_type': 'authorization_code',
        'access_type': 'offline',
        'code': parse_url,
        'client_id': key,
        'redirect_uri': 'http://localhost'
    }

    authreply = requests.post(url, headers = headers, data = payload).json()

    return authreply

print(get_access_token())
'''

def get_total_balance():
    from getToken import access_token
    bearer_key = "Bearer " + access_token
    url = "https://api.tdameritrade.com/v1/accounts"

    headers = {
        'Authorization': bearer_key
    }

    balance = requests.get(url, headers = headers).json()

    return balance

#account_stats = get_total_balance()
#print("Account Value: $" + str(account_stats[0]['securitiesAccount']['currentBalances']['liquidationValue']))

def get_cash_balance():
    from getToken import access_token
    bearer_key = "Bearer " + access_token
    url = "https://api.tdameritrade.com/v1/accounts"

    headers = {
        'Authorization': bearer_key
    }

    balance = requests.get(url, headers = headers).json()

    return balance

#account_stats = get_cash_balance()
#print("Amount Ready To Trade: $" + str(account_stats[0]['securitiesAccount']['projectedBalances']['cashAvailableForTrading']))

def buy_stock(number_to_buy, symbol):
    from getToken import access_token
    symbol = str(symbol)
    bearer_key = "Bearer " + access_token
    url = f"https://api.tdameritrade.com/v1/accounts/{account_number}/orders"

    headers = {
        'Authorization': bearer_key,
        'Content-Type': 'application/json'
    }

    payload = {
        'orderType': 'MARKET',
        'session': 'NORMAL',
        'duration': 'DAY',
        'orderStrategyType': 'SINGLE',
        'orderLegCollection': [
            {
                'instruction': 'BUY',
                'quantity': number_to_buy,
                'instrument': {
                    'symbol': symbol,
                    'assetType': "EQUITY"
                }
            }
        ]
    }

    send_order = requests.post(url, json = payload, headers = headers)
    
    if send_order.status_code == 200:
        print("Order Placed!")
    else:
        print("Order Failed!")

'''def trail_stock(number_to_sell, symbol):
    from getToken import access_token
    symbol = str(symbol)
    bearer_key = "Bearer " + access_token
    url = f"https://api.tdameritrade.com/v1/accounts/{account_number}/orders"

    headers = {
        'Authorization': bearer_key,
        'Content-Type': 'application/json'
    }

    payload = {
        "complexOrderStrategyType": "NONE",
        "orderType": "TRAILING_STOP",
        "session": "NORMAL",
        "stopPriceLinkBasis": "BID",
        "stopPriceLinkType": "VALUE",
        "stopPriceOffset": 0.10,
        'duration': 'DAY',
        'orderStrategyType': 'SINGLE',
        'orderLegCollection': [
            {
                'instruction': 'SELL',
                'quantity': number_to_sell,
                'instrument': {
                    'symbol': symbol,
                    'assetType': "EQUITY"
                }
            }
        ]
    }

    send_order = requests.post(url, json = payload, headers = headers)
    
    if send_order.status_code == 200:
        print("Order Placed!")
    else:
        print("Order Failed!")

trail_stock("ASRT", 16)
'''

def sell_stock(number_to_sell, symbol, price):
    from getToken import access_token
    symbol = str(symbol)
    bearer_key = "Bearer " + access_token
    url = f"https://api.tdameritrade.com/v1/accounts/{account_number}/orders"

    headers = {
        'Authorization': bearer_key,
        'Content-Type': 'application/json'
    }

    payload = {
        "complexOrderStrategyType": "NONE",
        'orderType': 'TRAILING_STOP',
        'session': 'NORMAL',
        "stopPriceLinkBasis": "BID",
        "stopPriceLinkType": "VALUE",
        "stopPriceOffset": price - 0.10,
        'duration': 'DAY',
        'orderStrategyType': 'SINGLE',
        'orderLegCollection': [
            {
                'instruction': 'SELL',
                'quantity': number_to_sell,
                'instrument': {
                    'symbol': symbol,
                    'assetType': "EQUITY"
                }
            }
        ]
    }

    send_order = requests.post(url, json = payload, headers = headers)
    
    if send_order.status_code == 200:
        print("Order Placed!")
    else:
        print("Order Failed!")

#sell_stock(13, "AVGR")

def place_saved_order(number_to_buy, symbol, typeof):
    from getToken import access_token
    symbol = str(symbol)
    typeof = str(typeof)
    bearer_key = "Bearer " + access_token
    url = f"https://api.tdameritrade.com/v1/accounts/{account_number}/savedorders"

    headers = {
        'Authorization': bearer_key,
        'Content-Type': 'application/json'
    }

    payload = {
        'orderType': 'MARKET',
        'session': 'NORMAL',
        'duration': 'DAY',
        'orderStrategyType': 'SINGLE',
        'orderLegCollection': [
            {
                'instruction': typeof,
                'quantity': number_to_buy,
                'instrument': {
                    'symbol': symbol,
                    'assetType': "EQUITY"
                }
            }
        ]
    }

    send_order = requests.post(url, json = payload, headers = headers)
    
    if send_order.status_code == 200:
        print("Order Placed!")
    else:
        print("Order Failed!")

#place_saved_order(1, "AAPL", "Buy")

def query_saved_order():
    from getToken import access_token
    bearer_key = "Bearer " + access_token
    url = f"https://api.tdameritrade.com/v1/accounts/{account_number}/savedorders"

    headers = {
        'Authorization': bearer_key,
    }

    send_query = requests.get(url, headers = headers).json()

    return send_query

#print(query_saved_order())
def get_share_balance():
    from getToken import access_token
    bearer_key = "Bearer " + access_token
    url = "https://api.tdameritrade.com/v1/accounts"

    payload = {
        'fields': "positions"
    }

    headers = {
        'Authorization': bearer_key
    }

    balance = requests.get(url, params = payload, headers = headers).json()

    return balance

while True:
    stock_stats = get_share_balance()
    #print(json.dumps(stock_stats, indent = 4))
    i = 0
    for stock in stock_stats[0]['securitiesAccount']['positions']:
        stock_sym = str(stock_stats[0]['securitiesAccount']['positions'][i]['instrument']['symbol'])
        num_to_sell = str(stock_stats[0]['securitiesAccount']['positions'][i]['longQuantity'])
        quote = get_quote(stock_sym)
        if quote[stock_sym]['netChange'] < 0:
            sell_stock(num_to_sell, stock_sym)
            print(stock_sym + " sold!")
        i += 1
