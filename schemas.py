from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime



class User(BaseModel):
    name: str
    username: str
    mobile_number: str
    email_id: str
    password: str
    bio: Optional[str] = None
    
    class Config:
        orm_mode = True

class UpdateUser(BaseModel):
    name: str
    mobile_number: str
    email_id: str
    profile_photo: Optional[int] = None
    bio: Optional[str] = None
    
    class Config:
        orm_mode = True

class UpdateUserRole(BaseModel):
    role: str
    
    class Config:
        orm_mode = True


class ResetPassReq(BaseModel):
    email_id : str
    
    class Config:
        orm_mode = True


class ResetPass(BaseModel):
    #email_id : str
    password :str
    
    class Config:
        orm_mode = True

class UserRes(BaseModel):
    user_id: int
    name: str
    username: str
    mobile_number: str
    email_id: str
    role: Optional[str] = None
    profile_photo: Optional[int] = None
    bio: Optional[str] = None
    #password:str
    
    class Config:
        orm_mode = True       


class UserWithPosts(BaseModel):
    user_id: int
    name: str
    username: str
    mobile_number: str
    email_id: str
    role: Optional[str] = None
    profile_photo: Optional[int] = None
    bio: Optional[str] = None
    posts: List
    #password:str
    
    class Config:
        orm_mode = True    


class UserDetails(BaseModel):
    name: str
    username: str 

    class Config:
        orm_mode = True
    

class CategoryRes(BaseModel):
    category_id: int
    category_name: str
    
    class Config:
        orm_mode = True

        
class Post(BaseModel):
    post_title: str
    post_description: str
    #posted_on: Optional[str] = None
    post_category: int
    media_id: Optional[int] = None


    class Config:
        orm_mode = True


class UpdatePost(BaseModel):
    post_title: str
    post_description: str
    #posted_on: Optional[str] = None
    is_published: bool
    post_category: int
    media_id: Optional[int] = None


    class Config:
        orm_mode = True

class PostRes(BaseModel):
    post_id: int
    posted_by: UserDetails
    post_title: str
    post_description: str
    posted_on: datetime
    is_featured: bool
    media_id: Optional[int] = None
    is_published: bool
    category: CategoryRes
    
    class Config:
        orm_mode = True



class MediaRes(BaseModel):
    media_id: int
    uploader: UserDetails
    link : str
    
    class Config:
        orm_mode = True


class PostWithComments(BaseModel):
    post_id: int
    post_title: str
    post_description: str
    posted_on: datetime
    is_featured: bool
    is_published: bool
    category: CategoryRes
    media_id: Optional[int] = None
    #medias: MediaRes
    posted_by: UserDetails
    comments: List
    

    class Config:
        orm_mode = True        

        


class Comment(BaseModel):
    
    comment_description: str
    #commented_on: Optional[str]= None
    
    class Config:
        orm_mode = True



class CommentRes(BaseModel):
    comment_id: int
    post_id: int
    comment_description: str
    commented_by: UserDetails
    commented_on: datetime
    comment_on_post: PostRes
    
    class Config:
        orm_mode = True
  

class Category(BaseModel):
    category_name: str
    
    class Config:
        orm_mode = True





class PostsOfCategory(BaseModel):
    category_id: int
    category_name: str
    posts: List
    
    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    username:str
    password:str

    class Config:
        orm_mode = True


# class Token(BaseModel):
#     access_token: str
#     token_type: str

#     class Config:
#         orm_mode=True


class TokenData(BaseModel):
    username: Optional[str]= None

    class Config:
        orm_mode=True


