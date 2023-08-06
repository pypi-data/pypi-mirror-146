from valr.session import ValrAPISession


class Account(ValrAPISession):

    def current_api_key_info(self):
        """
        Returns the current API Key's information and permissions.
        """
        return self.get(path='account/api-keys/current')

    def subaccounts(self):
        """
        Returns the list of all subaccounts that belong to a primary account, with each subaccount's label and id.
        """
        return self.get(path='account/subaccounts')

    def all_non_zero_balances(self):
        """
        Returns the entire portfolio's balances that are greater than 0, grouped by
        account for primary account and subaccounts.
        """
        return self.get(path='account/balances/all')

    def register_subaccount(self, label: str):
        """
        Creates a new subaccount.

        :param label: The name given to the newly created subaccount
        """
        return self.post(path='account/subaccount', data={'label': label})

    def internal_transfer_account(self, from_id: int, told: int, currency_code: str, amount: float):
        """
        Transfer funds between 2 accounts.

        :param from_id: The id of the source account. Use 0 for the primary account
        :param told: The id of source account. Use 0 for the primary account
        :param currency_code: The currency code of the currency being transferred
        :param amount: The total amount being transferred
        """
        return self.post(
            path='account/subaccounts/transfer',
            data={
                'fromId': from_id,
                'told': told,
                'currencyCode': currency_code,
                'amount': amount
            }
        )

    def balances(self):
        """
        Returns the list of all wallets with their respective balances.
        """
        return self.get(path='account/balances')

    def transaction_history(
            self,
            skip: int = 0, limit: int = 200,
            transaction_type: list = None, currency: str = None,
            start_date_time: str = None, end_date_time: str = None,
            before_id: str = None
    ):
        """
        Transaction history for your account.

        :param skip: Skip number of items from the list
        :param limit: Limit the number of items returned. Max: 200
        :param transaction_type: List of transaction types to include.
                                See `transactionTypes` in docs.valr.com under Account
        :param currency: Include only transactions in this currency
        :param start_date_time: Include only transactions after this ISO 8601 start time
        :param end_date_time: Include only transactions before this ISO 8601 end time
        :param before_id: Transaction history may be paginated by supplying a transaction ID
        """
        if limit > 200:
            limit = 200
        path = f'account/transactionhistory?skip={skip}&limit={limit}'
        if transaction_type:
            path += f'&transactionType={",".join(transaction_type)}'
        if currency:
            path += f'&currency={currency}'
        if start_date_time:
            path += f'&startTime={start_date_time}'
        if end_date_time:
            path += f'&endTime={end_date_time}'
        if before_id:
            path += f'&beforeId={before_id}'
        return self.get(path=path)

    def trade_history_for_currency_pair(self, currency_pair: str, skip: int = 0, limit: int = 100):
        """
        Get the last 100 recent trades for a given currency pair for your account.

        :param currency_pair: Specify the currency pair for which you want to query the trade history.
                            Examples: BTCZAR, ETHZAR, XRPZAR, SOLZAR
        :param skip: Skip number of items from the list.
        :param limit: Limit the number of items returned.
        """
        if limit > 100:
            limit = 100
        return self.get(path=f'account/{currency_pair}/tradehistory?limit={limit}&skip={skip}')
