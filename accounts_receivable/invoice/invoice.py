from fastapi import APIRouter
from pydantic import BaseModel
from .logic import QueryDB

query_db = QueryDB()

router = APIRouter(prefix='/invoice', tags=['invoice'])

@router.get('/all')
async def get_all():
    return query_db.get_all()

class SearchInvoice(BaseModel):
    invoice_id:int = None
    client_id:int = None
    pay_date:str = None
    total:float = None
    status:str = None

@router.post('/search')
async def get_invoice(invoice:SearchInvoice):
    return query_db.search_invoice(invoice)

class CreateInvoice(BaseModel):
    client_id:int
    pay_date:str
    line_items:list
    total:float
    status:str

@router.post('/create')
async def create_invoice(invoice:CreateInvoice):
    query_db.create_invoice(invoice)

class UpdateInvoice(BaseModel):
    invoice_id:int
    client_id:int
    pay_date:str
    line_items:list
    total:float
    status:str
    
@router.put('/update')
async def update_invoice(invoice:UpdateInvoice):
    """
    status - "g":generated, "d":draft, "p":paid, "v":void
    """
    query_db.update_invoice(invoice)