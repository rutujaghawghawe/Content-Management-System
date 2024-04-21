from fastapi import APIRouter, status, HTTPException, Depends
from routers.authentication import get_current_user
from schemas import Category, CategoryRes, PostsOfCategory
from database import SessionLocal
from typing import List
import models


router= APIRouter(tags=["Categories"], prefix="/category")

db=SessionLocal()




# Create a category
@router.post('/add', response_model=CategoryRes, status_code=status.HTTP_201_CREATED)
def create_category(category: Category, login:int = Depends(get_current_user)):
    if login is not None:
        new_category = models.Category(
            category_name= category.category_name
        )

        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return new_category




# List all categories
@router.get('/view_all', response_model=List[CategoryRes])
def get_all_categories(login:int = Depends(get_current_user)):
    if login is not None:
        categories = db.query(models.Category).all()
        return categories




# # Delete a category
# @router.delete('/category/{category_id}')
# def delete_a_category(category_id: int):
#     category_to_delete = db.query(models.Category).filter(models.Category.category_id == category_id).first()
#     if category_to_delete is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category does not exist")
    
#     db.delete(category_to_delete)
#     db.commit()
#     db.refresh(category_to_delete)
#     return category_to_delete



# Search posts by category id
@router.get('/search/{category_id}', response_model=PostsOfCategory, status_code=status.HTTP_200_OK)
def search_post_by_a_category(category_id:int, login:int = Depends(get_current_user)):
    if login is not None:
        posts=db.query(models.Category).filter(models.Category.category_id==category_id).first()
        return posts