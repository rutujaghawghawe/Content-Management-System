from fastapi import APIRouter, status, HTTPException,Depends
from routers.authentication import get_current_user
from schemas import  UserRes, UpdateUser, UserWithPosts
from database import SessionLocal
from typing import List
import models
from sqlalchemy import exc 



router= APIRouter(tags=["User"], prefix="/user")

db=SessionLocal()



# List all Users
@router.get('/view_all', response_model=List[UserRes], status_code=200)
def get_all_users(login:int = Depends(get_current_user)):
    if login is not None:
        users=db.query(models.User).all()
        return users




# Search a user by username with posts
@router.get('/view/{username}', response_model=UserWithPosts, status_code=status.HTTP_200_OK)
def get_an_user_with_posts(username:str, login:int = Depends(get_current_user)):
    if login is not None:
        user=db.query(models.User).filter(models.User.username==username).first()
        return user



# Search a user by username with posts
@router.get('/view_my_profile', response_model=UserWithPosts, status_code=status.HTTP_200_OK)
def get_my_profile_with_posts(user_id:int = Depends(get_current_user)):
    user=db.query(models.User).filter(models.User.user_id==user_id).first()
    return user
    


# Update an user
@router.put('/edit_profile', response_model=UserRes, status_code=status.HTTP_200_OK)
def update_an_user(user:UpdateUser, user_id:int = Depends(get_current_user)):
    user_to_update=db.query(models.User).filter(models.User.user_id ==user_id).first()

    user_to_update.name=user.name
    user_to_update. mobile_number=user.mobile_number
    user_to_update.email_id=user.email_id
    user_to_update.profile_photo=user.profile_photo
    user_to_update.bio=user.bio

    db.commit()
    db.refresh(user_to_update)
    return user_to_update




# Delete an user by username
@router.delete('/delete_profile')
def delete_an_user(user_id:int = Depends(get_current_user)):

    posts_of_a_user = db.query(models.Post).filter(models.Post.author_id == user_id).all()

    try:
        for i in range(len(posts_of_a_user)):
            for j in range(len(posts_of_a_user[i].comments)):
                db.delete(posts_of_a_user[i].comments[j])
        db.delete(posts_of_a_user[i])

        print("Deleted all the posts along with comments")


        db.query(models.Comment).filter(models.Comment.commenter_id == user_id).delete()
        print("Deleted all the comments made by me")

        user_to_delete=db.query(models.User).filter(models.User.user_id==user_id).first()
        
        db.delete(user_to_delete)
        db.commit()
        db.refresh(user_to_delete)

    except exc.InvalidRequestError:
        raise HTTPException(status_code=status.HTTP_200_OK, detail="User deleted successfully")
    




 
        
  