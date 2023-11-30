from pydantic import BaseModel
from typing import List
class ListadoEstudiante(BaseModel):
    id:int=0
    
    id_usuario:int
    asistencia:bool
    id_tutoria:int
    observacion:str


class DatosRecibir(BaseModel):
    estudiantes:List[ListadoEstudiante]