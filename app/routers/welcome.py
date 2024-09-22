from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database.db import get_session


router = APIRouter(prefix="", tags=["Welcome"])

@router.get('', status_code=200)
async def welcome(session: Session = Depends(get_session)):
    return {"message": "API funcionando!"}