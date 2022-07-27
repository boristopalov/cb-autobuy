import requests
import base64
import hmac
import hashlib
import json
import products
import os
from dotenv import load_dotenv

load_dotenv()
secret = os.getenv('SECRET').encode('utf-8')
passphrase = os.getenv('PASSPHRASE')
key = os.getenv('KEY')


cb_server_time = requests.get(
    "https://api.coinbase.com/v2/time").json()['data']
timestamp = str(cb_server_time['epoch'])
PRODUCTS = products.products


def search(arr, id):
    for p in arr:
        if p['id'] == id:
            return True
    return False


def getProducts():
    method = "GET"
    requestPath = "/products"
    url = f"https://api.exchange.coinbase.com{requestPath}"
    message = timestamp + method + requestPath + ""
    message = message.encode("UTF-8")
    signature = hmac.new(
        key=base64.b64decode(secret),
        msg=message,
        digestmod=hashlib.sha256
    ).digest()
    signature_b64 = base64.b64encode(signature).decode('utf-8')
    headers = {
        "Accept": "application/json",
        "cb-access-key": key,
        "cb-access-passphrase": passphrase,
        "cb-access-sign": signature_b64,
        "cb-access-timestamp": timestamp
    }
    response = requests.get(url, headers=headers)
    return response.json()


def getProduct(id):
    method = "GET"
    requestPath = f"/products/{id}"
    url = f"https://api.exchange.coinbase.com{requestPath}"
    message = timestamp + method + requestPath + ""
    message = message.encode("UTF-8")
    signature = hmac.new(
        key=base64.b64decode(secret),
        msg=message,
        digestmod=hashlib.sha256
    ).digest()
    signature_b64 = base64.b64encode(signature).decode('utf-8')
    headers = {
        "Accept": "application/json",
        "cb-access-key": key,
        "cb-access-passphrase": passphrase,
        "cb-access-sign": signature_b64,
        "cb-access-timestamp": timestamp
    }
    response = requests.get(url, headers=headers)
    return response.json()


def buyOrder(id, amt):
    method = "POST"
    requestPath = "/orders"
    url = f"https://api.exchange.coinbase.com{requestPath}"
    body = {
        "side": "buy",
        "product_id": id,
        "type": "market",
        "stp": "dc",
        "time_in_force": "GTC",
        "funds": amt,
        "post_only": "false",
        "cancel_after": "hour"
    }
    message = timestamp + method + requestPath + json.dumps(body)
    message = message.encode("UTF-8")

    signature = hmac.new(
        key=base64.b64decode(secret),
        msg=message,
        digestmod=hashlib.sha256
    ).digest()
    signature_b64 = base64.b64encode(signature).decode('utf-8')
    headers = {
        "Accept": "application/json",
        "cb-access-key": key,
        "cb-access-passphrase": passphrase,
        "cb-access-sign": signature_b64,
        "cb-access-timestamp": timestamp
    }
    response = requests.post(url, headers=headers, json=body)
    return response.json()


def main():
    buyRes = buyOrder("ETH-USD", 10)
    print(buyRes)
    # method = "GET"
    # requestPath = "/accounts"
    # url = f"https://api.exchange.coinbase.com{requestPath}"
    # message = timestamp + method + requestPath + ""
    # message = message.encode("UTF-8")
    # signature = hmac.new(
    #     key=base64.b64decode(secret),
    #     msg=message,
    #     digestmod=hashlib.sha256
    # ).digest()
    # signature_b64 = base64.b64encode(signature).decode('utf-8')
    # headers = {
    #     "Accept": "application/json",
    #     "cb-access-key": key,
    #     "cb-access-passphrase": passphrase,
    #     "cb-access-sign": signature_b64,
    #     "cb-access-timestamp": timestamp
    # }
    # response = requests.get(url, headers=headers)
    # print(response.json())
    # return


if __name__ == "__main__":
    main()
