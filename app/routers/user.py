from fastapi import APIRouter, Depends, status, HTTPException
from app.models import User
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated
from app.schemas import CreateUser, UpdateUser
from sqlalchemy import insert, select, update, delete
from slugify import slugify

router = APIRouter(prefix='/user', tags=['user'])


@router.get('/')
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users_db = db.scalars(select(User)).all()
    return users_db


@router.get('/user_id')
async def user_by_id(db: Annotated[Session, Depends(get_db)],
                     user_id: int):

    one_user = db.scalar(select(User).where(User.id == user_id))
    if one_user is not None:
        return one_user
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
        )


@router.post('/create')
async def create_user(db: Annotated[Session, Depends(get_db)],
                      model: CreateUser):

    db.execute(insert(User).values(username=model.username,
                                   firstname=model.firstname,
                                   lastname=model.lastname,
                                   age=model.age,
                                   slug=slugify(model.username)))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful'}


@router.put('/update')
async def update_user(db: Annotated[Session, Depends(get_db)],
                      schema: UpdateUser,
                      user_id: int):

    user_check = db.scalar(select(User).where(User.id == user_id))
    if user_check:
        db.execute(update(User).where(User.id == user_id).values(firstname=schema.firstname,
                                                                 lastname=schema.lastname,
                                                                 age=schema.age))
        db.commit()
        return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'Successful'
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
        )


@router.delete('/delete')
async def delete_user(db: Annotated[Session, Depends(get_db)],
                      user_id: int):

    user_check = db.scalar(select(User).where(User.id == user_id))
    if user_check:
        db.execute(delete(User).where(User.id == user_id))
        db.commit()
        return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'Successful'
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
        )
