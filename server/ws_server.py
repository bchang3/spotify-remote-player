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

# Event handler for when a client connects
@socketio.on('connect')
def handle_connect():
    print("A client has connected.")

# Event handler for when a client disconnects
@socketio.on('disconnect')
def handle_disconnect():
    print("A client has disconnected.")

@socketio.on('message')
def handle_message(msg):
    print(f"Received message: {msg}")
    socketio.send(f"Echo: {msg}")

if __name__ == '__main__':
    # Bind to a specific port, e.g., 5001
    print(f"Starting WebSocket server at port {port}")
    socketio.run(app, host='0.0.0.0', port=port)
