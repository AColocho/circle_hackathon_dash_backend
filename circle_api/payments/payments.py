from fastapi import APIRouter
from pydantic import BaseModel
from .logic import Connect
from hashlib import blake2b

connect = Connect()

router = APIRouter(prefix='/payments', tags=['payments'])

@router.get('/public_key')
async def get_public_key():
    return connect.get_public_key()

class Card(BaseModel):
    encrypted_data:str
    exp_month:int
    exp_year:int
    session_id:str
    address_ip:str
    name:str
    email:str
    phone:str
    address_1:str
    address_2:str = None
    state:str
    city:str
    country:str = 'US'
    zipcode:str
    amount:float
    currency:str = 'USD'
    description:str
        
@router.post('/pay_card')
def pay_card(card_details:Card):
    return connect.pay(card_details)

class ACH(BaseModel):
    pass

@router.post('/pay_ach')
def pay_ach():
    pass

@router.post('/pay_wire')
def pay_wire():
    pass

@router.post('/pay_blockchain')
def pay_blockchain():
    pass