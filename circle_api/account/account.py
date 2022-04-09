from fastapi import APIRouter
from .logic import Connect

connect = Connect()

router = APIRouter(prefix='/account', tags=['account'])

@router.post('/generate_wallet')
def generate_wallet():
    return connect.generate_wallet()