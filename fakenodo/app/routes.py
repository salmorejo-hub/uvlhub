# app/routes.py
from flask import Blueprint, jsonify, render_template, request
from app.modules.dataset.models import DataSet
from app.modules.featuremodel.models import FeatureModel
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

@api_bp.route('/api/fakenodo/deposition', methods=['POST'])
def create_deposition():
    data = request.json
    dataset = DataSet(**data)  # Asumiendo que DataSet se puede inicializar directamente con un diccionario
    try:
        deposition = service.create_new_deposition(dataset)
        return jsonify(deposition), 201
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@api_bp.route('/api/fakenodo/deposition/<int:deposition_id>/upload', methods=['POST'])
def upload_file(deposition_id):
    data = request.json
    dataset_id = data.get("dataset_id")
    feature_model_data = data.get("feature_model")  # Asumiendo que puedes crear un FeatureModel de esta manera
    feature_model = FeatureModel(**feature_model_data)
    
    try:

        dataset = DataSet.get_by_id(dataset_id)
        uploaded_file = service.upload_file(dataset, deposition_id, feature_model)
        return jsonify(uploaded_file), 201
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
