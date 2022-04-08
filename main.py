from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from accounts_receivable.clients import client
from accounts_receivable.invoice import invoice

app = FastAPI()

app.include_router(client.router)
app.include_router(invoice.router)
origins = [
    "http://localhost:3000/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=[""],
    allow_headers=[""],
)