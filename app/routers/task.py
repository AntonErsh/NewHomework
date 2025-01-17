from fastapi import APIRouter, Depends, status, HTTPException
from app.models import Task, User
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated
from app.schemas import CreateTask, UpdateTask, CreateUser
from sqlalchemy import insert, select, update, delete
from slugify import slugify

router = APIRouter(prefix='/task', tags=['task'])


@router.get('/')
async def all_tasks(db: Annotated[Session, Depends(get_db)]):

    all_tasks_db = db.scalars(select(Task)).all()
    return all_tasks_db


@router.get('/task_id')
async def task_by_id(db: Annotated[Session, Depends(get_db)],
                     task_id: int):

    one_task = db.scalar(select(Task).where(Task.id == task_id))
    if one_task:
        return one_task
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task was not found'
        )


@router.post('/create')
async def create_task(db: Annotated[Session, Depends(get_db)],
                      schema_task: CreateTask,
                      user_id: int):

    check_user = db.scalar(select(User).where(User.id == user_id))
    if check_user:
        db.execute(insert(Task).values(title=schema_task.title,
                                       content=schema_task.content,
                                       priority=schema_task.priority,
                                       slug=slugify(schema_task.title),
                                       user_id=user_id))
        db.commit()
        return {'status_code': status.HTTP_201_CREATED,
                'transaction': 'Successful'}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
        )


@router.put('/update')
async def update_task(db: Annotated[Session, Depends(get_db)],
                      schema: UpdateTask,
                      task_id: int):

    task_check = db.scalar(select(Task).where(Task.id == task_id))
    if task_check:
        db.execute(update(Task).where(Task.id == task_id).values(title=schema.title,
                                                                 content=schema.content,
                                                                 priority=schema.priority))
        db.commit()
        return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'Successful'
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task was not found'
        )


@router.delete('/delete')
async def delete_task(db: Annotated[Session, Depends(get_db)],
                      task_id: int):

    task_check = db.scalar(select(Task).where(Task.id == task_id))
    if task_check:
        db.execute(delete(Task).where(Task.id == task_id))
        db.commit()
        return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'Successful'
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task was not found'
        )
