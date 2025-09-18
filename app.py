from flask import Flask, request, jsonify
import base64
import os

app = Flask(__name__)

# Simulated license key database
LICENSE_KEYS = {
    "RAILONE": {"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2OGNjOGJjZDJmODYzNjE5ZTQ4ZGQ2YWEiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2OGNjOGJmOTQ5OWU1MDdhYmM5Y2M0M2IifQ.n09lGm2vr3gYyMD_Io8fCK8yqQWFctjrbKevRS2PhmM"},
    "railone": {"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2OGNjOGJjZDJmODYzNjE5ZTQ4ZGQ2YWEiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2OGNjOGJmOTQ5OWU1MDdhYmM5Y2M0M2IifQ.n09lGm2vr3gYyMD_Io8fCK8yqQWFctjrbKevRS2PhmM"}
}


ZIP_FILE_PATH = "rail-one.zip"  # Ensure this file exists in the same directory

# Expected Access-Token
ACCESS_TOKEN = "6b87036af1b3eb1eae8fef8211a7df7749875940d2868b8d7c169844f5cf124a"

@app.route('/api/v1/verify-license', methods=['POST'])
def verify_license():
    try:
        data = request.get_json()
        key = data.get('key')
        if not key:
            return jsonify({"status": False, "message": "No license key provided"}), 400
        if key in LICENSE_KEYS:
            return jsonify({"status": True, "data": {"token": LICENSE_KEYS[key]["token"]}})
        return jsonify({"status": False, "message": "Invalid license key"}), 401
    except Exception as e:
        return jsonify({"status": False, "message": str(e)}), 500

@app.route('/api/v1/get-active-app', methods=['POST'])
def get_active_app():
    try:
        # Check Access-Token
        access_token = request.headers.get('Access-Token')
        if access_token != ACCESS_TOKEN:
            return jsonify({"status": False, "message": "Invalid Access-Token"}), 401
        
        # License key is optional
        data = request.get_json()
        key = data.get('key')
        if key and key not in LICENSE_KEYS:
            return jsonify({"status": False, "message": "Invalid license key"}), 401
        
        if not os.path.exists(ZIP_FILE_PATH):
            return jsonify({"status": False, "message": "rail-one zip file not found"}), 500
        
        with open(ZIP_FILE_PATH, 'rb') as f:
            zip_content = base64.b64encode(f.read()).decode('utf-8')
        return jsonify({"status": True, "data": {"application": zip_content}})
    except Exception as e:
        return jsonify({"status": False, "message": str(e)}), 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)