from requests import Session
from urllib.parse import urljoin


class Public(Session):
    """ Public APIs (APIs starting with the prefix /public) do not require authentication. """

    def __init__(self):
        super(Public, self).__init__()
        self.headers.update({
            'cache-control': 'max-age=1000,public'
        })
        self.base_url = 'https://api.valr.com/v1/'

    def order_book(self, currency_pair: str, aggregated: bool = True):
        """
        :param currency_pair: Currency pair for which you want to query the order book, example BTCZAR
        :param aggregated: Aggregates query if False
        :return: Returns a list of the top 40 bids and asks in the order book.
        """
        path = f'public/{currency_pair}/orderbook'
        if not aggregated:
            path += '/full'
        url = urljoin(self.base_url, path)
        return self.get(url)

    def currencies(self):
        """
        :return: List of supported currencies by VALR
        """
        path = 'public/currencies'
        url = urljoin(self.base_url, path)
        return self.get(url)

    def currency_pairs(self):
        """
        :return: Get a list of all the currency pairs supported by VALR.
        """
        path = 'public/pairs'
        url = urljoin(self.base_url, path)
        return self.get(url)

    def order_types(self):
        """
        :return: Get all the order types supported for all currency pairs.
        """
        path = 'public/pairs'
        url = urljoin(self.base_url, path)
        return self.get(url)

    def order_types_currency_pair(self, currency_pair: str):
        """
        :param currency_pair: Currency pair for which you want to query the order book, example BTCZAR
        :return: Get the order types supported for a given currency pair.
        """
        path = f'public/{currency_pair}/ordertypes'
        url = urljoin(self.base_url, path)
        return self.get(url)

    def market_summary(self):
        """
        :return: Get the market summary for all supported currency pairs.
        """
        path = f'public/marketsummary'
        url = urljoin(self.base_url, path)
        return self.get(url)

    def market_summary_currency_pair(self, currency_pair: str):
        """
        :param currency_pair: Currency pair for which you want to query the order book, example BTCZAR
        :return: Get the market summary by supported currency pair.
        """
        path = f'public/{currency_pair}/marketsummary'
        url = urljoin(self.base_url, path)
        return self.get(url)

    def trade_history(self, currency_pair: str, skip: int = 0, limit: int = 10, start_datetime: str = None,
                      end_datetime: str = None, before_id: str = None):
        """
        :param currency_pair: Currency pair for which you want to query the order book, example BTCZAR
        :param skip: Skip number of items from the list
        :param limit: Limit the number of items returned. Max: 100
        :param start_datetime: Include only trades after this ISO 8601 start time
        :param end_datetime: Include only transactions before this ISO 8601 end time
        :param before_id: Only include trades before this ID
        :return: Get the trade history for a given currency pair.
        """
        if limit > 100:
            limit = 100
        path = f'public/{currency_pair}/trades?skip={skip}&limit={limit}'
        if start_datetime:
            path += f'&startTime={start_datetime}'
        if end_datetime:
            path += f'&endTime={end_datetime}'
        if before_id:
            path += f'&beforeId={before_id}'
        url = urljoin(self.base_url, path)
        return self.get(url)

    def server_time(self):
        """
        :return: Get the server time. Please note: The server time is returned in seconds.
        """
        path = 'public/time'
        url = urljoin(self.base_url, path)
        return self.get(url)

    def valr_status(self):
        """
        May be "online" when all functionality is available, or
        "read-only" when only GET and OPTIONS requests are accepted.
         All other requests in read-only mode will respond with a 503 error code.
        :return: Get the current status of VALR.
        """
        path = 'public/status'
        url = urljoin(self.base_url, path)
        return self.get(url)
