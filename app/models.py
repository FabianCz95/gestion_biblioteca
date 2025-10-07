from typing import Optional

class Autor:
    def __init__(self, id_autor: Optional[int] = None, primer_nombre: str = "", segundo_nombre: Optional[str] = None, primer_apellido: str = "", segundo_apellido: Optional[str] = None):
        self.id_autor = id_autor
        self.primer_nombre = primer_nombre
        self.segundo_nombre = segundo_nombre
        self.primer_apellido = primer_apellido
        self.segundo_apellido = segundo_apellido

    def to_dict(self):
        """Convierte el objeto Autor a un diccionario"""
        return {
            "id_autor": self.id_autor,
            "primer_nombre": self.primer_nombre,
            "segundo_nombre": self.segundo_nombre,
            "primer_apellido": self.primer_apellido,
            "segundo_apellido": self.segundo_apellido
        }
    