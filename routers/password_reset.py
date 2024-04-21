from fastapi import APIRouter, HTTPException, status, Depends
from database import SessionLocal
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from jose import JWTError, jwt
from schemas import ResetPass, ResetPassReq
import models
from routers.register import pwd_cxt
from routers.authentication import create_access_token

router = APIRouter(tags=["Login"])

db = SessionLocal()

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 100



def verify_token(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email_id : str = payload.get("sub")
    
        if email_id is None:
            raise credentials_exception
    
    except JWTError:
        raise credentials_exception

    return email_id 





def send_email(to_email, token):

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login("rutuja.ghawghawe.stpl.2023@gmail.com", "jmqandzvazkgdcjn")

    msg = MIMEMultipart()
    msg["From"] = "rutuja.ghawghawe.stpl.2023@gmail.com"
    msg["To"] = to_email
    msg["Subject"] = "Password reset"
    msg.attach(MIMEText(f"Please click the following link to reset your password: http://localhost:8000/reset-password?token={token}", "plain"))

    server.sendmail("rutuja.ghawghawe.stpl.2023@gmail.com", to_email, msg.as_string())
    server.quit()





@router.post("/reset-password-request", status_code=status.HTTP_200_OK)
def reset_password_request(email: ResetPassReq):

    user=db.query(models.User).filter(models.User.email_id==email.email_id).first() 
    if user is None:
        raise HTTPException(status_code=404, detail="You are not a registered user.")
    
    token = create_access_token(data={"sub": user.email_id})
   
    send_email(user.email_id, token)
    return {"message": "Password reset successfully."}





@router.post("/reset-password")
def reset_password(reset: ResetPass, token: str, email: str):  

    user = db.query(models.User).filter(models.User.email_id == email).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    
    token_email = verify_token(token)

    if token_email != email:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid token.")

    hashed_pwd= pwd_cxt.hash(reset.password)
    user=db.query(models.User).filter(models.User.email_id == token_email).first()

    user.password = hashed_pwd

    db.commit()
    db.refresh(user)
    return {"message": "Password reset successfully."}


