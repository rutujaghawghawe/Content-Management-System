from fastapi import APIRouter, status, HTTPException
from schemas import User, UserRes
from database import SessionLocal
import models
from passlib.context import CryptContext


router= APIRouter(tags=["Register"])

db=SessionLocal()

pwd_cxt=CryptContext(schemes=["bcrypt"], deprecated="auto")



# Register an user
@router.post('/register', response_model=UserRes, status_code=status.HTTP_201_CREATED)
def register_an_user(user:User):
    db_user=db.query(models.User).filter(models.User.username==user.username).first()
    if db_user is not None:
        raise HTTPException(status_code=400, detail="User account already exists")
    
    hashed_pwd= pwd_cxt.hash(user.password)
    new_user=models.User(
        name=user.name,
        username=user.username,
        mobile_number=user.mobile_number,
        email_id=user.email_id,
        password=hashed_pwd,
        bio=user.bio
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user 




