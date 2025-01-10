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
spotifyClient = spotipy.Spotify(token)

user_name = spotifyClient.current_user()

print(spotifyClient.devices()['devices'] )
device = [x for x in spotifyClient.devices()['devices'] if x['name'] == "Benjamin’s MacBook Pro"][0] #gets the ID for specified device
deviceID = device["id"]
rgb_playlist = get_playlists(spotifyClient, deviceID) # a dictionary of the playlists called "red", "green", "blue" that the user has

print(f"WELCOME TO THE PROJECT, {user_name['display_name']}\nCurrent Device: {device['name']}"  )

command_to_playlist = {
    "0x58": "spotify:playlist:09dqjgCuarBiOKInqOKIdF",
    "0x59": "spotify:playlist:1t6z5svHyNX5UXQjjNhZbL",
    "0x45": "spotify:playlist:5NjzcO3AA4l7Gj1q6J7BB9"
}
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback_default_key')
socketio = SocketIO(app)
port = int(os.getenv('PORT', "3333"))

@app.route('/')
def index():
    return "APT Spotify WebSocket server is running!"

@app.route('/api/play_music', methods=['POST'])
def handle_post_request():
    global spotifyClient
    # Parse the JSON data from the request
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
    
    # Process the data (for example, log it or store it)
    print(f"Received message: {data}")
    if (data.get("action") == "play_music"):
        token = oauth_object.get_cached_token()
        if (oauth_object.is_token_expired(token)):
          print("refreshing token:")
          token_info = oauth_object.refresh_access_token(token_info['refresh_token'])
          spotifyClient = spotipy.Spotify(auth=token_info['access_token'])
        else:
           print("using cached token:")
        print(command_to_playlist.get(data.get("command")))
        spotifyClient.start_playback(deviceID, context_uri=command_to_playlist.get(data.get("command")))
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