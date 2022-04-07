from fastapi import APIRouter
from pydantic import BaseModel
from .logic import QueryDB

query_db = QueryDB()

router = APIRouter(prefix='/client', tags=['client'])

class SearchClient(BaseModel):
    client_id:int = None
    name:str = None
    phone:str = None
    address_1:str = None
    city:str = None
    state:str = None
    client_email:str = None
    
@router.post('/search')
async def get_client(client:SearchClient):
    return query_db.search_client(client)

class Client(BaseModel):
    client_id:int
    name:str
    phone:str
    address_1:str
    address_2:str = None
    city:str
    state:str
    zipcode:str
    client_email:str

@router.post('/create')
async def create_client(client:Client):
    query_db.create_client(client)

@router.put('/update')
async def update_client(client:Client):
    query_db.update_client(client)
