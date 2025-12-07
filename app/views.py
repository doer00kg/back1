from app import app
from flask import jsonify
from datetime import datetime

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'message': 'Backend Labs API',
        'status': 'running',
        'endpoints': {
            'healthcheck': '/healthcheck'
        }
    }), 200

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({
        "status": "OK",
        "time": datetime.now().isoformat()
    }), 200
