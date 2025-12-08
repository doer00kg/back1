from app import app
from flask import jsonify
from flask import Blueprint, jsonify
from datetime import datetime

@app.route('/', methods=['GET'])
bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET'])
def index():
    return jsonify({
        'message': 'Backend Labs API',
        'status': 'running',
        'endpoints': {
            'healthcheck': '/healthcheck'
        }
    }), 200

@app.route('/healthcheck', methods=['GET'])
@bp.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({
        'status': 'OK',
        'date': datetime.now().isoformat()
    }), 200