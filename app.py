import json, config
from flask import Flask, request, jsonify, render_template
from binance.client import Client
from binance.enums import *

app = Flask(__name__)

client = Client(config.API_KEY, config.API_SECRET)
#order_price
def order(side, quantity, symbol, order_type=FUTURE_ORDER_TYPE_MARKET):
    try:
        #{order_price}
        print(f"sending order {order_type} - {side} {quantity} {symbol}")
        #price=order_price, timeInForce='GTC'
        order = client.futures_create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False

    return order

@app.route("/")
def welcome():
    return render_template('index.html')

@app.route("/webhook", methods=['POST'])
def webhook():
    #print(request.data)
    data = json.loads(request.data)

    if data['passphrase'] != config.WEBHOOK_PASSPHRASE:
        return {
            "code": "error",
            "message": "Nice try, invalid passphrase"
        }
    print(data['ticker'])
    print(data['bar'])

    side = data['strategy']['order_action'].upper()
    quantity = data['strategy']['order_contracts']
    #price = data['strategy']['order_price'] 
    order_response = order(side, quantity, "ETHUSDT")#price,
    
    if order_response:
        return {
            "code": "success",
            "message": "order executed"
        }
    else:
        print("order failed")

        return {
            "code": "error",
            "message": "order failed"
        }