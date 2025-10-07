import psycopg2 
import os
from dotenv import load_dotenv
from psycopg2.errors import OperationalError
from .models import Autor


def crear_tablas():
    conn = None
    try:
        conn = psycopg2.connect(
            dbname="biblioteca",
            user="postgres",
            password="admin",
            host="localhost"
        )
        cur = conn.cursor()

        create_autores_table = """
        CREATE TABLE IF NOT EXISTS CatAutores (
            id_autor SERIAL PRIMARY KEY,
            primer_nombre VARCHAR(255) NOT NULL,
            segundo_nombre VARCHAR(255),
            primer_apellido VARCHAR(255) NOT NULL,
            segundo_apellido VARCHAR(255)
        );


        CREATE TABLE IF NOT EXISTS CatUsuarios (
            id_usuario SERIAL PRIMARY KEY,
            primer_nombre VARCHAR(255) NOT NULL,
            segundo_nombre VARCHAR(255),
            primer_apellido VARCHAR(255) NOT NULL,
            segundo_apellido VARCHAR(255)
        );

        CREATE TABLE IF NOT EXISTS CatLibros (
            id_libro SERIAL PRIMARY KEY,
            nom_titulo VARCHAR(255) NOT NULL,
            anio_publicacion DATE NOT NULL,
            id_autor INT NOT NULL,
            FOREIGN KEY (id_autor) REFERENCES CatAutores (id_autor)
        );

        CREATE TABLE IF NOT EXISTS TraLibrosUsuarios (
            id_libro INT,
            id_usuario INT,
            PRIMARY KEY (id_libro,id_usuario),
            FOREIGN KEY (id_libro) REFERENCES CatLibros (id_libro),
            FOREIGN KEY (id_usuario) REFERENCES CatUsuarios (id_usuario)
        );

        """

        cur.execute(create_autores_table)
        conn.commit()
        print("Tablas creada o ya existentes")
        
    except OperationalError as e:
        print(f"Error al conectar o crear tablas: {e}")
    finally:
        if conn is not None:
            cur.close()
            conn.close()

def insertar_autor(autor: Autor):
    """
    Inserta un nuevo autor en la base de datos y retorna su ID.
    """
    conn = None
    try:
        conn = psycopg2.connect(
            dbname="biblioteca",
            user="postgres",
            password="admin",
            host="localhost"
        )
        cur = conn.cursor()
        
        insert_autor = """
        INSERT INTO CatAutores(primer_nombre, segundo_nombre, primer_apellido, segundo_apellido)
        VALUES (%s, %s, %s, %s)
        RETURNING id_autor;
        """

        cur.execute(insert_autor, (autor.primer_nombre, autor.segundo_nombre, autor.primer_apellido, autor.segundo_apellido))
        result = cur.fetchone()

        if result is not None:
            autor.id_autor = result[0]
        else:
            print("No se pudo obtener el ID del autor insertado.")
        conn.commit()

    except OperationalError as e:
        print(f"Error en la capa de datos al insertar autor: {e}")

    finally:
        if conn is not None:
            cur.close()
            conn.close()
    return autor

def obtener_autores():
    conn = None
    autores_dict_list: list[Autor] = []
    try:
        conn = psycopg2.connect(
            dbname = os.getenv("DB_NAME"),
            user = os.getenv("DB_USER"),
            password = os.getenv("DB_PASSWORD"),
            host = os.getenv("DB_HOST")
        )
        cur = conn.cursor()

        query = """
        SELECT id_autor, primer_nombre, segundo_nombre, primer_apellido, segundo_apellido FROM CatAutores
        """

        cur.execute(query)
        autores_tuplas = cur.fetchall() #Obtiene todos los resultados

        if autores_tuplas is not None:
            for autor_tuple in autores_tuplas:
                autores_dict_list.append(Autor(autor_tuple[0], autor_tuple[1], autor_tuple[2], autor_tuple[3], autor_tuple[4]))

    except (Exception, OperationalError) as e:
        print(f"Error al obtener autores: {e}")
        return []
    finally:
        if conn is not None:
            cur.close()
            conn.close()
    return autores_dict_list
    
def buscar_autor(id_autor):
    conn = None
    new_autor: Autor = Autor()
    try:
        conn = psycopg2.connect(
            dbname = os.getenv("DB_NAME"),
            user = os.getenv("DB_USER"),
            password = os.getenv("DB_PASSWORD"),
            host = os.getenv("DB_HOST")
        )
        cur = conn.cursor()

        query = """
        SELECT id_autor, primer_nombre, segundo_nombre, primer_apellido, segundo_apellido FROM catautores WHERE id_autor=%s;
        """
        cur.execute(query, (id_autor,))
        autor_tuple = cur.fetchone()
        if autor_tuple is not None:
            new_autor: Autor = Autor(autor_tuple[0], autor_tuple[1], autor_tuple[2], autor_tuple[3], autor_tuple[4])
    except (Exception, OperationalError) as e:
        print(f"Error en la capa de datos al buscar el autor: {e}")
    finally:
        if conn is not None:
            cur.close()
            conn.close()
    return new_autor

def actualizar_autor(autor: Autor):
    conn = None
    nuevo_autor: Autor = Autor()
    try:
        conn = psycopg2.connect(
            dbname = os.getenv("DB_NAME"),
            user = os.getenv("DB_USER"),
            password = os.getenv("DB_PASSWORD"),
            host = os.getenv("DB_HOST")
        )
        cur = conn.cursor()

        query = """
        UPDATE catautores
        SET primer_nombre = %s,
            segundo_nombre = %s,
            primer_apellido = %s,
            segundo_apellido = %s
        WHERE id_autor = %s
        RETURNING id_autor, primer_nombre, segundo_nombre, primer_apellido, segundo_apellido;
        """

        cur.execute(query,(autor.primer_nombre, autor.segundo_nombre, autor.primer_apellido, autor.segundo_apellido, autor.id_autor))
        autor_tuple = cur.fetchone()
        if autor_tuple is not None:
            nuevo_autor: Autor = Autor(autor_tuple[0], autor_tuple[1], autor_tuple[2], autor_tuple[3], autor_tuple[4])
        conn.commit()
    except (Exception, OperationalError) as e:
        print(f"Error en la capa de datos al actualizar el autor: {e}")
    finally:
        if conn is not None:
            cur.close()
            conn.close()
    return nuevo_autor