import time
linebreak = "~" * 100
def clearQueue(spotifyObject, deviceID):
    for i in range(len(spotifyObject.queue())):
        spotifyObject.next_track(deviceID)
        time.sleep(0.1)
    # spotifyObject.pause_playback(deviceID)
    print("Queue cleared!")
def print_playlists(spotifyObject, deviceID):
    playlists = spotifyObject.current_user_playlists()
    while playlists:
        for i, playlist in enumerate(playlists['items']):
            print(playlist["name"], playlist["uri"])
        if playlists['next']:
            playlists = spotifyObject.next(playlists)
        else:
            playlists = None
def getDevice(spotifyClient):
  laptop = [x for x in spotifyClient.devices()['devices'] if x['name'] == "Benjamin’s MacBook Pro"] #laptop
  tv = [x for x in spotifyClient.devices()['devices'] if x['id'] == "7ad217996fa91ef7df0408e1d8057415bb4667c5"] # suites TV
  projector = [x for x in spotifyClient.devices()['devices'] if x['id'] == "7cb0e9bcb58e0cdba910a8ed006b7c41a8692f68"]  #projector
  if len(tv) > 0:
    device = tv[0]
  elif len(projector) > 0:
    device = projector[0]
  elif len(laptop) > 0:
    device = laptop[0]
  else:
    print("Could not find a device to play on!")
    return False
  return device
def getDeviceID(spotifyClient):
  device = getDevice(spotifyClient)
  if device:
     return device["id"]
  return False