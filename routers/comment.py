from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.database import get_db
from db.db_comment import get_all, create
from auth.oauth2 import get_current_user
from routers.schemas import CommentBase, UserAuth

router = APIRouter(
    prefix='/comment',
    tags=['comment'],
)

@router.get('/all/{post_id}')
def get_post_comments(post_id: int, db: Session = Depends(get_db)):
    return get_all(db, post_id)

@router.post('/')
def create_comment(
    request: CommentBase,
    db: Session = Depends(get_db),
    current_user:UserAuth = Depends(get_current_user)
):
    username = current_user.username
    return create(db, request, username)
