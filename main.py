from fastapi import FastAPI
from  routers import user, post, comment, category, admin, authentication, register, password_reset, media_files

app = FastAPI()

app.include_router(register.router)
app.include_router(password_reset.router)
app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(post.router)
app.include_router(comment.router)
app.include_router(category.router)
app.include_router(admin.router)
app.include_router(media_files.router)



# # List all Users
# @app.get('/users', response_model=List[UserRes], status_code=200)
# def get_all_users():
#     users=db.query(models.User).all()
#     return users


# # Search a user by username
# @app.get('/user/{username}', response_model=UserRes, status_code=status.HTTP_200_OK)
# def get_an_user(username:str):
#     user=db.query(models.User).filter(models.User.username==username).first()
#     return user


# # Register an user

# pwd_cxt=CryptContext(schemes=["bcrypt"], deprecated="auto")

# @app.post('/user', response_model=UserRes, status_code=status.HTTP_201_CREATED)
# def create_an_user(user:User):
#     db_user=db.query(models.User).filter(models.User.name==user.name).first()
#     if db_user is not None:
#         raise HTTPException(status_code=400, detail="User account already exists")
    
#     hashed_pwd= pwd_cxt.hash(user.password)
#     new_user=models.User(
#         name=user.name,
#         username=user.username,
#         mobile_number=user.mobile_number,
#         email_id=user.email_id,
#         password=hashed_pwd,
#         profile_photo=user.profile_photo,
#         bio=user.bio
#     )

#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user 


# # Update an user by username
# @app.put('/user/{username}', response_model=UserRes, status_code=status.HTTP_200_OK)
# def update_an_user(username:str, user:UpdateUser):
#     user_to_update=db.query(models.User).filter(models.User.username==username).first()

#     user_to_update.name=user.name
#     user_to_update.username=user.username
#     user_to_update. mobile_number=user.mobile_number
#     user_to_update.email_id=user.email_id
#     user_to_update.profile_photo=user.profile_photo
#     user_to_update.bio=user.bio

#     db.commit()
#     db.refresh(user_to_update)
#     return user_to_update


# # Delete an user by username
# @app.delete('/user/{username}')
# def delete_an_user(username:str):
#     user_to_delete=db.query(models.User).filter(models.User.username==username).first()
#     if user_to_delete is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")
    
#     db.delete(user_to_delete)
#     db.commit()
#     db.refresh(user_to_delete)
#     return user_to_delete





# # Create a post
# @app.post('/post/{user_id}', response_model= PostRes, status_code=status.HTTP_201_CREATED)
# def create_post(user_id:int, post: Post):
    
#     new_post=models.Post(
#             author_id= user_id,
#             post_title = post.post_title,
#             post_description = post.post_description,
#             posted_on= post.posted_on,
#             post_category= post.post_category,
#             media_id= post.media_id
#     )
#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)
#     return new_post


# # List all posts
# @app.get('/posts', response_model = List[PostRes], status_code=200)
# def get_all_posts():
#     posts = db.query(models.Post).all()
#     return posts


# # List all posts of a user by user id
# @app.get('/posts/{user_id}', response_model=List[PostRes], status_code=status.HTTP_200_OK)
# def get_all_posts_of_a_user(user_id:int):
#     posts=db.query(models.Post).filter(models.Post.author_id==user_id).all()
#     return posts


# # View a post by post id with comments
# @app.get('/post/{post_id}', response_model=PostWithComments, status_code=status.HTTP_200_OK)
# def view_a_post(post_id:int):
#     post=db.query(models.Post).filter(models.Post.post_id==post_id).first()
#     return post


# # Update a post by post id
# @app.put('/post/{post_id}', response_model=PostRes, status_code=status.HTTP_200_OK)
# def update_a_post(post_id: int, post:UpdatePost):    
#     post_to_update = db.query(models.Post).filter(models.Post.post_id == post_id).first()

#     post_to_update.post_title = post.post_title
#     post_to_update.post_description = post.post_description
#     post_to_update.is_published = post.is_published
#     post_to_update.post_category = post.post_category
#     post_to_update.media_id= post.media_id

#     db.commit()
#     db.refresh(post_to_update)
#     return post_to_update


# # Delete a post by post id
# @app.delete('/post/{post_id}')
# def delete_a_post(post_id: int):
#     post_to_delete=db.query(models.Post).filter(models.Post.post_id==post_id).first()
#     if post_to_delete is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist")
    
#     db.delete(post_to_delete)
#     db.commit()
#     db.refresh(post_to_delete)
#     return post_to_delete




# # Add comment on a post by post id
# @app.post('/comment/{post_id}', response_model= CommentRes, status_code=status.HTTP_201_CREATED)
# def add_comment(post_id: int, comment: Comment):
#     check=db.query(models.Post).filter(models.Post.post_id==post_id).first()
#     if check is not None: 
#         new_comment=models.Comment(
#                 post_id= check.post_id,  
#                 comment_description = comment.comment_description,
#                 commented_on= comment.commented_on,
#                 commenter_id=comment.commenter_id
#         )
#     db.add(new_comment)
#     db.commit()
#     db.refresh(new_comment)
#     return new_comment



# # List all comments on a post by post id
# @app.get('/comments/{post_id}', response_model=List[CommentRes], status_code=status.HTTP_200_OK)
# def get_all_comments_on_a_post(post_id:int):
#     comments=db.query(models.Comment).filter(models.Comment.post_id==post_id).all()
#     return comments



# # Delete a comment by comment id
# @app.delete('/comment/{comment_id}')
# def delete_a_comment(comment_id: int):
#     comment_to_delete=db.query(models.Comment).filter(models.Comment.comment_id==comment_id).first()
#     if comment_to_delete is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment does not exist")
    
#     db.delete(comment_to_delete)
#     db.commit()
#     db.refresh(comment_to_delete)
#     return comment_to_delete



# # @app.get('/comments', response_model = List[CommentRes], status_code=200)
# # def get_all_comments():
# #     comments = db.query(models.Comment).all()
# #     return comments





# # Create a category
# @app.post('/category', response_model=CategoryRes)
# def create_category(category: Category):

#     new_category = models.Category(
#         category_name= category.category_name
#     )

#     db.add(new_category)
#     db.commit()
#     db.refresh(new_category)
#     return new_category



# # List all categories
# @app.get('/categories', response_model=List[CategoryRes])
# def get_all_categories():
#     categories = db.query(models.Category).all()
#     return categories




# # Delete a category
# @app.delete('/category/{category_id}')
# def delete_a_category(category_id: int):
#     category_to_delete = db.query(models.Category).filter(models.Category.category_id == category_id).first()
#     if category_to_delete is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category does not exist")
    
#     db.delete(category_to_delete)
#     db.commit()
#     db.refresh(category_to_delete)
#     return category_to_delete



# # Search posts by category id
# @app.get('/search/posts/{category_id}', response_model=PostsOfCategory, status_code=status.HTTP_200_OK)
# def view_all_posts_of_a_category(category_id:int):
#     posts=db.query(models.Category).filter(models.Category.category_id==category_id).first()
#     return posts


# # Mark as a featured post
# @app.put('/admin/feature_post/{post_id}', response_model= PostRes)
# def mark_as_featured(post_id: int):
#     post_to_mark = db.query(models.Post).filter(models.Post.post_id == post_id).first()
#     if post_to_mark.is_featured == False:
#         post_to_mark.is_featured = True

#     db.commit()
#     db.refresh(post_to_mark)
#     return post_to_mark


# # show all featured posts
# @app.get('/posts/is_featured/{value}', response_model=List[PostRes])
# def list_all_featured_posts(value: bool):
#     featured_posts = db.query(models.Post).filter(models.Post.is_featured==value).all()
#     return featured_posts


# # Change role of a user
# @app.put('/admin/change_role/{user_id}', response_model= UserRes)
# def change_role_of_a_user(user_id: int, user:UpdateUserRole):
#     role_to_change = db.query(models.User).filter(models.User.user_id == user_id).first()
    
#     role_to_change.role=user.role

#     db.commit()
#     db.refresh(role_to_change)
#     return role_to_change