from fastapi import APIRouter, status, HTTPException, Depends
from routers.authentication import get_current_user
from schemas import PostRes, UserRes, UpdateUserRole
from database import SessionLocal
from typing import List
import models


router= APIRouter(tags=["Admin"])

db=SessionLocal()



# Mark as a featured post
@router.put('/admin/feature_post/{post_id}', response_model= PostRes)
def mark_as_featured(post_id: int, current: int = Depends(get_current_user)):

    current_user = db.query(models.User).filter(models.User.user_id == current).first()
    post_to_mark = db.query(models.Post).filter((models.Post.post_id == post_id)  & (current_user.role=="admin")).first()
    if post_to_mark is not None:
        
        if post_to_mark.is_featured == False:
            post_to_mark.is_featured = True

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You don't have authority to mark a post as featured.")

    db.commit()
    db.refresh(post_to_mark)
    return post_to_mark




# Change role of a user
@router.put('/admin/change_role/{username}', response_model= UserRes)
def change_role_of_a_user(username: str, user:UpdateUserRole, current: int = Depends(get_current_user)):
    current_user = db.query(models.User).filter(models.User.user_id == current).first()
    role_to_change = db.query(models.User).filter((models.User.username == username) & (current_user.role=="admin")).first()
    if role_to_change is not None:
        role_to_change.role=user.role
    
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You don't have authority to update role of any user")
    
    db.commit()
    db.refresh(role_to_change)
    return role_to_change



# show all featured posts
# @router.get('/posts/is_featured/{value}', response_model=List[PostRes])
# def list_all_featured_posts(value: bool):
#     featured_posts = db.query(models.Post).filter(models.Post.is_featured==value).all()
#     return featured_posts


# # List users based on their roles
# @router.get('/view_all/{role}', response_model=List[UserRes], status_code=200)
# def get_all_users(role:str, login:int = Depends(get_current_user)):
#     if login is not None:
#         users=db.query(models.User).filter(models.User.role == role) .all()
#         return users


# @router.put('/admin/change_role/{username}', response_model= UserRes)
# def change_role_of_a_user(username: str, user:UpdateUserRole):
  
#     role_to_change = db.query(models.User).filter(models.User.username == username).first()
#     if role_to_change is not None:
#         role_to_change.role=user.role
    
#     db.commit()
#     db.refresh(role_to_change)
#     return role_to_change