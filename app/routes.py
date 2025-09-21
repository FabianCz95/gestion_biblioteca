from flask import Blueprint,jsonify,request
from . import library_manager
from .models import Autor

routes_bp = Blueprint('routes_bp', __name__)

@routes_bp.route("/", methods=['GET'])
def root():
    return "Hello from Blueprint in Flask"


@routes_bp.route('/autores', methods=['GET'])
def get_autores():
    autores: list[Autor] = library_manager.obtener_autores()
    autores_dict = [autor.to_dict() for autor in autores]
    if autores:
        return jsonify(autores_dict), 200
    else:
        return jsonify({"message": "No se encontraron autores."}), 404

@routes_bp.route('/autores', methods=['POST'])
def post_autor():
    data = request.get_json()
    if not data or not data.get('primer_nombre') or not data.get('primer_apellido'):
        return jsonify({'message': "Faltan datos obligatorios (primer_nombre, primer_apellido)."}), 400 #400 Bad Request
    
    autor: Autor =  Autor(None, data.get("primer_nombre"), data.get("segundo_nombre"), data.get("primer_apellido"), data.get("segundo_apellido)"))
    nuevo_autor = library_manager.agregar_autor(autor)

    if nuevo_autor:
        return jsonify({"message": "Autor agregado exitosamente", "Autor": nuevo_autor.to_dict()}), 201 # 201 Created
    else:
        return jsonify({"message": "Error al agregar el autor."}), 500 # 500 Internal Server Error

@routes_bp.route('/autores/<int:id_autor>', methods=['GET'])
def get_autor(id_autor):
    autor: Autor = library_manager.buscar_autor(id_autor)
    if autor:
        return jsonify({"Autor": autor.to_dict()}), 200
    else:
        return jsonify({"message": f"No se encontró ningún autor id: {id_autor}"}), 404
    
@routes_bp.route('/autores/<int:id_autor>', methods=['PUT'])
def update_autor(id_autor):
    data = request.get_json()
    if not data:
        return jsonify({"message": "El cuerpo de la solicitud no puede estar vacío."}), 400
    
    #autor = Autor(id_autor, data.get("primer_nombre"), data.get("segundo_nombre"), data.get("primer_apellido"), data.get("segundo_apellido"))
    autor_actualizado = library_manager.actualizar_autor(id_autor, data)

    if autor_actualizado:
        return jsonify({"message": "Datos del autor actualizados correctamente", "Autor": autor_actualizado.to_dict()}), 200 # 200 OK
    else:
        return jsonify({"message": "Faltan datos obligatorios (primer_nombre, primer_apellido)."}), 400

