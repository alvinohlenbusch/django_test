import requests
import json
from integrationApis.models import SynapseFIUser
from django.core.exceptions import ObjectDoesNotExist

class SynapseFI():
    """ Class for interacting with the SynapseFI API """
    client_id = 'client_id_2bb1e412edd311e6bd04e285d6015267'
    client_secret = 'client_secret_2bb1e714edd311e6bd04e285d6015267'
    fp = 'e83cf6ddcf778e37bfe3d48fc78a6502062fc1030449628c699ef3c4ffa6f9a2000b8acc3c4c0addd8013285bb52c89e5267b628ca02fa84a6d71fe186b7cd5d'
    refresh_token = 'refresh_WLODtEHjqwXzmTNsGYuJoCQng60M13Pdk4fbpB00'
    oauth_key = ''

    def _url(self, path):
        return 'https://uat-api.synapsefi.com/v3.1' + path
    
    def _hdr(self):
        return {'x-sp-gateway': self.client_id + '|' + self.client_secret, 
           'x-sp-user-ip': '127.0.0.1',
           'x-sp-user': '|' + self.fp}

    def _oauth_hdr(self):
        return {'x-sp-user-ip': '127.0.0.1',
           'x-sp-user': self.oauth_key + '|' + self.fp}

    def _get_ref_tok(self, user_id):
        """ helper function to get a new refresh_token """
        print('Getting a new refresh token for user={}'.format(user_id))
        r = requests.get(self._url('/users/' + user_id + '?full_dehydrate=no'), headers=self._hdr())
        if r.status_code == 200:
            answer = r.json()
            return answer['refresh_token']
        else:
            raise ObjectDoesNotExist('user_id %s does not exist' % user_id)
    
    def _get_oauth(self, user_id):
        """ helper function to get new oauth, and deal with getting a new refresh_token if needed """
        url = self._url('/oauth/' + user_id)
        header = self._hdr()
        data = {
            "refresh_token": self.refresh_token
            }
        print('Getting a new oauth_key for user={}'.format(user_id))
        r = requests.post(url, headers=header, json=data)
        if r.status_code == 409:
            self.refresh_token = self._get_ref_tok(user_id)
            # Try the oauth call again
            header = self._hdr()
            data = {
                "refresh_token": self.refresh_token
                }

            r = requests.post(url, headers=header, json=data)
        answer = r.json()
        return answer['oauth_key']

    
    def _syn_get(self, url, user_id):
        """ helper function to make a call, and deal with reauthenticating if needed """
        header = self._oauth_hdr();
        r = requests.get(url, headers=header)
        # check if we need to get a new oauth_key
        if r.status_code == 401:
            self.oauth_key = self._get_oauth(user_id)
            # retry the original query
            header = self._oauth_hdr();
            r = requests.get(url, headers=header)
        answer = r.json()
        return answer
    
    def get_users(self, query):
        """ for a given query string, return the list of users from SynapseFI """
        url = self._url('/users?show_refresh_tokens=yes&per_page=10&page=1&query='  + query);
        r = requests.get(url, headers=self._hdr())
        answer = r.json()
        return answer
    
    def get_accounts(self, user_id):
        """ for a given query string, return the list of users from SynapseFI """
        # Lookup the user in our DB and grab its oauth_token and refresh_token
        localoauth = ''
        localreftok = ''
        sfiu = ''
        # Get existing keys from DB if we have them
        try:
            sfiu = SynapseFIUser.objects.get(user_id=user_id)
            print("sfiu={}".format(sfiu))
            self.oauth_key = localoauth = sfiu.oauth_key
            print("got key %s" % self.oauth_key)
            self.refresh_token = localreftok = sfiu.refresh_token
        except ObjectDoesNotExist:
            print("user_id {} doesn't exist".format(user_id))
            sfiu = SynapseFIUser(user_id=user_id)
        
        # Now make actual Synapse API calls
        url = self._url('/users/'  + user_id + '/nodes');
        answer = self._syn_get(url, user_id)
        
        # Save our new keys to DB if we got them
        if (self.oauth_key != localoauth):
            print("We got a new oauth")
            sfiu.oauth_key = self.oauth_key
        if (self.refresh_token != localreftok):
            print("We got a new reftok")
            sfiu.refresh_token = self.refresh_token
        sfiu.save()
        return answer
       
    def create_user(self):
        """ create a user """
        
        data = {
              "logins": [
                {
                  "email": "aro@aro.com",
                  "password":"test1234",
                  "scope":"READ_AND_WRITE"
                }
              ],
              "phone_numbers": [
                "901.942.8167"
              ],
              "legal_names": [
                "ARO Test User"
              ],
              "documents":[{
                    "email":"test@test.com",
                    "phone_number":"901-942-8167",
                    "ip":"12134323",
                    "name":"Charlie Brown",
                    "alias":"Woof Woof",
                    "entity_type":"M",
                    "entity_scope":"Arts & Entertainment",
                    "day":2,
                    "month":5,
                    "year":1989,
                    "address_street":"170 St Germain Ave",
                    "address_city":"SF",
                    "address_subdivision":"CA",
                    "address_postal_code":"94114",
                    "address_country_code":"US",
                    "virtual_docs":[{
                        "document_value":"2222",
                        "document_type":"SSN"
                    }],
                    "physical_docs":[{
                        "document_value": "data:image/gif;base64,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",
                        "document_type": "GOVT_ID"
                    }],
                    "social_docs":[{
                        "document_value":"https://www.facebook.com/sankaet",
                        "document_type":"FACEBOOK"
                    }]
                }],
              "extra": {
                "note": "Interesting user",
                "supp_id": "122eddfgbeafrfvbbb",
                "cip_tag":1,
                "is_business": False,
                "extra_security": False
              }
            }

        url = self._url('/users');
        r = requests.post(url, json=data, headers=self._hdr())
        answer = r.json()
        return answer

    
class CapitalOne():
    
    def get_access_token(self):
        client_id = 'enterpriseapi-sb-tJOw55ype3LktRNB5zY7oIHq'
        client_secret = '175384eb1888f2dded491e8d7242398f0c5901db'
        url = 'https://api-sandbox.capitalone.com/oauth2/token' 
        params = {'client_id': client_id, 'client_secret': client_secret, 'grant_type': 'client_credentials'}
        r = requests.get(url, params=params)
        answer = r.json()
        token = answer['access_token']
        return token
    
    def get_account_applications(self):
        token = self.get_access_token()
        
        url = 'https://api-sandbox.capitalone.com/deposits/account-applications/'
        hdr = {'Content-Type': 'application/json', 
               'Authorization': 'Bearer ' + token}
        params = {
            "applicants": [
            {
            "applicantRole": "primary",
            "firstName": "John",
            "lastName": "Smith",
            "taxIdType": "SSN",
            "taxId": "000-00-0001",
            "dateOfBirth": "1986-01-01",
            "homeAddress": {
            "addressLine1": "000 Main St",
            "city": "Richmond",
            "stateCode": "VA",
            "postalCode": "00000"
            },
            "primaryPhoneNumber": "1111111111",
            "backupWithholding": False,
            "emailAddress": "email@capitalone.com",
            "citizenshipCountry": "USA",
            "secondaryCitizenshipCountry": "CAN",
            "employmentStatus": "Employed",
            "jobTitle": "Branch Manager",
            "annualIncome": 75000
            }
            ],
            "productId": "3000",
            "fundingDetails": {
            "fundingType": "fundach",
            "fundingAmount": 100.1,
            "externalAccountDetails": {
            "accountNumber": "123456",
            "bankABANumber": "000234456",
            "accountOwnership": "primary"
            }
            },
            "termsAndConditions": {
            "acceptAccountDisclosures": True,
            "acceptPaperlessAgreement": True,
            "acceptFraudProtection": True
            }
            }

        r = requests.post(url, json=params, headers=hdr)
        if r.status_code > 300:
            return { 'bankABANumber': token, 'applicationStatus': r.status_code}
        account_applications_list = r.json()
        return account_applications_list
    