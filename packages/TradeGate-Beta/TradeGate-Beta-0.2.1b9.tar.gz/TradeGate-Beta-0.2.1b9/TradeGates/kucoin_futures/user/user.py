from kucoin_futures.base_request.base_request import KucoinFuturesBaseRestApi


class UserData(KucoinFuturesBaseRestApi):

    def transfer_kucoin_account(self, amount, bizNo=''):
        """
        https://docs.kumex.com/#transfer-funds-to-kucoin-main-account
        :param bizNo:  (Mandatory) A unique ID generated by the user, to ensure the operation is processed by the system only once.
            You are suggested to use UUID
        :type: str
        :param amount: (Mandatory) Amount to be transfered out
        :type:float
        :return:
        {
            "applyId": "5bffb63303aa675e8bbe18f9" //Transfer-out request ID
        }
        """
        params = {'amount': amount}
        if not bizNo:
            bizNo = self.return_unique_id[0:23]
        params['bizNo'] = bizNo
        return self._request('POST', '/api/v1/transfer-out', params=params)

    def transfer_kucoin_account_v2(self, amount, bizNo=''):
        """
        https://docs.kumex.com/#transfer-funds-to-kucoin-main-account-2
        :param bizNo:  (Mandatory) A unique ID generated by the user, to ensure the operation is processed by the system only once.
            You are suggested to use UUID
        :type: str
        :param amount: (Mandatory) Amount to be transfered out
        :type:float
        :return:
        {
            "applyId": "5bffb63303aa675e8bbe18f9" //Transfer-out request ID
        }
        """
        params = {'amount': amount}
        if not bizNo:
            bizNo = self.return_unique_id[0:23]
        params['bizNo'] = bizNo
        return self._request('POST', '/api/v2/transfer-out', params=params)

    def get_Transfer_history(self, **kwargs):
        """
        https://docs.kumex.com/#get-transfer-out-request-records-2
        :param kwargs:  [optional]  status,  startAt, endAt, currentPage , pageSize  and so on
        :return: {'totalNum': 0, 'totalPage': 0, 'pageSize': 50, 'currentPage': 1, 'items': [{
        "applyId": "5cd53be30c19fc3754b60928", //Transfer-out request ID
        "currency": "XBT", //Currency
        "status": "SUCCESS", //Status  PROCESSING, SUCCESS, FAILURE
        "amount": "0.01", //Transaction amount
        "reason": "", //Reason caused the failure
        "offset": 31986850860000, //Offset
        "createdAt": 1557769977000 //Request application time}, ....]}
        """
        params = {}
        if kwargs:
            params.update(kwargs)
        return self._request('GET', '/api/v1/transfer-list', params=params)

    def cancel_Transfer_out(self, applyId):
        """
        https://docs.kumex.com/#cancel-transfer-out-request
        :param applyId: (Mandatory) Transfer ID (Initiate to cancel the transfer-out request)
        :return: {'code': '200000',"data": {
       "applyId": "5bffb63303aa675e8bbe18f9" //Transfer-out request ID
        }  }
        """
        return self._request('DELETE', '/api/v1/cancel/transfer-out?applyId={}'.format(applyId))

    def get_withdrawal_quota(self, currency):
        """
        https://docs.kumex.com/#get-withdrawal-limit
        :param currency:  XBT  str (Mandatory)
        :return:
        {
          "currency": "XBT",//Currency
          "limitAmount": 2,//24h withdrawal limit
          "usedAmount": 0,//Withdrawal amount over the past 24h.
          "remainAmount": 2,//24h available withdrawal amount
          "availableAmount": 99.89993052,//Available balance
          "withdrawMinFee": 0.0005,//Withdrawal fee charges
          "innerWithdrawMinFee": 0,//Inner withdrawal fee charges
          "withdrawMinSize": 0.002,//Min. withdrawal amount
          "isWithdrawEnabled": true,//Available to withdrawal or not
          "precision": 8//Precision of the withdrawal amount
        }
        """
        params = {
            'currency': currency
        }
        return self._request('GET', '/api/v1/withdrawals/quotas', params=params)

    def sand_withdrawal(self, currency, address, amount, **kwargs):
        """
        https://docs.kumex.com/#withdraw-funds
        :param currency: Currency, only Bitcoin (XBT) is currently supported. (Mandatory)
        :type: str
        :param address: 	Withdrawal address (Mandatory)
        :type: str
        :param amount: Withdrawal amount (Mandatory)
        :type: float
        :param kwargs:  [Optional]  isInner, remark
        :return:
         {
            "withdrawalId": "" // Withdrawal ID. This ID can be used to cancel the withdrawal
        }
        """
        params = {
            'currency': currency,
            'address': address,
            'amount': amount
        }
        if kwargs:
            params.update(kwargs)

        return self._request('POST', '/api/v1/withdrawals', params=params)

    def get_withdrawal_list(self, **kwargs):
        """
        https://docs.kumex.com/#get-withdrawal-list
        :param kwargs: [optional] currentPage , pageSize  and so on
        :return:
         {
              "currentPage": 1,
              "pageSize": 50,
              "totalNum": 10,
              "totalPage": 1,
              "items": [{
                "withdrawalId": "5cda659603aa67131f305f7e",//Withdrawal ID. This ID can be used to cancel the withdrawal
                "currency": "XBT",//Currency
                "status": "FAILURE",//Status
                "address": "3JaG3ReoZCtLcqszxMEvktBn7xZdU9gaoJ",//Withdrawal address
                "isInner": true,//Inner withdrawal or not
                "amount": 1,//Withdrawal amount
                "fee": 0,//Withdrawal fee charges
                "walletTxId": "",//Wallet TXID
                "createdAt": 1557816726000,//Withdrawal time
                "remark": "",//Withdrawal remarks
                "reason": "Assets freezing failed."// Reason causing the failure
          }]
        }
        """
        params = {}
        if kwargs:
            params.update(kwargs)

        return self._request('GET', '/api/v1/withdrawal-list', params=params)

    def cancel_withdrawal(self, withdrawalId):
        """
        https://docs.kumex.com/#cancel-withdrawal
        :param withdrawalId: Path Parameter. Withdrawal ID  (Mandatory)
        :type: str
        :return: {'address': '', 'memo': ''}
        """
        return self._request('DELETE', '/api/v1/withdrawals/{withdrawalId}'.format(withdrawalId=withdrawalId))

    def get_deposit_address(self, currency):
        """
        https://docs.kumex.com/#get-deposit-address
        :param currency:  XBT  str (Mandatory)
        :return:
        """
        params = {
            'currency': currency
        }
        return self._request('GET', '/api/v1/deposit-address', params=params)

    def get_deposit_list(self, **kwargs):
        """
        https://docs.kumex.com/#get-deposits-list

        :param kwargs:  [optional]  currentPage , pageSize  and so on
        :return:
            {
              "currentPage": 1,
              "pageSize": 50,
              "totalNum": 1,
              "totalPage": 1,
              "items": [{
                "currency": "XBT",//Currency
                "status": "SUCCESS",//Status type: PROCESSING, WALLET_PROCESSING, SUCCESS, FAILURE
                "address": "5CD018972914B66104BF8842",//Deposit address
                "isInner": false,//Inner transfer or not
                "amount": 1,//Deposit amount
                "fee": 0,//Fees for deposit
                "walletTxId": "5CD018972914B66104BF8842",//Wallet TXID
                "createdAt": 1557141673000 //Funds deposit time
              }]
            }

        """
        params = {}
        if kwargs:
            params.update(kwargs)

        return self._request('GET', '/api/v1/deposit-list', params=params)

    def get_account_overview(self, currency='XBT'):
        """
        https://docs.kumex.com/#get-account-overview
        :return:
        {
          "accountEquity": 99.8999305281, //Account equity
          "unrealisedPNL": 0, //Unrealised profit and loss
          "marginBalance": 99.8999305281, //Margin balance
          "positionMargin": 0, //Position margin
          "orderMargin": 0, //Order margin
          "frozenFunds": 0, //Frozen funds for withdrawal and out-transfer
          "availableBalance": 99.8999305281 //Available balance
          "currency": "XBT" //currency code
        }
        """
        params = {
            'currency': currency
        }
        return self._request('GET', '/api/v1/account-overview', params=params)

    def get_transaction_history(self, **kwargs):
        """
        https://docs.kumex.com/#get-transaction-history
        :param kwargs: [optional]  startAt, endAt, type, offset maxCount
        :return:
         {
          "hasMore": false,//Whether there are more pages
          "dataList": [{
            "time": 1558596284040, //Event time
            "type": "RealisedPNL", //Type
            "amount": 0, //Transaction amount
            "fee": null,//Fees
            "accountEquity": 8060.7899305281, //Account equity
            "status": "Pending", //Status. If you have held a position in the current 8-hour settlement period.
            "remark": "XBTUSDM",//Ticker symbol of the contract
            "offset": -1 //Offset,
            "currency": "XBT"  //Currency
          },
          {
            "time": 1557997200000,
            "type": "RealisedPNL",
            "amount": -0.000017105,
            "fee": 0,
            "accountEquity": 8060.7899305281,
            "status": "Completed",//Status. Status. Funding period that has been settled.
         "remark": "XBTUSDM",
         "offset": 1,
         "currency": "XBT"  //Currency
         }]
        }
        """
        params = {}
        if kwargs:
            params.update(kwargs)

        return self._request('GET', '/api/v1/transaction-history', params=params)
