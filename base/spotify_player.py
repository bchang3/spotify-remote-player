import json
import spotipy
import webbrowser
import time
import serial
import serial.tools.list_ports
from spotify_player_utils import clearQueue, get_playlists
import random
import signal
import sys


try:
    ser = serial.Serial('/dev/cu.usbmodem101',9600, timeout = 1)
except:
    print("ARDUINO IS NOT CONNECTED!")
username = "jwpzy3f95b860qvipvqhxmira"
clientID = "57bc553732ef4299bea6391c4ae59019"
clientSecret = "a1d6b74fb4f84bb4b5fa72a0b38bcdcb"
redirect_uri = "http://google.com/callback/"
scope = "user-read-playback-state playlist-modify-public user-modify-playback-state streaming app-remote-control playlist-read-collaborative playlist-read-private"
oauth_object = spotipy.SpotifyOAuth(clientID, clientSecret, redirect_uri, scope=scope)
token = oauth_object.get_access_token()['access_token']
spotifyObject = spotipy.Spotify(token)

user_name = spotifyObject.current_user()

play_dict = {1: "red", 2: "green", 3: "blue"}

device = [x for x in spotifyObject.devices()['devices'] if x['name'] == "Benjamin’s MacBook Pro"][0] #gets the ID for specified device
deviceID = device["id"]
print(f"WELCOME TO THE PROJECT, {user_name['display_name']}\nCurrent Device: {device['name']}"  )

rgb_playlist = get_playlists(spotifyObject, deviceID) # a dictionary of the playlists called "red", "green", "blue" that the user has
for color in rgb_playlist.keys():
    random.shuffle(rgb_playlist[color])

print(deviceID)

current_playlist = 0
last = ""
ser.reset_input_buffer()
ser.reset_output_buffer()

queueing = True
try:
    while True:
        try:
            data = ser.readline()
        except:
            print("Error reading line!")
            data = True
        if data:
            print("SIGNAL RECEIVED")
            current_playlist += 1
            queueing = True
            if (current_playlist > 3):
                current_playlist = 0
                rgb_playlist = get_playlists(spotifyObject, deviceID)
            if current_playlist != 0:
                clearQueue(spotifyObject, deviceID)
                playlist = rgb_playlist[play_dict[current_playlist]]
                for song in playlist[0:2]:
                    spotifyObject.add_to_queue(song, deviceID)
                    last = song
                playlist = playlist[2:]
                spotifyObject.next_track(deviceID)
            else:
                clearQueue(spotifyObject, deviceID)
                spotifyObject.pause_playback()
            ser.reset_input_buffer()
            time.sleep(4)

        else:
            cp = spotifyObject.currently_playing()
            if cp != None and cp["item"] != None and cp["item"]["uri"] == last and current_playlist != 0:
                if queueing:
                    for song in playlist[0:2]:
                        spotifyObject.add_to_queue(song)
                        last = song
                    if len(playlist) > 2:
                        playlist = playlist[2:]
                        queueing = False
            print("...")
except KeyboardInterrupt:
    print("quitting")
    spotifyObject.pause_playback()
    ser.reset_input_buffer()
    ser.reset_output_buffer()
    ser.close()
    sys.exit(0)
