from flask import Flask
from flask_socketio import SocketIO
from dotenv import load_dotenv
import os


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback_default_key')
socketio = SocketIO(app)
port = int(os.getenv('PORT', "3333"))

@app.route('/')
def index():
    return "APT Spotify WebSocket server is running!"

@app.route('/api/play_music', methods=['POST'])
def handle_post_request():
    # Parse the JSON data from the request
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
    
    # Process the data (for example, log it or store it)
    print(f"Received data: {data}")
    
    # Create a response
    response = {
        "message": "Data received successfully",
        "received_data": data
    }
    
    return jsonify(response), 200

if __name__ == '__main__':
    # Run the Flask app on port 5000
    app.run(host='0.0.0.0', port=port)