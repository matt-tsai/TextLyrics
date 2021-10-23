from flask import Flask, request, jsonify
app = Flask(__name__)

import requests
import lyricsgenius
from pprint import pprint

SPOTIFY_GET_CURRENT_TRACK_URL = 'https://api.spotify.com/v1/me/player/currently-playing'
SPOTIFY_ACCESS_TOKEN = 'BQAcvg2pob-WID89gThgt8kV5fRMhVx-TV3zAAOPMbMYblq6NiLso8E9JEs7QibcvLfLoG0fCqAY9THiDEpo6FTMPv8NtAAjNcMCDM8k9qSkZESMMxLec7qo1awWTdFqeZTCWR6eNOdMfc6QiwadJDO6C8716RSbijjSIIcY'
GENIUS_ACCESS_TOKEN = 'bYgIwxrrSVrNgyC9lKIXi-Q40BxI1o7pda5RgXyEeRvZjHotfizmANoX7R6zdd0Y'
genius = lyricsgenius.Genius(GENIUS_ACCESS_TOKEN)


def get_current_track(access_token):
    response = requests.get(
        SPOTIFY_GET_CURRENT_TRACK_URL,
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )
    json_resp = response.json()

    track_id = json_resp['item']['id']
    track_name = json_resp['item']['name']
    artists = [artist for artist in json_resp['item']['artists']]
    artist_names = [artist['name'] for artist in artists][0]

    current_track_info = {
    	"id": track_id,
    	"track_name": track_name,
    	"artists": artist_names
    }
    return current_track_info

def get_song_lyrics(artistName, songName):
    song = genius.search_song(artistName, songName)
    if song == None:
        return None
    
    songLyrics = song.lyrics.split("\n\n")
    tLen = len(songLyrics[len(songLyrics)-1])
    songLyrics[len(songLyrics)-1] = songLyrics[len(songLyrics)-1][:tLen-27]
    return "\n\n".join(songLyrics)

def get_song_lyrics_index(artistName, songName):
    song = genius.search_song(artistName, songName)
    if song == None:
        return None
    
    songLyrics = song.lyrics.split("\n\n")
    tLen = len(songLyrics[len(songLyrics)-1])
    songLyrics[len(songLyrics)-1] = songLyrics[len(songLyrics)-1][:tLen-27]
    return "<br><br>".join(songLyrics)

def get_song_link(artistName, songName):
    song = genius.search_song(artistName, songName)
    if song == None:
        return None
    else:
        return song.url 

@app.route('/')
def index():
    current_track_info = get_current_track(SPOTIFY_ACCESS_TOKEN)
    song = get_song_lyrics_index(current_track_info['track_name'], current_track_info['artists'])
    if song == None:
        return "Couldn't find lyrics on Genius"
    else:
        return "<h2>"+song+"</h2>"

@app.route('/songlink')
def songLink():
    current_track_info = get_current_track(SPOTIFY_ACCESS_TOKEN)
    song = get_song_link(current_track_info['track_name'], current_track_info['artists'])
    if song == None:
        return "Couldn't find song on Genius"
    else:
        return song

@app.route('/songlyrics')
def songLyrics():
    current_track_info = get_current_track(SPOTIFY_ACCESS_TOKEN)
    song = get_song_lyrics(current_track_info['track_name'], current_track_info['artists'])
    if song == None:
        return "Couldn't find lyrics on Genius"
    else:
        return song


#Scrapped code 


# def main():
#     current_track_info = get_current_track(SPOTIFY_ACCESS_TOKEN)
#     song = get_song_lyrics(current_track_info['track_name'], current_track_info['artists'])
#     if song == None:
#         print("Couldn't find lyrics on Genius")
#     else:
#         for x in song:
#             print(x)
# if __name__ == '__main__':
#     main()
# @app.route('/post', methods=["POST"])
# def testpost():
#      input_json = request.get_json(force=True) 
#      dictToReturn = {'text':input_json['text'], 'ee':'ree'}
#      return jsonify(dictToReturn)