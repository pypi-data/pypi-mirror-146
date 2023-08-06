from valr.account import Account
from valr.exchange_buy_sell import Exchange
from valr.market_data import MarketData
from valr.pay import Pay
from valr.public import Public
from valr.simple_buy_sell import Simple
from valr.wallet import Wallet


class Valr:

    def __init__(self, key: str = None, secret: str = None):
        # Public APIs
        self.public = Public()

        # Authentication Required APIs
        if key and secret:
            self.account = Account(key=key, secret=secret)
            self.wallet = Wallet(key=key, secret=secret)
            self.market_data = MarketData(key=key, secret=secret)
            self.simple = Simple(key=key, secret=secret)
            self.pay = Pay(key=key, secret=secret)
            self.exchange = Exchange(key=key, secret=secret)
