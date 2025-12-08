from app import app
from flask import jsonify, request
from app.data import users, get_next_user_id
from flask import Blueprint, jsonify, request
from app import db
from app.models import User
from app.schemas import UserSchema
from marshmallow import ValidationError

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user), 200
bp = Blueprint('user', __name__)
user_schema = UserSchema()
users_schema = UserSchema(many=True)

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id not in users:
        return jsonify({'error': 'User not found'}), 404
    deleted_user = users.pop(user_id)
    return jsonify({'message': 'User deleted', 'user': deleted_user}), 200
@bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify(users_schema.dump(users)), 200

@bp.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id, description='User not found')
    return jsonify(user_schema.dump(user)), 200

@app.route('/user', methods=['POST'])
@bp.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    try:
        data = user_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400

    if not data or 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400
    user = User(**data)
    db.session.add(user)
    db.session.commit()

    user_id = get_next_user_id()
    user = {
        'id': user_id,
        'name': data['name']
    }
    users[user_id] = user
    
    return jsonify(user), 201
    return jsonify(user_schema.dump(user)), 201

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(list(users.values())), 200
@bp.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id, description='User not found')
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({'message': 'User deleted'}), 200