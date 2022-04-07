from fastapi import FastAPI
from accounts_receivable.clients import client
from accounts_receivable.invoice import invoice

app = FastAPI()

app.include_router(client.router)
app.include_router(invoice.router)