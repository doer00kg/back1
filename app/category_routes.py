from app import app
from flask import jsonify, request
from app.data import categories, get_next_category_id
from flask import Blueprint, jsonify, request
from app import db
from app.models import Category
from app.schemas import CategorySchema
from marshmallow import ValidationError

@app.route('/category', methods=['GET'])
bp = Blueprint('category', __name__)
category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)

@bp.route('/category', methods=['GET'])
def get_categories():
    return jsonify(list(categories.values())), 200
    categories = Category.query.all()
    return jsonify(categories_schema.dump(categories)), 200

@bp.route('/category/<int:category_id>', methods=['GET'])
def get_category(category_id):
    category = Category.query.get_or_404(category_id, description='Category not found')
    return jsonify(category_schema.dump(category)), 200

@app.route('/category', methods=['POST'])
@bp.route('/category', methods=['POST'])
def create_category():
    data = request.get_json()
    try:
        data = category_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400

    if not data or 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400
    category = Category(**data)
    db.session.add(category)
    db.session.commit()

    category_id = get_next_category_id()
    category = {
        'id': category_id,
        'name': data['name']
    }
    categories[category_id] = category
    
    return jsonify(category), 201
    return jsonify(category_schema.dump(category)), 201

@app.route('/category/<int:category_id>', methods=['DELETE'])
@bp.route('/category/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    if category_id not in categories:
        return jsonify({'error': 'Category not found'}), 404
    deleted_category = categories.pop(category_id)
    return jsonify({'message': 'Category deleted', 'category': deleted_category}), 200
    category = Category.query.get_or_404(category_id, description='Category not found')
    db.session.delete(category)
    db.session.commit()
    
    return jsonify({'message': 'Category deleted'}), 200