from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from dotenv import load_dotenv
import os
import spotipy
from spotify_player_utils import clearQueue, get_playlists

load_dotenv()

#set up spotify API client

username = "jwpzy3f95b860qvipvqhxmira"
clientID = os.getenv('SPOTIFY_CLIENT_ID',)
clientSecret = os.getenv('SPOTIFY_CLIENT_SECRET',)
redirect_uri = "http://google.com/callback/"
scope = "user-read-playback-state playlist-modify-public user-modify-playback-state streaming app-remote-control playlist-read-collaborative playlist-read-private"
oauth_object = spotipy.SpotifyOAuth(clientID, clientSecret, redirect_uri, scope=scope)
auth_url = oauth_object.get_authorize_url()
print(f"Authorize URL: {auth_url}")
token = oauth_object.get_access_token()['access_token']
spotifyObject = spotipy.Spotify(token)

user_name = spotifyObject.current_user()

print(spotifyObject.devices()['devices'] )
device = [x for x in spotifyObject.devices()['devices'] if x['name'] == "Benjamin’s MacBook Pro"][0] #gets the ID for specified device
deviceID = device["id"]
rgb_playlist = get_playlists(spotifyObject, deviceID) # a dictionary of the playlists called "red", "green", "blue" that the user has

print(f"WELCOME TO THE PROJECT, {user_name['display_name']}\nCurrent Device: {device['name']}"  )


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
    print(f"Received message: {data}")
    if (data.get("action") == "play_music"):
        spotifyObject.start_playback(deviceID, context_uri="spotify:playlist:09dqjgCuarBiOKInqOKIdF")
        response = {
          "message": "Starting playlist!",
          "received_data": data
        }
        return jsonify(response), 200
    else:
      response = {
          "message": "Action not found!",
          "received_data": data
      }
      
      return jsonify(response), 400

if __name__ == '__main__':
    # Run the Flask app on port 5000
    app.run(host='0.0.0.0', port=port)