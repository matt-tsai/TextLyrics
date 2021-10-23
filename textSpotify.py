import requests
import lyricsgenius
from pprint import pprint



SPOTIFY_GET_CURRENT_TRACK_URL = 'https://api.spotify.com/v1/me/player/currently-playing'
SPOTIFY_ACCESS_TOKEN = 'BQAW_BZnvUqVQuL5Ex8QUwzGhFEXV0WCm_FeaH573gJRSzAV-_RkincvrxFP_OW5X-40u_nIA7eApWZ8H9U9ouhG1fL9xNAKjQ8jwL59obN72YXmsWWOea73omgXiya4_wDq9vzpJtekWSkbgOwKTATNHRN6wQ7pY9mPZqle'
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
    return songLyrics


def main():
    current_track_info = get_current_track(SPOTIFY_ACCESS_TOKEN)
    song = get_song_lyrics(current_track_info['track_name'], current_track_info['artists'])
    if song == None:
        print("Couldn't find lyrics on Genius")
    else:
        pprint(song)
    

if __name__ == '__main__':
    main()