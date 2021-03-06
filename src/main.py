import requests
import json
from pprint import pprint
from bs4 import BeautifulSoup
import re
import os
import threading


# Returns GET request response from url
def get_info(call):
    r = requests.get(call)
    return r.json()


# Returns all Bazaar data
def get_bazaar_data():
    return get_info("https://api.hypixel.net/skyblock/bazaar")


# Returns total coin counts in buy orders on the bazaar
def get_bazaar_buy_order_value(bazaar_data):
    sum_coins = 0
    price_increase_threshold = 1.2

    # For every product
    for item_name, item_data in bazaar_data.get("products", {}).items():

        item_sum_coins = 0

        # For every buy order
        for idx, buy_order in enumerate(item_data.get("buy_summary", [])):

            # If it's the best price
            if idx == 0:
                item_expected_value = buy_order.get("pricePerUnit", 0)
                item_sum_coins += buy_order.get("amount", 0) * buy_order.get(
                    "pricePerUnit", 0
                )

            # If it's not the best price, check for reasonable price
            else:
                if buy_order.get("pricePerUnit", 0) < (
                    item_expected_value * price_increase_threshold
                ):
                    item_sum_coins += buy_order.get("amount", 0) * buy_order.get(
                        "pricePerUnit", 0
                    )

        print(f"{item_name} | {round(item_sum_coins)}")
        sum_coins += item_sum_coins

    return sum_coins


# API_KEY.json is not in GitHub repo
API_FILE = open("../API_KEY.json", "r")
API_KEY = json.loads(API_FILE.read())["API_KEY"]

pprint(get_bazaar_buy_order_value(get_bazaar_data()))
