from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
import requests
from utils.utils import Hasher
from schemas.Materia import Materia
from config.db_config import get_db_connection
import mysql.connector

class ModelUser:
    def verificar_agendamiento(id_tutoria:int,id_usuario:int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            sql="select count(*) from lista_estudiantes where id_usuario=%s and id_tutoria=%s"
            cursor.execute(sql,(id_usuario,id_tutoria))
            print(sql)
            tutoria_agendada=cursor.fetchone()[0]
            print(tutoria_agendada)
            return tutoria_agendada
        except mysql.connector.Error as err:
            print(err)
            conn.rollback()
            return ({"error": "el horario ya existe en el programa"})
        finally:
            conn.close()
    def agendar_tutoria(id_tutoria:int,id_usuario:int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            sql="insert into lista_estudiantes (id_tutoria,id_usuario,asistencia) values (%s,%s,%s)"
            cursor.execute(sql,(id_tutoria,id_usuario,0))
            conn.commit()
            conn.close()
            return {"message":"la tutoria ha sido agendada con exito"}
        except mysql.connector.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()
    def actualizarCupos(id_tutoria):
         try:
            conn = get_db_connection()
            cursor = conn.cursor()
            sql="update horario_tutorias set cupos=cupos-1  where id_tutoria=%s"
            cursor.execute(sql,(id_tutoria,))
            
            conn.commit()
            conn.close()
         except mysql.connector.Error as err:
            print(err)
            conn.rollback()
         finally:
            conn.close()
    def obtenerTutoriasPendientes(user_id:int):
     try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
SELECT ht.id_tutoria,f.facultad,p.programa,m.materia ,s.salon,le.id_usuario,txe.estado,ht.cupos,ht.tema,ht.fecha,ht.hora_inicial,ht.hora_final,u.nombres,u.apellidos  FROM `horario_tutorias` ht 
join lista_estudiantes le on le.id_tutoria=ht.id_tutoria
join salones s on ht.id_salon=s.id_salon
join tipoxestado txe on ht.id_estado_tutoria=txe.id_tipoxestado 
join fpxmateria fpxm on fpxm.id_fpxm=ht.id_fpxm
join facultadxprograma fxp on fxp.id_fxp=fpxm.id_fxp
join facultades f on f.id_facultad=fxp.id_facultad
join programas p on p.id_programa=fxp.id_programa
join materias m on m.id_materia=fpxm.id_materia
join usuarios u on u.id_usuario=ht.id_usuario
where txe.id_tipoxestado=6 and le.id_usuario=%s
""",(user_id,))
            result = cursor.fetchall()
            print(result)
            payload = []
            content = {}
            for data in result:
                content = {
                       'id':data[0],
                       'facultad':data[1],
                       'programa':data[2],
                       'materia':data[3],
                       'salon':data[4],
                       'id_usuario':data[5],
                       'estado_tutoria':data[6],
                       'cupos':data[7],
                       'tema':data[8],
                       'fecha':data[9],
                       'hora_inicial':data[10],
                       'hora_final':data[11],
                       'nombres':data[12],
                       'apellidos':data[13]
                    

                }
                payload.append(content)
                content = {}
            json_data = jsonable_encoder(payload)
            print(json_data)
            if result:
                return {"resultado": json_data}
            else:
                raise HTTPException(
                    status_code=404, detail="tutorias no encontradas")
     
     except Exception as e: 
            print(e)
            raise HTTPException(status_code=400, detail=e)
    def cancelarTutoria(id_user,id_tutoria):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            sql="delete  from lista_estudiantes where id_tutoria=%s and id_usuario=%s"
            cursor.execute(sql,(id_tutoria,id_user))
            
            conn.commit()
            conn.close()
        except mysql.connector.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()
    def recuperarCupos(id_tutoria):
         try:
            conn = get_db_connection()
            cursor = conn.cursor()
            sql="update horario_tutorias set cupos=cupos+1  where id_tutoria=%s"
            cursor.execute(sql,(id_tutoria,))
            
            conn.commit()
            conn.close()
         except mysql.connector.Error as err:
            print(err)
            conn.rollback()
         finally:
            conn.close()
    def obtenerTutoriaFinalizada(user_id:int):
     try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
            SELECT ht.id_tutoria,f.facultad,p.programa,m.materia ,s.salon,le.id_usuario,txe.estado,ht.cupos,ht.tema,ht.fecha,ht.hora_inicial,ht.hora_final,u.nombres,u.apellidos,le.comentario  FROM `horario_tutorias` ht 
            join lista_estudiantes le on le.id_tutoria=ht.id_tutoria
            join salones s on ht.id_salon=s.id_salon
            join tipoxestado txe on ht.id_estado_tutoria=txe.id_tipoxestado 
            join fpxmateria fpxm on fpxm.id_fpxm=ht.id_fpxm
            join facultadxprograma fxp on fxp.id_fxp=fpxm.id_fxp
            join facultades f on f.id_facultad=fxp.id_facultad
            join programas p on p.id_programa=fxp.id_programa
            join materias m on m.id_materia=fpxm.id_materia
            join usuarios u on u.id_usuario=ht.id_usuario
            where txe.id_tipoxestado=2 and le.id_usuario=%s
            """,(user_id,))
            result = cursor.fetchall()
            print(result)
            payload = []
            content = {}
            for data in result:
                content = {
                       'id':data[0],
                       'facultad':data[1],
                       'programa':data[2],
                       'materia':data[3],
                       'salon':data[4],
                       'id_usuario':data[5],
                       'estado_tutoria':data[6],
                       'cupos':data[7],
                       'tema':data[8],
                       'fecha':data[9],
                       'hora_inicial':data[10],
                       'hora_final':data[11],
                       'nombres':data[12],
                       'apellidos':data[13],
                       'observacion':data[14]
                    

                }
                payload.append(content)
                content = {}
            json_data = jsonable_encoder(payload)
            print(json_data)
            if result:
                return {"resultado": json_data}
            else:
               return {"error":"no hay tutorias finalizadas"}
     
     except Exception as e: 
            print(e)
            raise HTTPException(status_code=400, detail=e)
    def obtenerTutoriaFinalizadaDocente(user_id:int):
     try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
             SELECT ht.id_tutoria,f.facultad,p.programa,m.materia ,s.salon,ht.id_usuario,txe.estado,ht.cupos,ht.tema,ht.fecha,ht.hora_inicial,ht.hora_final,u.nombres,u.apellidos  FROM `horario_tutorias` ht 
            join salones s on ht.id_salon=s.id_salon
            join tipoxestado txe on ht.id_estado_tutoria=txe.id_tipoxestado 
            join fpxmateria fpxm on fpxm.id_fpxm=ht.id_fpxm
            join facultadxprograma fxp on fxp.id_fxp=fpxm.id_fxp
            join facultades f on f.id_facultad=fxp.id_facultad
            join programas p on p.id_programa=fxp.id_programa
            join materias m on m.id_materia=fpxm.id_materia
            join usuarios u on u.id_usuario=ht.id_usuario
            where txe.id_tipoxestado=2 and ht.id_usuario=%s
            """,(user_id,))
            print(user_id)
            result = cursor.fetchall()
            print(result)
            payload = []
            content = {}
            for data in result:
                print(content)
                content = {
                       'id':data[0],
                       'facultad':data[1],
                       'programa':data[2],
                       'materia':data[3],
                       'salon':data[4],
                       'id_usuario':data[5],
                       'estado_tutoria':data[6],
                       'cupos':data[7],
                       'tema':data[8],
                       'fecha':data[9],
                       'hora_inicial':data[10],
                       'hora_final':data[11],
                       'nombres':data[12],
                       'apellidos':data[13]
                    

                }
                payload.append(content)
                content = {}
            json_data = jsonable_encoder(payload)
            print(json_data)
            if result:
                return {"resultado": json_data}
            else:
               return {"error":"no hay tutorias finalizadas"}
     
     except Exception as e: 
            print(e)
            raise HTTPException(status_code=400, detail=e)
    



    def obtenerTutoriaFinalizadass():
     try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
             SELECT ht.id_tutoria,f.facultad,p.programa,m.materia ,s.salon,ht.id_usuario,txe.estado,ht.cupos,ht.tema,ht.fecha,ht.hora_inicial,ht.hora_final,u.nombres,u.apellidos  FROM `horario_tutorias` ht 
            join salones s on ht.id_salon=s.id_salon
            join tipoxestado txe on ht.id_estado_tutoria=txe.id_tipoxestado 
            join fpxmateria fpxm on fpxm.id_fpxm=ht.id_fpxm
            join facultadxprograma fxp on fxp.id_fxp=fpxm.id_fxp
            join facultades f on f.id_facultad=fxp.id_facultad
            join programas p on p.id_programa=fxp.id_programa
            join materias m on m.id_materia=fpxm.id_materia
            join usuarios u on u.id_usuario=ht.id_usuario
            where txe.id_tipoxestado=2 
            """)
            
            result = cursor.fetchall()
            print(result)
            payload = []
            content = {}
            for data in result:
                print(content)
                content = {
                       'id':data[0],
                       'facultad':data[1],
                       'programa':data[2],
                       'materia':data[3],
                       'salon':data[4],
                       'id_usuario':data[5],
                       'estado_tutoria':data[6],
                       'cupos':data[7],
                       'tema':data[8],
                       'fecha':data[9],
                       'hora_inicial':data[10],
                       'hora_final':data[11],
                       'nombres':data[12],
                       'apellidos':data[13]
                    

                }
                payload.append(content)
                content = {}
            json_data = jsonable_encoder(payload)
            print(json_data)
            if result:
                return {"resultado": json_data}
            else:
               return {"error":"no hay tutorias finalizadas"}
     
     except Exception as e: 
            print(e)
            raise HTTPException(status_code=400, detail=e)
    def obtenerDatosUsuario(id_user:int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            sql="""SELECT  u.nombres,u.apellidos,ht.tema from usuarios u
            join horario_tutorias ht on ht.id_usuario=u.id_usuario
            WHERE u.id_usuario=%s;"""
            cursor.execute(sql, (id_user,))
            result = cursor.fetchone()
            content = {} 
            
            content={
                    'nombres':result[0],
                    'apellidos':result[1],
                    'tema':result[2]
                    # 'id_estado':result[10],
                    # 'id_rol':result[11]  
            }
            
            json_data = jsonable_encoder(content)  
            if result:
               return  json_data
            else:
                raise HTTPException(status_code=404, detail="User not found")  
                
        except mysql.connector.Error as err:
            conn.rollback()
        finally:
            conn.close()

    def obtenerListado(id_tutoria):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
               SELECT ht.id_tutoria,ht.id_usuario,concat(u.nombres," ",u.apellidos) as nombre_estudiante, le.id_usuario,txe.estado,m.materia,u.numero_documento,p.programa,le.asistencia,le.comentario,u.correo  FROM `horario_tutorias` ht 
            join lista_estudiantes le on le.id_tutoria=ht.id_tutoria
            join salones s on ht.id_salon=s.id_salon
            join tipoxestado txe on ht.id_estado_tutoria=txe.id_tipoxestado 
            join fpxmateria fpxm on fpxm.id_fpxm=ht.id_fpxm
            join facultadxprograma fxp on fxp.id_fxp=fpxm.id_fxp
            join facultades f on f.id_facultad=fxp.id_facultad
            join programas p on p.id_programa=fxp.id_programa
            join materias m on m.id_materia=fpxm.id_materia
            join usuarios u on u.id_usuario=le.id_usuario
            where ht.id_tutoria=%s
            and txe.id_tipoxestado=8
""", (id_tutoria,))
            data = cursor.fetchall()
            print(data)
            payload = []
            content = {}
            for i in data:
        

                content = {
                     'id_tutoria':i[0],
                       'id_docente':i[1],
                       'nombre_estudiante':i[2],
                       'id_estudiante':i[3],
                       'estado_tutoria':i[4],
                       'materia':i[5],
                       'numero_documento':i[6],
                       'programa':i[7],
                       'asistencia':i[8],
                       'comentario':i[9],
                       'correo':i[10]
                }
                payload.append(content)
                content={}
            if payload:

             return payload
            return None
        except mysql.connector.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()

    def enviarCorreo(data,listado):
            for i in listado:
             email_data = {
                "subject": "Tutoria cancelada",
                "message": f"Estimado {i['nombre_estudiante']},\n\n la tutoria del docente {data['nombres']} con el tema {data['tema']} ha sido cancelada  Equipo de Administracion",
                "to_email": i['correo']

                }
             response=requests.post('http://127.0.0.1:8300/send-email',json=email_data)
            #  response=requests.post('https://fastapi-production-adfd.up.railway.app/send-email',json=email_data)
            
            