from flask import Blueprint, jsonify, request
from app import db
from app.models import Currency
from app.schemas import CurrencySchema
from marshmallow import ValidationError

bp = Blueprint('currency', __name__)
currency_schema = CurrencySchema()
currencies_schema = CurrencySchema(many=True)

@bp.route('/currency', methods=['GET'])
def get_currencies():
    currencies = Currency.query.all()
    return jsonify(currencies_schema.dump(currencies)), 200

@bp.route('/currency/<int:currency_id>', methods=['GET'])
def get_currency(currency_id):
    currency = Currency.query.get_or_404(currency_id, description='Currency not found')
    return jsonify(currency_schema.dump(currency)), 200

@bp.route('/currency', methods=['POST'])
def create_currency():
    try:
        data = currency_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400
    
    currency = Currency(**data)
    db.session.add(currency)
    db.session.commit()
    
    return jsonify(currency_schema.dump(currency)), 201

@bp.route('/currency/<int:currency_id>', methods=['DELETE'])
def delete_currency(currency_id):
    currency = Currency.query.get_or_404(currency_id, description='Currency not found')
    db.session.delete(currency)
    db.session.commit()
    
    return jsonify({'message': 'Currency deleted'}), 200