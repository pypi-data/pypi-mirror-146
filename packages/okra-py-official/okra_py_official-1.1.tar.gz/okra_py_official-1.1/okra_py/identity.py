from .base import Initializer


class OkraIdentify(Initializer):
    """
    allows you to retrieve various account holder information on file with the bank, including names, emails, phone numbers, and addresses.
    
    docs link: https://docs.okra.ng/products/identity
    
    Initialize with token and base_url(e.g 'https://api.okra.ng/sandbox/v2/')

    Each of the underlying methods return the full response object
    """

    def get_identity(self):
        """
        Retrieve transactions

        Returns: Response object
        """
        url = self._base_url + "products/identities"
        return self._requests.post(url, headers=self._headers)

    def get_by_id(self, idx, page=1, limit=20):
        """
        retrieve various account holder information on file using the id.
        
        Args : "idx" (string)
        """
        url = self._base_url + "identity/getById"
        data_ = {"id": idx, "page": page, "limit": limit}
        return self._requests.post(url, headers=self._headers, json=data_)

    def get_by_options(self, first_name, last_name, page=1, limit=20):
        """
        fetch identity info using the options metadata you provided when setting up the widget.
        
        Args : "first_name" (string): "Uchencho",
               "last_name" (string): "Nwa Alozie"
        """
        url = self._base_url + "identity/byOptions"
        data_ = {"page": page, "limit": limit,
                 "options": {"first_name": first_name, "last_name": last_name}}
        return self._requests.post(url, headers=self._headers, json=data_)

    def get_by_customer(self, customer_id, page=1, limit=20):
        """
        retrieve various account holder information on file using the customer id.
        
        Args : "customer_id" (string)
        """
        url = self._base_url + "identity/getByCustomer"
        data_ = {"page": page, "limit": limit, "customer": customer_id}
        return self._requests.post(url, headers=self._headers, json=data_)

    def get_by_date(self, from_, to_, page=1, limit=20):
        """
        etrieve various account holder information on file using date range.
        
        Args : "to_" (string): "2020-4-02",
                "from_" (string): "2020-01-01"
        """
        url = self._base_url + "identity/getByDate"
        data_ = {"page": page, "limit": limit, "to": to_, "from": from_}
        return self._requests.post(url, headers=self._headers, json=data_)

    def get_by_customer_date(self, customer_id, from_, to_, page=1, limit=20):
        """
        fetch account holder information on file using date range and customer id.
        
        Args : "customer" (string):"5rggfdfghjkl4567",
                "to_" (string): "2020-04-02",
                "from_" (string): "2020-01-01"
        """
        url = self._base_url + "identity/getByCustomerDate"
        data_ = {"page": page, "limit": limit, "to": to_, "from": from_, "customer": customer_id}
        return self._requests.post(url, headers=self._headers, json=data_)

    def verify_bvn(self, bvn):
        """
        BVN means Bank Verification Number. It is a unique identity given to users that can be verified across the
        Nigerian Banking Industry

        lookup BVN and get detailed information on the BVN Identity.

        Args : "bvn" (string):"5rggfdfghjkl4567",
        """
        url = self._base_url + "products/kyc/bvn-verify"
        data_ = {"bvn": bvn}
        return self._requests.post(url, headers=self._headers, json=data_)

    def verify_company(self, company_name, rc_number):
        """
        retrieve the full details of a registered company in Nigeria
        NOTE - This endpoint is only available for Nigerians..

        Args : "company_name" (string):"5rggfdfghjkl4567",
               "rc_number" (string):"5rggfdfghjkl4567",
        """
        url = self._base_url + "products/kyc/rc-verify"
        data_ = {"company_name": company_name, "rc_number": rc_number}
        return self._requests.post(url, headers=self._headers, json=data_)

    def verify_company_tax(self, company_name, rc_number, tin_number):
        """
        retrieve  the full details of registered company in Nigeria and their tax information
        NOTE - This endpoint is only available for Nigerians..

        Args : "company_name" (string):"5rggfdfghjkl4567",
               "rc_number" (string):"5rggfdfghjkl4567",
        """
        url = self._base_url + "products/kyc/rc-tin-verify"
        data_ = {"company_name": company_name, "rc_number": rc_number, "tin_number": tin_number}
        return self._requests.post(url, headers=self._headers, json=data_)

    def verify_customer_tin(self, company_name, tin_number):
        """
        TIN means Tax Identification Number. It is an identification number used for tax purposes

        fetch your end user's details using the Tax Identification Number of the person

        Args : "company_name" (string):"5rggfdfghjkl4567",
               "tin_number" (string):"5rggfdfghjkl4567",
        """
        url = self._base_url + "products/kyc/rc-verify"
        data_ = {"company_name": company_name, "tin_number": tin_number}
        return self._requests.post(url, headers=self._headers, json=data_)

    def verify_customer_nin(self, nin):
        """
        NIN means National Identification Number. It is a means of identification that contains robust information of
        an individual .

        fetch and verify customers details using National Identification Number.

        Args : "nin" (string):"5rggfdfghjkl4567",
        """
        url = self._base_url + "products/kyc/nin-verify"
        data_ = {"nin": nin}
        return self._requests.post(url, headers=self._headers, json=data_)

    def merge_identities(self, initial, final):
        """
        merge identities in your Okra account

        Args : "nin" (string):"5rggfdfghjkl4567",
        """
        url = self._base_url + "products/identity/merge"
        data_ = {"initial": initial, "final": final}
        return self._requests.post(url, headers=self._headers, json=data_)
