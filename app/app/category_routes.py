from app import app
from flask import jsonify, request
from app.data import categories, get_next_category_id

@app.route('/category', methods=['GET'])
def get_categories():
    return jsonify(list(categories.values())), 200

@app.route('/category', methods=['POST'])
def create_category():
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400
    
    category_id = get_next_category_id()
    category = {
        'id': category_id,
        'name': data['name']
    }
    categories[category_id] = category
    
    return jsonify(category), 201

@app.route('/category/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    if category_id not in categories:
        return jsonify({'error': 'Category not found'}), 404
    deleted_category = categories.pop(category_id)
    return jsonify({'message': 'Category deleted', 'category': deleted_category}), 200
