from pyuniswap.pyuniswap import Token
import time
import json
from web3 import Web3
from datetime import datetime
import threading
import os
f = open('config.json')
data = json.load(f)
PROVIDER = data["provider"]
ADDRESS = data["address"]
PRIVATE_KEY = data["private_key"]
TRAILINGSTOP = int(data["trailing_stop"])
NEW_TOKEN = data["new_token_address"]
sliipage = int(data["slippage"]) / 100
speed = int(data["speed"])
gas_limit = int(data["gas_limit"])
amount = data["amount"] * pow(10, 18)
w3 = Web3(Web3.HTTPProvider(PROVIDER))
current_token = Token(NEW_TOKEN, PROVIDER)
current_token.connect_wallet(ADDRESS, PRIVATE_KEY)  # craete token
current_token.set_gaslimit(gas_limit)
print(current_token.is_connected())  # check if the token connected correctlye
try:
    if(current_token.price() > 0):
        print("This token launched")
        os._exit(1)
except:
    pass
buy_price = 0
find_token_flag = False
class EventTread(threading.Thread):
    def __init__(self, event):
        threading.Thread.__init__(self)
        self.event = event
    def handle_event(self,event):
        try:
            tx = w3.toHex(event)
            transaction = w3.eth.getTransaction(tx)
            transaction_input = transaction.input
            transaction_method = transaction_input[:10]
            # if (transaction_method == "0xe8e33700"):
            if transaction_method == "0xf305d719" or transaction_method == '0xe8e33700':
                address = transaction_input[34:74]
                address = "0x" + address
                if(address.lower() == NEW_TOKEN.lower()):
                    print("This is liquidity : {}".format(tx))
                    act()
                return True
            else:
                return False
        except:
            pass
    def run(self) -> None:
        self.handle_event(self.event)
def log_loop(event_filter):
    while True:
        for event in event_filter.get_new_entries():
            thread = EventTread(event)
            thread.start()
        if(not find_token_flag):
            print("{} :we are waiting liqudity will be add".format(datetime.utcnow()))

def buy(amount):  # address:token address.amount:amount for BNB with wei unit
    global buy_price
    global current_token
    buy_flag = False
    while not buy_flag:
        try:
            print(datetime.utcnow())
            start_time = time.time()
            result = current_token.buy(int(amount), slippage=sliipage, timeout=2100,
                                       speed=speed)  # buy token as amount
            print(time.time() - start_time)
            buy_flag = True
            print("Buy token: ",result)
        except Exception as e:
            print(e)
            print("{} :we are waiting liqudity will be add".format(datetime.utcnow()))


def sell():
    global current_token
    balance = current_token.balance()
    sell_flag = False
    while not sell_flag:
        try:
            transaction_addreses = current_token.sell(balance, slippage=sliipage, timeout=2100,
                                                      speed=speed)  # sell token as amount
            print("Sell transaction address", transaction_addreses)
            sell_flag = True
        except Exception as e:
            print(e)
def act():
    global buy_price
    global find_token_flag
    find_token_flag = True
    balance = current_token.balance()
    confirm_flag = False
    index = 0
    while not confirm_flag:
        if(index > 2):
            print("Please change parameters")
            os._exit(1)
        buy(amount)  # buy new token\
        buy_price = current_token.price()
        time.sleep(1)
        current_balance = current_token.balance()
        if (current_balance > balance):
            confirm_flag = True
        index += 1
    # wait sell moment trailing stop
    trailing_stop = buy_price * (100 - TRAILINGSTOP) / 100
    print ("Trailing stop",trailing_stop)
    print("Buy price", buy_price)
    while True:
        current_price = current_token.price()
        current_trailing_stop = current_price * (100 - TRAILINGSTOP) / 100
        print("Trailing stop", current_trailing_stop)
        if current_trailing_stop > trailing_stop:
            trailing_stop = current_trailing_stop
            print("We are waiting sell moment")
        elif current_price > trailing_stop:
            pass
            print("We are waiting sell moment")
        else:
            sell()
            os._exit(1)
        if buy_price/2 > current_price:
            print("sell with half price")
            sell()
            os._exit(1)
        time.sleep(1)

def main():
    block_filter = w3.eth.filter("latest")
    log_loop(block_filter)

if __name__ == '__main__':
    main()

