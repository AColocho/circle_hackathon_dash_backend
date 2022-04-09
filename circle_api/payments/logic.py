import requests as r
from uuid import uuid4
from hashlib import blake2b
import os

os.environ['API_KEY'] = "Bearer QVBJX0tFWTo2ZWRmMjY5ODUxYTJlOTdkOTBkYmU1YTZhYmFjMThmZjpmOGE1YzZhZTIzNzM2OWMzNDIwMjhkZmMxYmFhYjA2NA=="

class Connect:
    def __init__(self) -> None:
        self.headers = { "Accept": "application/json", 
                        "Content-Type": "application/json",
                        "Authorization": os.environ['API_KEY']}
        
    def get_public_key(self):
        url = "https://api-sandbox.circle.com/v1/encryption/public"
        return r.get(url=url, headers=self.headers).json()
    
    def pay_card(self, query_object):
        url = "https://api-sandbox.circle.com/v1/cards"
        data = query_object.dict()
        
        h = blake2b(salt=b'win', digest_size=25)
        session_id = data['session_id']
        h.update(session_id.encode('utf-8'))
        
        card_request_id = str(uuid4())
        card_payment_id = str(uuid4())
        
        card_request = {
            "billingDetails": {
                "name": data['name'],
                "city": data['city'],
                "country": data['country'],
                "line1": data['address_1'],
                "line2": data['address_2'],
                "district": data['state'],
                "postalCode": data['zipcode']
            },
            "metadata": {
                "email": data['email'],
                "phoneNumber": data['phone'],
                "sessionId": h.hexdigest(),
                "ipAddress": data['address_ip']
            },
            "idempotencyKey": card_request_id,
            "keyId": "key1",
            "encryptedData": data['encrypted_data'],
            "expMonth": data['exp_month'],
            "expYear": data['exp_year']
        }
        
        response = r.post(url, json=card_request, headers=self.headers).json()
        

        url = "https://api-sandbox.circle.com/v1/payments"

        card_payment = {
            "metadata": card_request.get('metadata'),
            "amount": {
                "amount": data['amount'],
                "currency": "USD"
            },
            "autoCapture": True,
            "source": {
                "id": response['data']['id'],
                "type": "card"
            },
            "idempotencyKey": card_payment_id,
            "keyId": "key1",
            "verification": "none",
            "description": data['description'],
        }

        response = r.post(url, json=card_payment, headers=self.headers).json()
        return response


    def pay_ach(self, query_object):
        url = "https://api-sandbox.circle.com/v1/banks/ach"
        data = query_object.dict()
        
        h = blake2b(salt=b'win', digest_size=25)
        session_id = data['session_id']
        h.update(session_id.encode('utf-8'))
        
        ach_request_id = str(uuid4())
        ach_payment_id = str(uuid4())
        
        ach_request = {
            "billingDetails": {
                "name": data['name'],
                "city": data['city'],
                "country": data['country'],
                "line1": data['address_1'],
                "line2": data['address_2'],
                "district": data['state'],
                "postalCode": data['zipcode']
            },
            "metadata": {
                "email": data['email'],
                "phoneNumber": data['phone'],
                "sessionId": h.hexdigest(),
                "ipAddress": data['address_ip']
            },
            "idempotencyKey": ach_request_id,
            "plaidProcessorToken": "processor-sandbox-circle-82cf95bb-43f8-4191-8d30-2c9f42853621"
        }
        
        response = r.post(url, json=ach_request, headers=self.headers).json()
        
        card_payment = {
            "metadata": ach_request.get('metadata'),
            "amount": {
                "amount": data['amount'],
                "currency": "USD"
            },
            "autoCapture": True,
            "source": {
                "id": response['data']['id'],
                "type": "card"
            },
            "idempotencyKey": ach_payment_id,
            "keyId": "key1",
            "verification": "none",
            "description": data['description'],
        }
        
        response = r.post(url, json=card_payment, headers=self.headers).json()
        return response
    
    def pay_blockchain(self, query_object):
        data = query_object.dict()
        
        url = "https://api-sandbox.circle.com/v1/transfers"
        
        transfer_request_id = str(uuid4())

        payload = {
            "source": {
                "type": "wallet",
                "id": data['source_wallet_id']
            },
            "destination": {
                    "type": "wallet",
                    "id": "1000866229"
                },
            "amount": {
                "amount": data['amount'],
                "currency": data['currency']
            },
            "idempotencyKey": transfer_request_id
        }
        
        response = r.post(url, json=payload, headers=self.headers).json()
        
        return response
    
    