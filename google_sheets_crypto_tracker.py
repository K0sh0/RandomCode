from lxml import html
import bs4 
import requests
import time
import json
import re
import gspread

# Load the google spreadsheet
gs = gspread.service_account(filename='credentials.json')
sh = gs.open_by_key('1C0IDZGyJo_PnXaBy-6nnF_yKLpAWV4TjzfpyyXpxh3w')
worksheet = sh.sheet1

# Fetch the HTML content from the webpage
url = "https://www.coingecko.com/en"
response = requests.get(url)
html_content = bs4.BeautifulSoup(response.text, features="lxml")

def get_price(coin):
    """Function to fetch the price of a given coin from https://www.coingecko.com/en"""
    # Search for the HTML span tag containing the coin price
    coin_span = html_content.find('span', {'data-coin-symbol':coin})
    
    # Convert the parsed span element to string
    coin_price_string = str(coin_span)
    
    # Split the string by 'price.price' and extract the price from the string
    coin_price = coin_price_string.split('price.price')[1][3:-7]
    return coin_price

def update_spreadsheet(row, price):
    """Function to update the given row in the Google Sheets worksheet with fetched price"""
    worksheet.update_cell(row,10, price)

# Define a list of coins and corresponding rows
coins = {'ada': 3, 'btc': 4, 'xrp': 5, 'eth': 6, 'doge': 7}

# Fetch each coin price and update the corresponding cell in the spreadsheet
for coin, row in coins.items():
    coin_price = get_price(coin)
    update_spreadsheet(row, coin_price)

print('Updated')
