import time
linebreak = "~" * 100
def clearQueue(spotifyObject, deviceID):
    for i in range(len(spotifyObject.queue())):
        spotifyObject.next_track(deviceID)
        time.sleep(0.1)
    # spotifyObject.pause_playback(deviceID)
    print("Queue cleared!")
def get_playlists(spotifyObject, deviceID):
    playlists = spotifyObject.current_user_playlists()
    dict_playlists = {"red": [], "green": [], "blue": []}
    while playlists:
        for i, playlist in enumerate(playlists['items']):
            # print(playlist["name"], playlist["uri"])
            if (playlist["name"] in ["red", "green", "blue"]):
                playlistTracks = spotifyObject.playlist_tracks(playlist['uri'])
                trackItems = playlistTracks['items']
                for k in range(len(trackItems)):
                    trackItem = trackItems[k]
                    track = trackItem['track']
                    dict_playlists[playlist["name"]].append(track['uri'])
        if playlists['next']:
            playlists = spotifyObject.next(playlists)
        else:
            playlists = None
    return dict_playlists
