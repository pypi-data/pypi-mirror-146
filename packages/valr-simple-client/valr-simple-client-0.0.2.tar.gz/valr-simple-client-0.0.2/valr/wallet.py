from valr.session import ValrAPISession


class Crypto(ValrAPISession):
    """ Cryptocurrency Wallet APIs. """

    def deposit_address(self, currency_code: str):
        """
        :param currency_code: Currently, the allowed values here are BTC, ETH, XRP, SOL, ENJ, MANA, UNI, USDC
        :return: Returns the default deposit address associated with currency specified
        """
        return self.get(path=f'wallet/crypto/{currency_code}/deposit/address')

    def address_book(self, currency_code: str = None):
        """
        :param currency_code: Specify the currency for which you want to query the address book
        :return: Returns all the withdrawal addresses whitelisted for this account.
        """
        path = 'wallet/crypto/address-book'
        if currency_code:
            path += f'/?currencyCode={currency_code}'
        return self.get(path=path)

    def withdrawal_info(self, currency_code: str):
        """
        :param currency_code: This is the currency code of the currency you want withdrawal information about.
                            Examples: BTC, ETH, XRP, ADA, etc.
        :return: Get all the information about withdrawing a given currency from your VALR account.
                That will include withdrawal costs, minimum withdrawal amount etc.
        """
        return self.get(path=f'wallet/crypto/{currency_code}/withdraw')

    def withdraw(self, currency_code: str, address: str, amount: float, payment_ref: str = None):
        """
        Withdraw cryptocurrency funds to an address.

        :param currency_code: This is the currency code for the currency you are withdrawing. Examples: BTC, ETH, XRP, ADA, etc.
        :param address: address to withdraw to
        :param amount: amount in Float to withdraw
        :param payment_ref: Optional payment reference (max 256 char)
        :return:
        """
        data = {
            'amount': amount,
            'address': address
        }
        if payment_ref:
            data.update({
                'paymentReference': payment_ref
            })
        return self.post(path=f'wallet/crypto/{currency_code}/withdraw', data=data)

    def withdraw_status(self, currency_code: str, withdraw_id: str):
        """
        Check the status of a withdrawal.

        :param currency_code: This is the currency code for the currency you have withdrawn.
                            Examples: BTC, ETH, XRP, ADA, etc.
        :param withdraw_id: The unique id that represents your withdrawal request.
                        This is provided as a response to the API call to withdraw (new_withdraw).
        :return:
        """
        return self.get(path=f'wallet/crypto/{currency_code}/withdraw/{withdraw_id}')

    def deposit_history(self, currency_code: str, skip: int = 0, limit: int = 100):
        """
        :param currency_code: Currently, the allowed values here are BTC, ETH, XRP
        :param skip: Skip number of items from the list.
        :param limit: Limit the number of items returned.
        :return: Get the Deposit History records for a given currency.
        """
        return self.get(path=f'wallet/crypto/{currency_code}/deposit/history?skip={skip}&limit={limit}')

    def withdraw_history(self, currency_code: str, skip: int = 0, limit: int = 100):
        """
        :param currency_code: Currently, the allowed values here are BTC, ETH, XRP
        :param skip: Skip number of items from the list.
        :param limit: Limit the number of items returned.
        :return: Get Withdrawal History records for a given currency.
        """
        return self.get(path=f'wallet/crypto/{currency_code}/withdraw/history?skip={skip}&limit={limit}')


class Fiat(ValrAPISession):
    """ ZAR Wallet APIs """

    def accounts(self, currency_code: str = 'ZAR'):
        """
        :param currency_code: The currency code for the fiat currency. Supported: ZAR.
        :return: Get a list of bank accounts that are linked to your VALR account.
        """
        return self.get(path=f'wallet/fiat/{currency_code}/accounts')

    def deposit_reference(self, currency_code: str = 'ZAR'):
        """
        :param currency_code: The currency code for the fiat currency. Supported: ZAR.
        :return: Get the unique Deposit Reference for the primary account or subaccount whose API Key is authorised.
        """
        return self.get(path=f'wallet/fiat/{currency_code}/deposit/reference')

    def withdraw(self, bank_account_id: str, amount: float, fast: bool = True, currency_code: str = 'ZAR'):
        """
        Withdraw your ZAR funds into one of your linked bank accounts.
        :param bank_account_id: Id of your linked bank account to withdraw to
        :param amount: Amount in currency_code to Withdraw
        :param fast: f the value of this field is "true" the withdrawal will be processed with
        real-time clearing ("RTC") (participating banks only) or real-time gross settlement ("RTGS")
        during our next withdrawal run.
        :param currency_code: The currency code for the fiat currency. Supported: ZAR.
        :return: Get the unique Withdrawal Reference for this withdrawal
        """
        data = {
            "linkedBankAccountId": bank_account_id,
            "amount": amount,
            "fast": fast
        }
        return self.post(path=f'wallet/fiat/{currency_code}/withdraw', data=data)


class WireTransfer(ValrAPISession):
    """ Wire Transfer API for wire bank accounts deposits and withdrawals """

    def accounts(self):
        """
        :return: Get a list of all authorised wire bank accounts that are linked to your VALR account.
        """
        return self.get(path='wire/accounts')

    def deposit_instructions(self, identifier: str):
        """
        :param identifier: account identifier
        :return: Fetches the deposit (wire) instructions for the account specified by the identifier
        """
        return self.get(path=f'wire/accounts/{identifier}/instructions')

    def withdraw(self, wire_bank_account_id: str, amount: float):
        """
        Withdraw your USDC funds into one of your linked wire accounts in USD.

        :param wire_bank_account_id: id of your linked wire bank account
        :param amount: amount to withdraw (As USD)
        :return: Successful response body contains the id of the withdrawal, currency, amount, status and
                created at timestamp.
        """
        data = {
            "wireBankAccountId": wire_bank_account_id,
            "amount": amount
        }
        return self.post(path='wire/withdrawals', data=data)


class Wallet:
    """
    Access your wallets programmatically.
    """

    def __init__(self, key: str, secret: str):
        self.crypto = Crypto(key=key, secret=secret)
        self.fiat = Fiat(key=key, secret=secret)
        self.wire = WireTransfer(key=key, secret=secret)
