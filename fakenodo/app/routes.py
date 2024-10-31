# app/routes.py
import os
from flask import Blueprint, jsonify, render_template, request
from app.modules.dataset.models import DataSet
from app.modules.featuremodel.models import FeatureModel
from fakenodo.app.models import Deposition
from fakenodo.app.services import FakenodoService

api_bp = Blueprint("api_bp", __name__)
service = FakenodoService()

@api_bp.route('/fakenodo', methods=['GET'])
def index():
    return render_template('fakenodo/index.html')

@api_bp.route('/api/fakenodo/test', methods=['GET'])
def fakenodo_test():
    return service.test_full_connection()

@api_bp.route('/api/fakenodo/depositions', methods=['GET'])
def get_all_depositions():
    try:
        depositions = service.get_all_depositions()
        return jsonify(depositions)
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@api_bp.route('/api/fakenodo/deposition/empty', methods=['POST'])
def create_empty_deposition():
    data = request.json
    try:
        deposition = Deposition(**data)  
        return jsonify(deposition.to_dict()), 201
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@api_bp.route('/api/fakenodo/deposition/<int:deposition_id>/files', methods=['POST'])
def upload_file(deposition_id):
    try:
        # Obtener los datos del formulario y los archivos
        file = request.files.get('file')
        file_name = request.form.get('name')

        # Verifica que el archivo y el nombre estén presentes
        if not file or not file_name:
            return jsonify({"success": False, "message": "Missing file or name."}), 400
        
      # Guardar el archivo en la carpeta actual
        save_path = os.path.join(os.getcwd(), file_name)  # Ruta donde se guardará el archivo
        file.save(save_path)  # Guardar el archivo
        # Devuelve una respuesta de éxito

        return jsonify({"success": True, "message": "File uploaded successfully.", "file_name": file_name}), 201
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@api_bp.route('/api/fakenodo/deposition/<int:deposition_id>', methods=['GET'])
def get_deposition(deposition_id):
    try:
        deposition = service.get_deposition(deposition_id)
        return jsonify(deposition)
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@api_bp.route('/api/fakenodo/deposition/<int:deposition_id>/publish', methods=['POST'])
def publish_deposition(deposition_id):
    try:
        published_deposition = service.publish_deposition(deposition_id)
        return jsonify(published_deposition)
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@api_bp.route('/api/fakenodo/deposition/<int:deposition_id>/doi', methods=['GET'])
def get_doi(deposition_id):
    try:
        doi = service.get_doi(deposition_id)
        return jsonify({"doi": doi})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
