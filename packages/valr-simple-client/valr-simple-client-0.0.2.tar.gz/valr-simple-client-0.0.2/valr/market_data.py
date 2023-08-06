from valr.session import ValrAPISession


class MarketData(ValrAPISession):
    """ These API calls can be used to receive the market data. """

    def order_book(self, currency_pair: str, aggregated: bool = False):
        """
        :param currency_pair: Currency pair for which you want to query the order book, example: BTCZAR
        :param aggregated: orders of the same price are NOT aggregated if set to True
        :return: Returns a list of the top 40 bids and asks in the order book
        """
        path = f'marketdata/{currency_pair}/orderbook'
        if aggregated:
            path += '/full'
        return self.get(path=path)

    def trade_history(
            self,
            currency_pair: str, skip: int = 0, limit: int = 100,
            start_datetime: str = None, end_datetime: str = None,
            before_id: str = None
    ):
        """
        :param currency_pair: Currency pair for which you want to query the order book, example: BTCZAR
        :param skip: Skip number of items from the list
        :param limit: Limit the number of items returned. Max 100
        :param start_datetime: Include only trades after this ISO 8601 start time.
        :param end_datetime: Include only transactions before this ISO 8601 end time.
        :param before_id: Only include trades before this ID.
        :return: Get the last 100 recent trades for a given currency pair. Optional filtering/pagination
        """
        if limit > 100:
            limit = 100
        path = f'marketdata/{currency_pair}/tradehistory?skip={skip}&limit={limit}'
        if start_datetime:
            path += f'&startTime={start_datetime}'
        if end_datetime:
            path += f'&endTime={end_datetime}'
        if before_id:
            path += f'&beforeId={before_id}'
        return self.get(path=path)
