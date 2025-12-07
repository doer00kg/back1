from app import app
from flask import jsonify, request
from datetime import datetime
from app.data import records, users, categories, get_next_record_id

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

@app.route('/record', methods=['POST'])
def create_record():
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Request body is required'}), 400
    
    required_fields = ['user_id', 'category_id', 'amount']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    user_id = data['user_id']
    category_id = data['category_id']
    
    if user_id not in users:
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
    
    return jsonify(record), 201

@app.route('/record', methods=['GET'])
def get_records():
    user_id = request.args.get('user_id', type=int)
    category_id = request.args.get('category_id', type=int)
    
    if user_id is None and category_id is None:
        return jsonify({'error': 'user_id or category_id parameter is required'}), 400
    
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
    
    return jsonify(filtered_records), 200
