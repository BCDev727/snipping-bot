from pyuniswap.pyuniswap import Token
import time
import json
from web3 import Web3
busd = Web3.toChecksumAddress("0xe9e7cea3dedca5984780bafc599bd69add087d56")
f = open('config.json')
data = json.load(f)
PROVIDER = data["provider"]
ADDRESS = data["address"]
PRIVATE_KEY = data["private_key"]
NEW_TOKEN = data["new_token_address"]
TRAILINGSTOP = int(data["trailing_stop"])
sliipage = int(data["slippage"]) / 100
speed = int(data["speed"])
gas_limit = int(data["gas_limit"])
amount = data["amount"] * pow(10,18)
# PROVIDER = 'https://bsc-dataseed1.ninicoin.io'
# BUSD = "0xe9e7cea3dedca5984780bafc599bd69add087d56"
# NEW_TOKEN = BUSD
current_token = Token(NEW_TOKEN, PROVIDER)
current_token.connect_wallet(ADDRESS, PRIVATE_KEY)  # craete token
current_token.set_gaslimit(gas_limit)
print(current_token.is_connected())  # check if the token connected correctlye
buy_price = 0
def buy(amount):  # address:token address.amount:amount for BNB with wei unit
    global buy_price
    global current_token
    buy_flag = False
    while not buy_flag:
        try:
            start_time = time.time()
            result = current_token.buybybusd(int(amount), slippage=sliipage, timeout=2100,
                                                     speed=speed)  # buy token as amount
            print(time.time() -  start_time)
            buy_flag = True
            print(result)
        except Exception as e:
            print(e)
            print("we are waiting liqudity will be add")


def sell():
    global current_token
    balance = current_token.balance()
    sell_flag = False
    while not sell_flag:
        try:
            transaction_addreses = current_token.sellbybusd(balance, slippage=sliipage, timeout=2100,speed=speed)  # sell token as amount
            print("transaction address", transaction_addreses)
            sell_flag = True
        except Exception as e:
            print(e)
def main():
    global buy_price
    balance = current_token.balance()
    confirm_flag = False
    index = 0
    while not confirm_flag:
        print("{}th transaction".format(index + 1))
        if(index > 2):
            print("Please change parameters")
            exit()
        buy(amount)  # buy new token
        time.sleep(10)
        current_balance = current_token.balance()
        if (current_balance > balance):
            confirm_flag = True
        index += 1
    # wait sell moment trailing stop
    buy_price = current_token.price()
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
            exit()
        if buy_price/2 > current_price:
            print("sell with half price")
            sell()
            exit()
        time.sleep(3)


if __name__ == "__main__":
    main()
    # sell()