from fastapi import HTTPException, status
from sqlalchemy.orm.session import Session

from db.models import DbUser
from db.hashing import Hash
from routers.schemas import UserBase

def create_user_db(db: Session, request: UserBase):
    # Check if username exists
    if get_user_by_username(db, request.username, frontend=False):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'User with username {request.username} already exists'
        )
    # Check if email exists
    if get_user_by_email(db, request.email, frontend=False):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'User with email {request.email} already exists'
        )
    # Create user
    new_user = DbUser(
        username=request.username,
        email=request.email,
        password=Hash.bcrypt(request.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_by_username(db: Session, username: str, frontend=True):
    user = db.query(DbUser).filter(DbUser.username == username).first()
    if not user:
        if frontend:
             raise HTTPException(
                 status_code=status.HTTP_404_NOT_FOUND,
                 detail=f'User with username {username} not found'
             )
        else:
            return False
    return user

def get_user_by_email(db: Session, email: str, frontend=True):
    user = db.query(DbUser).filter(DbUser.email == email).first()
    if not user:
        if frontend:
            raise HTTPException(
                 status_code=status.HTTP_404_NOT_FOUND,
                 detail=f'User with email {email} not found'
             )
        else:
            return False
    return user
