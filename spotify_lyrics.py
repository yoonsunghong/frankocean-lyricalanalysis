import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError

#getting username from terminal
username = sys.argv[1]

#User permission
try:
	token = util.prompt_for_user_token(username)
except:
	os.remove(f".cache-{username}")
	token = util.prompt_for_user_token(username)

#creating the spotify object
spotify_object = spotipy.Spotify(auth = token)

#saving user as an object
user = spotify_object.current_user()

displayName = user['display_name']
follower_count = user['followers']['total']

while True:
	print()
	print(">>> Hello " + displayName + "!")
	print(">>> Your followers count: " + str(follower_count) + ".")
	print()
	print("0 - Search an artist")
	print("1 - Exit")
	print()
	choice = int(input("Your choice: "))

	#if user chooses search an artist
	if choice == 0:
		print()
		search_query = input("Ok, what's their name?: ")
		print()

		#searching an artist
		search_results = spotify_object.search(search_query, 1, 0, "artist")
		artist = search_results['artists']['items'][0]
		print(artist['name'])
		print(artist['genres'][0])
		print()
		webbrowser.open(artist['images'][0]['url'])
		artistID = artist['id']

		#albums and tracks
		trackURIs = []
		trackArt = []
		n = 0

		album_results = spotify_object.artist_albums(artistID)
		album_results = album_results['items']

		for album in album_results:
			print("ALBUM " + album['name'])
			albumID = album['id']
			albumArt = album['images'][0]['url']

			#extracting tracks
			track_results = spotify_object.album_tracks(albumID)
			track_results = track_results['items']

			for song in track_results:
				print(str(n) + ": " + song['name'])
				trackURIs.append(song['uri'])
				trackArt.append(albumArt)
				n += 1
			print()

		#showing album art
		while True:
			SelectSong = input("Enter the song number to see album art associated with the song number: ")
			if SelectSong == "x":
				break
			webbrowser.open(trackArt[int(SelectSong)])


	if choice == 1:
		break

# print(json.dumps(VARIABLE, sort_keys = True, indent = 4))