from .base import Initializer


class OkraBalance(Initializer):
    """
    returns the real-time balance for each of a record's accounts. 
    It can be used for existing Records that were added via any of Okra’s other products
    
    https://docs.okra.ng/products/balance
    
    Initialize with token and base_url(e.g 'https://api.okra.ng/sandbox/v2/')
    """

    def retrieve_balance(self):
        """
        Retrieve Bank balance

        Returns: Response object
        """
        url = self._base_url + "products/balances"
        return self._requests.post(url, headers=self._headers)

    def get_by_id(self, idx, page=1, limit=20):
        """
        fetch balance info using the id of the balance.
        
        Args : "idx" (string)
        """
        url = self._base_url + "balance/getById"
        data_ = {"id": idx, "page": page, "limit": limit}
        return self._requests.post(url, headers=self._headers, json=data_)

    def get_by_options(self, first_name, last_name, page=1, limit=20):
        """
        fetch balance info using the options metadata you provided when setting up the widget.
        
        Args : "first_name" (string): "Uchencho",
               "last_name" (string): "Nwa Alozie"
        """
        url = self._base_url + "balance/byOptions"
        data_ = {"page": page, "limit": limit,
                 "options": {"first_name": first_name, "last_name": last_name}}
        return self._requests.post(url, headers=self._headers, json=data_)

    def get_by_customer(self, customer_id, page=1, limit=20):
        """
        fetch balance info using the customer id.
        
        Args : "customer_id" (string)
        """
        url = self._base_url + "balance/getByCustomer"
        data_ = {"page": page, "limit": limit, "customer": customer_id}
        return self._requests.post(url, headers=self._headers, json=data_)

    def get_by_account(self, account_id, page=1, limit=20):
        """
        fetch balance info using the account id.
        
        Args : "account_id" (string)
        """
        url = self._base_url + "balance/getByAccount"
        data_ = {"page": page, "limit": limit, "account": account_id}
        return self._requests.post(url, headers=self._headers, json=data_)

    def get_by_type(self, type_, amount, page=1, limit=20):
        """
        fetch balance info using type of balance.
        
        Args : type_ (string) eg ledger_balance, available_balance
               value (string) eg 4000
        """
        url = self._base_url + "balance/getByType"
        data_ = {"page": page, "limit": limit, "type": type_, "value": amount}
        return self._requests.post(url, headers=self._headers, json=data_)

    def get_by_date(self, from_, to_, page=1, limit=20):
        """
        fetch balance info of a customer using date range only

        Args :  "to_" (string): "2020-04-02",
                "from_" (string): "2020-01-01"
        """
        url = self._base_url + "balance/getByDate"
        data_ = {"page": page, "limit": limit, "to": to_, "from": from_}
        return self._requests.post(url, headers=self._headers, json=data_)

    def get_by_customer_date(self, customer_id, from_, to_, page=1, limit=20):
        """
        fetch balance info of a customer using date range and customer id
        
        Args : "customer" (string):"5rggfdfghjkl4567",
                "to_" (string): "2020-04-02",
                "from_" (string): "2020-01-01"
        """
        url = self._base_url + "balance/getByCustomerDate"
        data_ = {"page": page, "limit": limit, "to": to_, "from": from_, "customer": customer_id}
        return self._requests.post(url, headers=self._headers, json=data_)

    def get_refresh_balance(self, account_id):
        """
        fetch the bank account balance associated with a record's current, savings, and domiciliary accounts when a
        slight change occurs in the account.
        
        Args : "account_id" (string),
        """
        url = self._base_url + "products/balance/refresh"
        data_ = {"account_id": account_id}
        return self._requests.post(url, headers=self._headers, json=data_)

    def get_enhanced_balance(self, account_id, customer_id, from_, to_, page=1, limit=20):
        """
        fetch a comprehensive paginated list of a specific balance of a customer.

        Args : "account_id" (string),
               "customer_id" (string),
               "to_" (string): "2020-04-02",
               "from_" (string): "2020-01-01",
        """
        url = self._base_url + "products/balance/process"
        data_ = {"page": page, "limit": limit, "from": from_, "to": to_, "customer_id": customer_id,
                 "account_id": account_id}
        return self._requests.post(url, headers=self._headers, json=data_)
