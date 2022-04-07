from fastapi import APIRouter
from pydantic import BaseModel
from .logic import QueryDB

query_db = QueryDB()

router = APIRouter(prefix='/invoice', tags=['invoice'])

class Invoice(BaseModel):
    invoice_id:int = None
    client_id:int = None
    invoice_date:str = None
    pay_date:str = None
    client_name:str = None
    client_phone:str = None
    client_email:str = None
    address_1:str = None
    address_2:str = None
    city:str = None
    state:str = None
    zip_code:str = None
    total:float = None

@router.post('/search')
async def get_invoice(invoice: Invoice):
    return query_db.search_invoice(invoice)

@router.post('/create')
async def create_invoice():
    return 'lol'

@router.put('/update')
async def update_invoice():
    return 'lol'