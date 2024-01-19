from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from bot.database import get_db

from bot.main import create_user, get_user, update, remove
from bot.dto import users as UserDTO

router = APIRouter()


@router.post('/', tags=['user'])
async def create(data: UserDTO = None, db: Session = Depends(get_db)):
    return create_user(data, db)


@router.get('/{id}', tags=['user'])
async def get(id: int = None, db: Session = Depends(get_db)):
    return get_user(db, id)


@router.put('/{id}', tags=['user'])
async def put(id: int = None, data: UserDTO.User = None, db: Session = Depends(get_db)):
    return update(data, db, id )


@router.delete('/{id}', tags=["user"])
async def delete(id: int = None, db: Session = Depends(get_db)):
    return remove(id, db)
