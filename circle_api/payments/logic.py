from ..connection import ConnectionDB
from sqlalchemy import insert, update, text
from sqlalchemy.orm import Session
import requests as r
from uuid import uuid4
from hashlib import blake2b
import os

os.environ['API_KEY'] = "Bearer QVBJX0tFWTo2ZWRmMjY5ODUxYTJlOTdkOTBkYmU1YTZhYmFjMThmZjpmOGE1YzZhZTIzNzM2OWMzNDIwMjhkZmMxYmFhYjA2NA=="

class Connect(ConnectionDB):
    def __init__(self) -> None:
        super().__init__()
        self.session = Session(self.engine)
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
        
        response = r.post(url, json=card_request, headers=self.headers)
        
        if response.status_code != 201:
            return response.json()
        else:
            response = response.json()

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
        
        payment_id = response['data']['id']
        raw_sql = text(f'UPDATE invoice SET payment_id="{payment_id}", status="p" WHERE invoice_id="{data["invoice_id"]}"')
        self.session.execute(raw_sql)
        self.session.commit()
        
        return {'payment_id':payment_id}


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
        
        response = r.post(url, json=ach_request, headers=self.headers)

        if response.status_code != 201:
            return response.json()
        else:
            response = response.json()
            
        url = "https://api-sandbox.circle.com/v1/payments"
        
        ach_payment = {
            "metadata": ach_request.get('metadata'),
            "amount": {
                "amount": data['amount'],
                "currency": "USD"
            },
            "autoCapture": True,
            "source": {
                "id": response['data']['id'],
                "type": "ach"
            },
            "idempotencyKey": ach_payment_id,
            "keyId": "key1",
            "verification": "none",
            "description": data['description'],
        }
        
        response = r.post(url, json=ach_payment, headers=self.headers).json()
        
        payment_id = response['data']['id']
        raw_sql = text(f'UPDATE invoice SET payment_id="{payment_id}", status="p" WHERE invoice_id="{data["invoice_id"]}"')
        self.session.execute(raw_sql)
        self.session.commit()
        
        return {'payment_id':payment_id}
    
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
    
    def payment_status(self, payment_id):
        payment_id = payment_id.dict()['payment_id']
        url = f"https://api-sandbox.circle.com/v1/payments/{payment_id}"
        
        return r.get(url, headers=self.headers).json()
        
    
    