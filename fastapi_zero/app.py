from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from fastapi_zero.database import get_session
from fastapi_zero.models import User
from fastapi_zero.schemas import Message, UserList, UserPublic, UserSchema

app = FastAPI()

database = []


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Hello, World!'}


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session=Depends(get_session)):

    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )
    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail='Username already registered'
            )
        if db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail='Email already registered'
            )
    db_user = User(
        username=user.username,
        email=user.email,
        password=user.password,
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserList)
def read_users(session=Depends(get_session), limit: int = 10, offset: int = 0):
    users = session.scalars(select(User).offset(offset).limit(limit))
    return {'users': users}


@app.get('/users/{user_id}/', status_code=HTTPStatus.OK, response_model=UserPublic)
def read_user_by_id(user_id: int, session=Depends(get_session)):
    user = session.scalar(select(User).where(User.id == user_id))

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found',
        )

    return user


@app.put('/users/{user_id}/', status_code=HTTPStatus.OK, response_model=UserPublic)
def update_user(user_id: int, user: UserSchema, session=Depends(get_session)):
    user_db = session.scalar(select(User).where(User.id == user_id))

    if not user_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')

    try:
        user_db.username = user.username
        user_db.email = user.email
        user_db.password = user.password

        session.add(user_db)
        session.commit()
        session.refresh(user_db)
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or email already registered',
        )

    return user_db


@app.delete('/users/{user_id}/', status_code=HTTPStatus.OK, response_model=Message)
def delete_user(user_id: int, session=Depends(get_session)):
    user_db = session.scalar(select(User).where(User.id == user_id))
    if not user_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')

    session.delete(user_db)
    session.commit()

    return {'message': 'User deleted'}
