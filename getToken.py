import time
import urllib
import requests
import json
from splinter import Browser
from config import key, password, user_id, account_number

executeable_path = {'executable_path': r'/home/simple/Desktop/TradingAlgorithms/chromedriver'}

browser = Browser("chrome", **executeable_path, headless = False)

method = "GET"
url = "https://auth.tdameritrade.com/auth?"
client_code = key + "@AMER.OAUTHAP"
payload = {
    'response_type': 'code',
    'redirect_uri': "http://localhost",
    'client_id': client_code
}

built_url = requests.Request(method, url, params = payload).prepare()
built_url = built_url.url

browser.visit(built_url)

payload = {
    'username': user_id,
    'password': password
}

browser.find_by_id("username0").first.fill(payload["username"])
browser.find_by_id("password1").first.fill(payload["password"])
browser.find_by_id("accept").first.click()

browser.find_by_id("accept").first.click()
time.sleep(1)

browser.find_by_text('Can\'t get the text message?').first.click()

# Get the Answer Box
browser.find_by_value("Answer a security question").first.click()

# Answer the Security Questions.
if browser.is_text_present('What is your paternal grandmother\'s first name?'):
    browser.find_by_id("secretquestion0").first.click()
    browser.find_by_id('secretquestion0').first.fill('alwar')

elif browser.is_text_present('What is your father\'s middle name?'):
    browser.find_by_id("secretquestion0").first.click()
    browser.find_by_id('secretquestion0').first.fill('babu')

elif browser.is_text_present('What was your high school mascot?'):
    browser.find_by_id("secretquestion0").first.click()
    browser.find_by_id('secretquestion0').first.fill('viking')

elif browser.is_text_present('What was the name of your junior high school? (Enter only \'Dell\' for Dell Junior High School.)'):
    browser.find_by_id("secretquestion0").first.click()
    browser.find_by_id('secretquestion0').first.fill('miller')

# Submit results
browser.find_by_id('accept').first.click()

#Trust this device
browser.find_by_xpath('/html/body/form/main/fieldset/div/div[1]/label').first.click()
browser.find_by_id('accept').first.click()
browser.find_by_id('accept').first.click()

new_url = browser.url

parse_url = urllib.parse.unquote(new_url.split("code=")[1])

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
#print(authreply)
#print(json.dumps(authreply, indent = 4))

access_token = authreply['access_token']
#print(access_token)

browser.quit
