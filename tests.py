import sys, getopt, time, math, os
from datetime import datetime
import json
from binance.client import Client
from binance.enums import *

# Add your Binance api key and secret!

api_key = "8V01KyzR2dKpvkTD1mloNRCcSyL7s4wP56EPvcxbHN1jlvp2P3YTBLuJZIw27G7t"
api_secret = "AQ5aGGGg14payTYrVA5nYdnlD6CIW1i1cpcWWUG34MwpGBlrsHcVx7RtwOSURHEY"

client = Client(api_key, api_secret, testnet=False)

orders = client.get_all_orders(symbol="ETHBTC")
print(json.dumps(orders, indent=4, sort_keys=True))
print(orders[len(orders)-1]['price'])
