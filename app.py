from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Хранилище для текста
storage = {
    "data": "",
    "timestamp": "",
    "last_updated_by": ""
}

@app.route('/api/text', methods=['POST'])
def set_text():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        storage["data"] = data.get('text', '')
        storage["timestamp"] = datetime.now().isoformat()
        storage["last_updated_by"] = data.get('player', 'unknown')
        
        print(f"📥 Получен текст: {storage['data']}")
        return jsonify({
            "status": "success", 
            "message": "Text stored successfully"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/text', methods=['GET'])
def get_text():
    try:
        return jsonify({
            "text": storage["data"],
            "timestamp": storage["timestamp"],
            "last_updated_by": storage["last_updated_by"]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "Roblox Text Server"})

@app.route('/')
def home():
    return "Roblox Text Server is running!"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
