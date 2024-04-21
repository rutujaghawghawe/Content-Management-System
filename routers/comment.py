from fastapi import APIRouter, status, HTTPException, Depends
from routers.authentication import get_current_user
from schemas import Comment, CommentRes
from database import SessionLocal
from typing import List
import models


router= APIRouter(tags=["Comments"], prefix="/comment")

db=SessionLocal()

# Add comment on a post by post id
@router.post('/add/{post_id}', response_model= CommentRes, status_code=status.HTTP_201_CREATED)
def add_comment(post_id: int, comment: Comment, user_id:int = Depends(get_current_user)):
    check=db.query(models.Post).filter(models.Post.post_id==post_id).first()
    if check is not None: 
        new_comment=models.Comment(
                post_id= check.post_id,  
                comment_description = comment.comment_description,
                commenter_id=user_id
        )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment



# List all comments on a post by post id
@router.get('/view_all/{post_id}', response_model=List[CommentRes], status_code=status.HTTP_200_OK)
def get_all_comments_on_a_post(post_id:int, login:int = Depends(get_current_user)):
    if login is not None:
        comments=db.query(models.Comment).filter(models.Comment.post_id==post_id).all()
        return comments



# Delete a comment by comment id
@router.delete('/delete/{comment_id}')
def delete_a_comment(comment_id: int, user_id: int= Depends(get_current_user)):
    comment_to_delete=db.query(models.Comment).filter((models.Comment.comment_id==comment_id) & (models.Comment.commenter_id==user_id)).first()
    if comment_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Either this comment is not yours or it does not exist")
    
    db.delete(comment_to_delete)
    db.commit()
    db.refresh(comment_to_delete)
    return comment_to_delete



# @router.get('/comments', response_model = List[CommentRes], status_code=200)
# def get_all_comments():
#     comments = db.query(models.Comment).all()
#     return comments
