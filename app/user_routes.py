from app import app
from flask import jsonify, request
from app.data import users, get_next_user_id

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user), 200

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id not in users:
        return jsonify({'error': 'User not found'}), 404
    deleted_user = users.pop(user_id)
    return jsonify({'message': 'User deleted', 'user': deleted_user}), 200

@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400
    
    user_id = get_next_user_id()
    user = {
        'id': user_id,
        'name': data['name']
    }
    users[user_id] = user
    
    return jsonify(user), 201

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(list(users.values())), 200
