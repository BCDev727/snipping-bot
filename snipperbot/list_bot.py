from pyuniswap.pyuniswap import Token
import time
import json
import hashlib
import datetime
def check_key (adress,key):
    public_key = "genius".format(adress)
    secret_key = hashlib.sha224(public_key.encode()).hexdigest()
    if secret_key == key:
        return True
    else:
        return False
if datetime.date(2021, 5, 30) > datetime.date.today():
    print("this is the test version")
    exit()
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
PROVIDER = 'https://late-bold-sound.bsc.quiknode.pro/1a8adf11a5744e16fc2edae4afae1529e6f7dfe2/'
BUSD = "0xe9e7cea3dedca5984780bafc599bd69add087d56"
NEW_TOKEN = BUSD

current_token = Token(NEW_TOKEN, PROVIDER)
current_token.connect_wallet(ADDRESS, PRIVATE_KEY)  # craete token
current_token.set_gaslimit(gas_limit)
print(current_token.is_connected())  # check if the token connected correctlye
buy_price = 0

def buy(amount):  # address:token address.amount:amount for BNB with wei unit
    global buy_price
    global current_token
    result = current_token.buy(int(amount), slippage=sliipage, timeout=2100,
                                             speed=speed)  # buy token as amount
    print(result)

def sell():
    global current_token
    balance = current_token.balance()
    sell_flag = False
    while not sell_flag:
        try:
            transaction_addreses = current_token.sellbywbnb(balance, slippage=sliipage, timeout=2100,speed=speed)  # sell token as amount
            print("transaction address", transaction_addreses)
            sell_flag = True
        except Exception as e:
            print(e)

def main():
    global buy_price
    balance = current_token.balance()
    confirm_flag = False
    index = 0
    buy(amount)  # buy new token
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