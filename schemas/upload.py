from fastapi import UploadFile
from pydantic import BaseModel,EmailStr
class Upload(BaseModel):
    file:UploadFile