from valr.session import ValrAPISession


class Pay(ValrAPISession):
    """
    Make use of our powerful Pay API to instantly initiate new payments,
    get status, details and a history of your payments made and received using VALR Pay.
    """

    def pay(
            self,
            amount: float,
            recipient_email: str, recipient_cell: str, recipient_pay_id: str,
            recipient_note: str = None, sender_note: str = None,
            currency: str = 'ZAR', anonymous: bool = False
    ):
        """
        Only one of the recipient identifiers is required at a time. Use more than one, and it will fail as expected.

        :param amount: Value of the currency to be paid
        :param recipient_email: Recipient email address
        :param recipient_cell: Recipient cell number
        :param recipient_pay_id: Recipient's paymentID / payment reference
        :param currency: The currency in which payment is made. Currently only ZAR is supported
        :param recipient_note: A note to the recipient (optional)
        :param sender_note: A note for the sender (optional)
        :param anonymous: Can be true or false. Default is false i.e. payment is not anonymous.
        :return: Successful requests return 202 - Accepted with an identifier and transactionId in the body
        """
        data = {
            "amount": amount,
            "currency": currency,
            "anonymous": anonymous
        }
        if recipient_email:
            data.update({'recipientEmail': recipient_email})
        elif recipient_cell:
            data.update({'recipientCellNumber': recipient_cell})
        elif recipient_pay_id:
            data.update({'recipientPayId': recipient_pay_id})
        else:
            return False
        if recipient_note:
            data.update({'recipientNote': recipient_note})
        if sender_note:
            data.update({'senderNote': sender_note})
        return self.post(path='pay', data=data)

    def limits(self):
        """
        :return: Retrieves all the payment limits applicable to your account.
        This will include minimum payment amount, maximum payment amount, payment currency and
         limit type (currently per transaction)
        """
        return self.get(path='pay/limits')

    def payid(self):
        """
        :return: Get your account's unique VALR PayID.
        """
        return self.get(path='pay/payid')

    def history(self, status: list = None, skip: int = 0, limit: int = 100):
        """
        :param status: Valid status are INITIATED, AUTHORISED, COMPLETE, RETURNED, FAILED, EXPIRED.
        :param limit: Max limit 100
        :param skip: Number of items to skip
        :return: Fetches a list of all payments made from and made to the current users account.
        """
        path = f'pay/history/?skip={skip}&limit={limit}'
        if status:
            path += f'&STATUS={",".join(status)}'
        return self.get(path=path)

    def payment_details(self, identifier: str):
        """
        :param identifier: payment identifier ID
        :return: Get the payment details by specifying the payment identifier
        """
        return self.get(path=f'pay/identifier/{identifier}')

    def payment_status(self, transaction_id: str):
        """
        :param transaction_id: transaction ID
        :return: Get the status and details of a payment transaction, by specifying a transactionId
        """
        return self.get(path=f'pay/transactionid/{transaction_id}')
