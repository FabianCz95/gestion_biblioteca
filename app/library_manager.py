from . import database as database
from .models import Autor

def agregar_autor(autor: Autor):
    try:
        autor = database.insertar_autor(autor)
        return autor
        
    except Exception as e:
        print(f"Ocurrió un error en la capa de negocio al agregar autor: {e}")
        return None
    
def obtener_autores():
    return database.obtener_autores()

def buscar_autor(id_autor):
    autor: Autor = database.buscar_autor(id_autor)

    if not autor:
        return {}
    
    return autor

def actualizar_autor(id_autor: int, data: dict):
    autor_existente: Autor = buscar_autor(id_autor)

    if not autor_existente:
        return None
    
    if "primer_nombre" in data:
        autor_existente.primer_nombre = data["primer_nombre"]
    if "segundo_nombre" in data:
        autor_existente.segundo_nombre = data["segundo_nombre"]
    if "primer_apellido" in data:
        autor_existente.primer_apellido = data["primer_apellido"]
    if "segundo_apellido" in data:
        autor_existente.segundo_apellido = data["segundo_apellido"]

    return database.actualizar_autor(autor_existente)
