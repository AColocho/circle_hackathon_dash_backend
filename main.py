from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from accounts_receivable.clients import client
from accounts_receivable.invoice import invoice
from circle_api.payments import payments
from circle_api.account import account

app = FastAPI()

app.include_router(client.router)
app.include_router(invoice.router)
app.include_router(payments.router)
app.include_router(account.router)

origins = ["http://localhost:3000/"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=[""],
    allow_headers=[""],
)