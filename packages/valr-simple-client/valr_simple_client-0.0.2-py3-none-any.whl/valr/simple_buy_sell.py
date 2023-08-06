from valr.session import ValrAPISession


class Simple(ValrAPISession):

    def quote(self, currency_pair: str, pay_in_currency: str, pay_amount: float, side: str):
        """
        :param currency_pair: Currency pair to get a simple quote for.
            Any currency pair that supports the "simple" order type, can be specified.
        :param pay_in_currency: currency to pay in, examples BTC, ETH
        :param pay_amount: Amount as float
        :param side: only accepts SELL or BUY side
        :return: Get a quote to buy or sell instantly using Simple Buy.
        """
        if side not in ['BUY', 'SELL']:
            return False
        data = {
            "payInCurrency": pay_in_currency,
            "payAmount": pay_amount,
            "side": side
        }
        return self.post(path=f'simple/{currency_pair}/quote', data=data)

    def order(self, currency_pair: str, pay_in_currency: str, pay_amount: float, side: str):
        """
        Submit an order to buy or sell instantly using Simple Buy/Sell.

        :param currency_pair: Currency pair to get a simple quote for.
            Any currency pair that supports the "simple" order type, can be specified.
        :param pay_in_currency: currency to pay in, examples BTC, ETH
        :param pay_amount: Amount as float
        :param side: only accepts SELL or BUY side
        :return:
        """
        if side not in ['BUY', 'SELL']:
            return False
        data = {
            "payInCurrency": pay_in_currency,
            "payAmount": pay_amount,
            "side": side
        }
        return self.post(path=f'simple/{currency_pair}/quote', data=data)

    def order_status(self, currency_pair: str, order_id: str):
        """
        :param currency_pair: Currency pair you want a simple buy/sell quote for.
        :param order_id: Order Id of the order for which you are querying the status.
        :return:
        """
        return self.get(path=f'simple/{currency_pair}/order/{order_id}')
