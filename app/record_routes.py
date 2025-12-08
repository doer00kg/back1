from app import app
from flask import jsonify, request
from datetime import datetime
from app.data import records, users, categories, get_next_record_id
from flask import Blueprint, jsonify, request
from app import db
from app.models import Record, User, Category
from app.schemas import RecordSchema
from marshmallow import ValidationError

@app.route('/record/<int:record_id>', methods=['GET'])
def get_record(record_id):
    record = records.get(record_id)
    if record is None:
        return jsonify({'error': 'Record not found'}), 404
    return jsonify(record), 200

@app.route('/record/<int:record_id>', methods=['DELETE'])
def delete_record(record_id):
    if record_id not in records:
        return jsonify({'error': 'Record not found'}), 404
    deleted_record = records.pop(record_id)
    return jsonify({'message': 'Record deleted', 'record': deleted_record}), 200
bp = Blueprint('record', __name__)
record_schema = RecordSchema()
records_schema = RecordSchema(many=True)

@app.route('/record', methods=['POST'])
def create_record():
    data = request.get_json()
@bp.route('/record', methods=['GET'])
def get_records():
    user_id = request.args.get('user_id', type=int)
    category_id = request.args.get('category_id', type=int)
    
    if user_id is None and category_id is None:
        return jsonify({'error': 'user_id or category_id parameter is required'}), 400

    if not data:
        return jsonify({'error': 'Request body is required'}), 400
    query = Record.query

    required_fields = ['user_id', 'category_id', 'amount']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    if user_id is not None:
        query = query.filter_by(user_id=user_id)
    if category_id is not None:
        query = query.filter_by(category_id=category_id)

    user_id = data['user_id']
    category_id = data['category_id']
    records = query.all()
    return jsonify(records_schema.dump(records)), 200

@bp.route('/record/<int:record_id>', methods=['GET'])
def get_record(record_id):
    record = Record.query.get_or_404(record_id, description='Record not found')
    return jsonify(record_schema.dump(record)), 200

@bp.route('/record', methods=['POST'])
def create_record():
    try:
        data = record_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400

    if user_id not in users:
    # Перевірка існування користувача
    user = User.query.get(data['user_id'])
    if not user:
        return jsonify({'error': 'User not found'}), 404
    if category_id not in categories:
        return jsonify({'error': 'Category not found'}), 404

    record_id = get_next_record_id()
    record = {
        'id': record_id,
        'user_id': user_id,
        'category_id': category_id,
        'amount': data['amount'],
        'created_at': datetime.now().isoformat()
    }
    records[record_id] = record
    # Перевірка існування категорії
    category = Category.query.get(data['category_id'])
    if not category:
        return jsonify({'error': 'Category not found'}), 404

    return jsonify(record), 201

@app.route('/record', methods=['GET'])
def get_records():
    user_id = request.args.get('user_id', type=int)
    category_id = request.args.get('category_id', type=int)
    # Якщо currency_id не вказано, використовуємо валюту користувача за замовчуванням
    if 'currency_id' not in data or data['currency_id'] is None:
        data['currency_id'] = user.default_currency_id

    if user_id is None and category_id is None:
        return jsonify({'error': 'user_id or category_id parameter is required'}), 400
    record = Record(**data)
    db.session.add(record)
    db.session.commit()

    filtered_records = []
    for record in records.values():
        match = False
        
        if user_id is not None and category_id is not None:
            if record['user_id'] == user_id and record['category_id'] == category_id:
                match = True
        elif user_id is not None:
            if record['user_id'] == user_id:
                match = True
        elif category_id is not None:
            if record['category_id'] == category_id:
                match = True
        
        if match:
            filtered_records.append(record)
    return jsonify(record_schema.dump(record)), 201

@bp.route('/record/<int:record_id>', methods=['DELETE'])
def delete_record(record_id):
    record = Record.query.get_or_404(record_id, description='Record not found')
    db.session.delete(record)
    db.session.commit()

    return jsonify(filtered_records), 200
    return jsonify({'message': 'Record deleted'}), 200