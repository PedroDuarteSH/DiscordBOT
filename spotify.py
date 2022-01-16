import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def spotify(url):
	if "playlist" in url[0]:
		return spotifyPlaylist(url[0])
	elif "track" in url[0]:
		print("here")
		return [spotifyTrack(url[0])]

def spotifyTrack(url):
	sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
	track = sp.track(url)
	return get_name(track)


def spotifyPlaylist(url):
	output = []
	sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
	playlist = sp.playlist_tracks(url)["items"]
	for item in playlist:
		output += [get_name(item['track'])]
	return output

def get_name(track):
	name = track['name']
	for i in track['artists']:
		name += " " + i['name']
	return name