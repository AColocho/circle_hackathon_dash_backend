from uuid import uuid4
import requests as r
import os

os.environ['API_KEY'] = "Bearer QVBJX0tFWTo2ZWRmMjY5ODUxYTJlOTdkOTBkYmU1YTZhYmFjMThmZjpmOGE1YzZhZTIzNzM2OWMzNDIwMjhkZmMxYmFhYjA2NA=="

class Connect:
    def __init__(self) -> None:
        self.headers = { "Accept": "application/json", 
                        "Content-Type": "application/json",
                        "Authorization": os.environ['API_KEY']}
        
    def generate_wallet(self):
        url = "https://api-sandbox.circle.com/v1/wallets"
        
        wallet_request_id = str(uuid4())
        payload = {"idempotencyKey": wallet_request_id}
        
        response = r.post(url, json=payload, headers=self.headers).json()
        
        return response