from database import Base
from sqlalchemy import String, Integer, Boolean, Column, Text, TIMESTAMP, ForeignKey, text
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__="users"
    
    user_id=Column(Integer,primary_key=True)
    name=Column(String(255),nullable=False)
    username=Column(String(255),nullable=False,unique=True)
    mobile_number=Column(String(10), nullable=False)
    email_id=Column(String(60), nullable=False)
    password=Column(String(255), nullable=False)
    role=Column(String(20), default="author")
    bio=Column(Text)

    profile_photo=Column(Integer, ForeignKey("media_files.media_id"), nullable=True)

    profile_pic = relationship("Media", foreign_keys=[profile_photo])

    posts= relationship("Post", back_populates= "posted_by")
    comments= relationship("Comment", back_populates="commented_by")
    #media_files = relationship("Media", back_populates="user_medias")

    def __repr__(self):
        return f"<User={self.username}>"
    


class Post(Base):
    __tablename__ = "posts"

    post_id= Column(Integer, primary_key=True)
    post_title= Column(String(255), nullable=False)
    post_description= Column(Text)
    posted_on= Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))
    is_featured= Column(Boolean, default=False)
    is_published = Column(Boolean,default=True) 

    author_id=Column(Integer,ForeignKey("users.user_id")) 
    post_category = Column(Integer, ForeignKey("categories.category_id"))
    media_id= Column(Integer,ForeignKey("media_files.media_id"), nullable=True)

    posted_by= relationship("User", back_populates="posts") 
    comments= relationship("Comment", back_populates="comment_on_post")
    category = relationship("Category", back_populates="posts")
    medias = relationship("Media", back_populates="posts")

    def __repr__(self):
        return f"<Post Title={self.post_title} Posted By={self.posted_by}>"  
    



class Comment(Base):
    __tablename__ = "comments"

    comment_id= Column(Integer, primary_key=True)
    comment_description= Column(Text)
    commented_on= Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))

    commenter_id= Column(Integer, ForeignKey("users.user_id"))
    post_id= Column(Integer, ForeignKey("posts.post_id")) 

    commented_by= relationship("User", back_populates="comments")
    comment_on_post= relationship("Post", back_populates= "comments")




class Category(Base):
    __tablename__ = "categories"

    category_id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String(50), nullable=False, unique=True)
    
    posts = relationship("Post", back_populates="category")


    
    
class Media(Base):
    __tablename__ = "media_files"
    media_id = Column(Integer, primary_key=True, index=True)
    link = Column(String(255), nullable=False)

    user = Column(Integer, ForeignKey("users.user_id"))

    uploader = relationship("User", foreign_keys=[user], backref="media_files")
    
    posts = relationship("Post", back_populates="medias")
   # user_medias = relationship("User", back_populates="media_files")
