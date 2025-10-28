from app import app
from flask import jsonify
from datetime import datetime

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({
        "status": "OK",
        "time": datetime.now().isoformat()
    }), 200
