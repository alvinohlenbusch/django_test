import requests
import json

class SynapseFI():
    def get_users(self, query):
        client_id = 'client_id_2bb1e412edd311e6bd04e285d6015267'
        client_secret = 'client_secret_2bb1e714edd311e6bd04e285d6015267'
        fp = 'e83cf6ddcf778e37bfe3d48fc78a6502062fc1030449628c699ef3c4ffa6f9a2000b8acc3c4c0addd8013285bb52c89e5267b628ca02fa84a6d71fe186b7cd5d'
        hdr = {'x-sp-gateway': client_id + '|' + client_secret, 
               'x-sp-user-ip': '127.0.0.1 ',
               'x-sp-user': '|' + fp}
        url = 'https://uat-api.synapsefi.com/v3.1/users?show_refresh_tokens=yes&per_page=10&page=1&query='  + query
        r = requests.get(url, headers=hdr)
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
    