from fastapi import APIRouter, HTTPException, Request, UploadFile,Depends

from controllers.upload import *
from schemas.upload import Upload
upload_controller=UploadController()
upload=APIRouter(prefix="/upload")



@upload.post('/send-photo')

def send_photo(request:Request,file:UploadFile):
    
    rpta=upload_controller.send_photo(request,file)
    return rpta