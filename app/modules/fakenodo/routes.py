from flask import Blueprint, jsonify, request
from fakenodo.repositories import create_deposit, get_all_deposits, get_deposit_by_id, delete_deposit

api = Blueprint('fakenodo', __name__)

@api.route('/deposits', methods=['POST'])
def create_deposit_route():
    data = request.json
    deposit = create_deposit(data)
    return jsonify(deposit), 201

@api.route('/deposits', methods=['GET'])
def get_all_deposits_route():
    deposits = get_all_deposits()
    return jsonify(deposits), 200

@api.route('/deposits/<deposit_id>', methods=['GET'])
def get_deposit_by_id_route(deposit_id):
    deposit = get_deposit_by_id(deposit_id)
    if deposit:
        return jsonify(deposit), 200
    return jsonify({"error": "Deposit not found"}), 404

@api.route('/deposits/<deposit_id>', methods=['DELETE'])
def delete_deposit_route(deposit_id):
    if delete_deposit(deposit_id):
        return jsonify({"message": "Deposit deleted"}), 200
    return jsonify({"error": "Deposit not found"}), 404
