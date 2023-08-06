from valr.session import ValrAPISession


class Exchange(ValrAPISession):
    """ Make use of our powerful Exchange Buy/Sell APIs to place your orders on the Exchange programmatically. """

    batch_orders = []

    def limit_order(
            self,
            side: str, quantity: float, price: float, pair: str,
            time_in_force: str = 'GTC', post_only: bool = False, custom_order_id: int = None
    ):
        """
        :param side: BUY or SELL
        :param quantity: Base amount
        :param price: Price per coin in ZAR
        :param pair: Can be BTCZAR, ETHZAR or XRPZAR
        :param custom_order_id: Use own order ID specified by client (Optional numeric value)
        :param time_in_force: Can be GTC, FOK or IOC. Default value is GTC
        :param post_only: Place a Maker order and cause it to fail, if matched immediately, if it's True (default False)
        :return:
        """
        data = {
            "side": side,
            "quantity": quantity,
            "price": price,
            "pair": pair,
            "postOnly": post_only,
            "timeInForce": time_in_force
        }
        if custom_order_id:
            data.update({'customerOrderId': custom_order_id})
        return self.post(path='orders/limit', data=data)

    def market_order(self, side: str, amount: float, pair: str, customer_order_id: int = None):
        """
        :param side: BUY or SELL
        :param amount: baseAmount if side is BUY else quoteAmount if side is SELL
        :param pair: Can be BTCZAR, ETHZAR or XRPZAR
        :param customer_order_id: Use own order ID specified by client (Optional numeric value)
        :return: 202 Accepted if successful
        """
        if side not in ['BUY', 'SELL']:
            return False
        if pair not in ['BTCZAR', 'ETHZAR', 'XRPZAR']:
            return False
        data = {
            "side": side,
            "baseAmount" if side == 'BUY' else "quoteAmount": amount,
            "pair": pair
        }
        if customer_order_id:
            data.update({'customerOrderId': customer_order_id})
        return self.post(path='orders/market', data=data)

    def stop_limit_order(
            self, side: str, quantity: float, price: float, pair: str, stop_price: float, limit_type: str,
            customer_order_id: int = None, time_in_force: str = 'GTC',
    ):
        """
        :param side: BUY or SELL
        :param quantity: Amount in Base Currency must be provided.
        :param price: The Limit Price at which the BUY or SELL order will be placed .
        :param pair: Can be BTCZAR, ETHZAR or XRPZAR.
        :param stop_price: The target price for the trade to trigger. Cannot be equal to last traded price.
        :param limit_type: Can be TAKE_PROFIT_LIMIT or STOP_LOSS_LIMIT.
        :param customer_order_id: Use own order ID specified by client (Optional numeric value)
        :param time_in_force: Can be GTC, FOK or IOC. Default value is GTC
        :return:
        """
        data = {
            "side": side,
            "quantity": quantity,
            "price": price,
            "pair": pair,
            "timeInForce": time_in_force,
            "stopPrice": stop_price,
            "type": limit_type
        }
        if customer_order_id:
            data.update({'customerOrderId': customer_order_id})
        return self.post(path='orders/stop/limit', data=data)

    def append_order_to_batch(
            self,
            order_type: str, pair: str, side: str, quantity: str, price: float,
            time_in_force: str = 'GTC', customer_order_id: int = None
    ):
        """

        :param order_type: Can be PLACE_MARKET, PLACE_LIMIT, PLACE_STOP_LIMIT or CANCEL_ORDER
        :param pair: Can be BTCZAR, ETHZAR or XRPZAR.
        :param side: BUY or SELL
        :param quantity: Amount in Base Currency must be provided.
        :param price: The Limit Price at which the BUY or SELL order will be placed .
        :param time_in_force: Can be GTC, FOK or IOC. Default value is GTC
        :return:
        """
        # check if customer order id already exists in batch order (Needs to be unique in batch)
        if customer_order_id:
            for order in self.batch_orders:
                if order.get('customerOrderId', None) == customer_order_id:
                    return False
        # add to batch orders
        self.batch_orders.append({
            "type": order_type,
            "data": {
                "pair": pair,
                "side": side,
                "quantity": quantity,
                "price": price,
                "timeInForce": time_in_force
            }
        })
        return True

    def execute_batch_orders(self):
        """
        Create a batch of multiple orders, or cancel orders, in a single request
        """
        if not self.batch_orders:
            return False

        data = {
            'requests': self.batch_orders
        }

        response = self.post(path='orders/batch', data=data)

        # clear batch orders and avoid possible duplication of orders
        self.batch_orders = []

        return response

    def order_status(self, currency_pair: str, order_id: str = None, customer_order_id: str = None):
        """
        Requires either order_id or customer_order_id to query order status

        :param currency_pair: Currency pair, example BTCZAR
        :param order_id: Order Id provided by VALR
        :param customer_order_id: Order Id provided by customer when creating the order
        """
        if order_id:
            return self.get(path=f'orders/{currency_pair}/orderid/{order_id}')
        elif customer_order_id:
            return self.get(path=f'orders/{currency_pair}/customerorderid/{customer_order_id}')
        return False

    def open_orders(self):
        """
        Get all open orders for your account.
        :return: A customerOrderId field will be returned in the response for all those orders that were created with
        a customerOrderId field.
        """
        return self.get(path='orders/open')

    def order_history(self, skip: int = 0, limit: int = 1):
        """
        :param skip: Skip number of items from the list.
        :param limit: Limit the number of items returned.
        :return: Get historical orders placed by you.

        """
        if limit > 2:
            limit = 2
        return self.get(path=f'orders/history?skip={skip}&limit={limit}')

    def order_history_summary(self, order_id: str = None, customer_order_id: str = None):
        """
        Requires either order_id or customer_order_id to query order status

        :param order_id: Order ID provided by VALR
        :param customer_order_id: Order ID provided by customer when creating the order
        :return: Get history summary of order
        """
        if order_id:
            return self.get(path=f'orders/history/summary/orderid/{order_id}')
        elif customer_order_id:
            return self.get(path=f'orders/history/summary/customerorderid/{customer_order_id}')
        return False

    def order_history_detail(self, order_id: str = None, customer_order_id: str = None):
        """
        Requires either order_id or customer_order_id to query order status

        :param order_id: Order ID provided by VALR
        :param customer_order_id: Order ID provided by customer when creating the order
        :return: Get detail history summary of order
        """
        if order_id:
            return self.get(path=f'orders/history/detail/orderid/{order_id}')
        elif customer_order_id:
            return self.get(path=f'orders/history/detail/customerorderid/{customer_order_id}')
        return False

    def delete_order(self, pair: str, order_id: str = None, customer_order_id: str = None):
        """
        Requires either order_id or customer_order_id to cancel order

        :param pair: Can be BTCZAR, ETHZAR or XRPZAR.
        :param order_id: id of order to be cancelled
        :param customer_order_id: Order ID provided by customer when creating the order
        :return: A 200 OK response means the request to cancel the order was accepted
        """
        data = {
            "orderId": order_id,
            "pair": pair
        }
        if order_id:
            data.update({'orderId': order_id})
        elif customer_order_id:
            data.update({'customerOrderId': customer_order_id})
        else:
            return False
        return self.delete(path='orders/order', data=data)
