from fastapi import APIRouter, status, HTTPException, Depends
from routers.authentication import get_current_user
from schemas import PostRes, Post, PostWithComments, UpdatePost
from database import SessionLocal
from typing import List
import models
from sqlalchemy import exc 

router= APIRouter(tags=["Posts"], prefix="/post")

db=SessionLocal()




# Create a post
@router.post('/create', response_model= PostRes, status_code=status.HTTP_201_CREATED)
def create_post( post: Post, user_id:int = Depends(get_current_user)):
    
    new_post=models.Post(
            author_id= user_id,
            post_title = post.post_title,
            post_description = post.post_description,
            post_category= post.post_category,
            media_id= post.media_id
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post





# List all posts
@router.get('/view_all', response_model = List[PostRes], status_code=200)
def get_all_posts(login:int = Depends(get_current_user)):
    if login is not None:
        posts = db.query(models.Post).filter(models.Post.is_published==True).all()
        return posts




@router.get('/featured', response_model=List[PostRes])
def list_all_featured_posts(login:int = Depends(get_current_user)):
    if login is not None:
        featured_posts = db.query(models.Post).filter(models.Post.is_featured==True).all()
        return featured_posts


# # List all posts of a user by user id
# @router.get('/view_all/{user_id}', response_model=List[PostRes], status_code=status.HTTP_200_OK)
# def get_all_posts_of_a_user(user_id:int, login:int = Depends(get_current_user)):
#     if login is not None:
#         posts=db.query(models.Post).filter(models.Post.author_id==user_id).all()
#         return posts



# View a post by post id with comments
@router.get('/{post_id}', response_model=PostWithComments, status_code=status.HTTP_200_OK)
def view_a_post_with_comments(post_id:int, login:int = Depends(get_current_user)):
    if login is not None:
        post=db.query(models.Post).filter(models.Post.post_id==post_id).first()
        if post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "The post does not exist")
        return post





# Update a post by post id
@router.put('/update/{post_id}', response_model=PostRes, status_code=status.HTTP_200_OK)
def update_a_post(post:UpdatePost, post_id: int, user_id: int= Depends(get_current_user)):    
    post_to_update = db.query(models.Post).filter((models.Post.post_id == post_id) & (models.Post.author_id==user_id)).first()

    if post_to_update is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not allowed to edit someone else's post")

    post_to_update.post_title = post.post_title
    post_to_update.post_description = post.post_description
    post_to_update.is_published = post.is_published
    post_to_update.post_category = post.post_category
    post_to_update.media_id= post.media_id

    db.commit()
    db.refresh(post_to_update)
    return post_to_update





# Delete a post by post id
@router.delete('/delete/{post_id}')
def delete_a_post(post_id: int, user_id: int= Depends(get_current_user)):
    post_to_delete=db.query(models.Post).filter((models.Post.post_id==post_id) & (models.Post.author_id==user_id)).first()
    if post_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Either you're not an author of this post or the post does not exist")
    
    try:
        db.query(models.Comment).filter(models.Comment.post_id == post_id).delete()
    
        db.delete(post_to_delete)
        db.commit()
        db.refresh(post_to_delete)
    
    except exc.InvalidRequestError:
        raise HTTPException(status_code=status.HTTP_200_OK, detail="Post deleted successfully")



# Delete a post by post id
# @router.delete('/delete/{post_id}')
# def delete_a_post(post_id: int):
#     post_to_delete=db.query(models.Post).filter((models.Post.post_id==post_id)).first()
#     if post_to_delete is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Either you're not an author of this post or the post doesn't exist")
    
#     db.delete(post_to_delete)
#     db.commit()
#     db.refresh(post_to_delete)
#     return post_to_delete