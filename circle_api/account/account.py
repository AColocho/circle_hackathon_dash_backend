from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix='/account', tags=['account'])