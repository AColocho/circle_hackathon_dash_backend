import email
from fastapi import APIRouter
from pydantic import BaseModel
from .logic import SendEmail

se = SendEmail()

router = APIRouter(prefix='/admin', tags=['admin'])

class Email(BaseModel):
    email: str
    invoice_url: str

@router.put('/send_email')
def send_email(email:Email):
    data = email.dict()
    try:
        se.send_message(data['invoice_url'],data['email'])
    except:
        pass