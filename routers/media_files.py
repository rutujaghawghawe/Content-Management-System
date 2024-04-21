import os, shutil
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, status
from database import SessionLocal
from typing import List
from schemas import MediaRes
from sqlalchemy import exc
import models
from routers.authentication import get_current_user

router = APIRouter(tags=["Media Library"], prefix="/media_library")
 
db= SessionLocal()

# APIs for Media Library

# View all uploaded files
@router.get('/view_all_files', response_model=List[MediaRes] )
def show_all_media_files(user_id:int = Depends(get_current_user)):
    files = db.query(models.Media).filter(models.Media.user == user_id).all()
    return files



# upload a file and add it to local directory
@router.post('/upload_file', response_model=MediaRes)
def upload_file(file: UploadFile = File(...), user_id:int = Depends(get_current_user)):  
    
    upload_dir = r'F:/Shubhchintak/Projects/Content Management System/routers/uploaded_files/'
    
    # get the destination path
    destination_path = os.path.join(upload_dir, file.filename)
    
    # copying file contents
    with open(destination_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    # wb means write and binary
    

    db_file = db.query(models.Media).filter((models.Media.link == destination_path) & (models.Media.user == user_id)).first()
    if db_file is not None:
        raise HTTPException(status_code=400, detail="Media File already exists")
    

    new_media = models.Media(
        link = destination_path ,
        user = user_id
    )

    db.add(new_media)
    db.commit()
    db.refresh(new_media)
    
    return new_media



# delete media
@router.delete("/delete/{media_id}")
def delete_media_file(media_id: int, user_id:int = Depends(get_current_user)):
    media_to_delete=db.query(models.Media).filter((models.Media.media_id == media_id) & (models.Media.user == user_id)).first()
    
    if media_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Either the media file does not exist or you are not the owner of this media file")
    
    try:
        # before deleting media file, make the media attributes of all the posts containing that media file as null
        post_containing_media = db.query(models.Post).filter(models.Post.media_id == media_id).all()
        
        for i in range(len(post_containing_media)):
            post_containing_media[i].media_id == None
            
        db.delete(media_to_delete)
        db.commit()
        db.refresh(media_to_delete)
        
    except exc.InvalidRequestError:
        raise HTTPException(status_code=status.HTTP_200_OK, detail="Media File deleted successfully")
    
    
    db.delete(media_to_delete)
    db.commit()
    db.refresh(media_to_delete)
    return media_to_delete