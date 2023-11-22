from fastapi import Request, UploadFile
import requests
import mysql.connector
from schemas.upload import Upload
from utils.Security import Security
from config.db_config import get_db_connection



# modelAdmin=ModelUpload()

class UploadController:
    def send_photo(self,request:Request,photo:UploadFile):
        headers=request.headers
        payload=Security.verify_token(headers)
        id_usuario=payload['id_usuario']
        print(id_usuario)
        bd=get_db_connection()
        cursor=bd.cursor()
        response=requests.post('https://fastapi-pwqp-production.up.railway.app/upload/upload-file',
        files={'file': (photo.filename, photo.file)})
        if (response.status_code==200):
            foto=response.json()['path']
            print(foto)
            cursor.execute('update usuarios set foto=%s where id_usuario=%s',(foto,id_usuario))
            bd.commit()

            return response.json()
        else:
            return response.json()