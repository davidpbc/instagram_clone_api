from fastapi import HTTPException, status
from sqlalchemy.orm.session import Session
from datetime import datetime

from db.models import DbPost
from routers.schemas import PostBase


def create(db: Session, request: PostBase, uid: int):
    new_post = DbPost(
        image_url=request.image_url,
        image_url_type=request.image_url_type,
        caption=request.caption,
        timestamp=datetime.now(),
        user_id=uid,
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

def get_all(db: Session):
    return db.query(DbPost).all()

def delete(db: Session, id: int, uid: int):
    post = db.query(DbPost).filter(DbPost.id == id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Post with id {id} not found.'
        )

    if post.user_id != uid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Only post creator can delete post.'
        )

    db.delete(post)
    db.commit()
    return 'ok'
