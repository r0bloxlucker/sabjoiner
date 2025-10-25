from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Хранилище для текста
storage = {
    "data": "Привет от сервера!",
    "timestamp": datetime.now().isoformat(),
    "last_updated_by": "Server"
}

@app.route('/api/text', methods=['POST'])
def set_text():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        text = data.get('text', '').strip()
        if not text:
            return jsonify({"error": "Text cannot be empty"}), 400
            
        storage["data"] = text
        storage["timestamp"] = datetime.now().isoformat()
        storage["last_updated_by"] = data.get('player', 'unknown')
        
        print(f"📥 Получен текст: '{storage['data']}' от {storage['last_updated_by']}")
        
        return jsonify({
            "status": "success", 
            "message": "Text stored successfully",
            "text": storage["data"]
        })
        
    except Exception as e:
        print(f"❌ Ошибка сервера: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/text', methods=['GET'])
def get_text():
    try:
        return jsonify({
            "text": storage["data"],
            "timestamp": storage["timestamp"],
            "last_updated_by": storage["last_updated_by"],
            "status": "success"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/test', methods=['GET'])
def test():
    """Простой тестовый endpoint"""
    return jsonify({
        "message": "Сервер работает!",
        "status": "success",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/')
def home():
    return """
    <h1>Roblox Text Server</h1>
    <p>Сервер работает!</p>
    <p>Endpoints:</p>
    <ul>
        <li>GET /api/text - получить текст</li>
        <li>POST /api/text - отправить текст</li>
        <li>GET /api/test - тест сервера</li>
    </ul>
    """

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
