import requests
import base64
import datetime


client_id = ""
client_secret = ""
auth_code = ""

class SpotifyAPI(object):
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    client_id = None
    client_secret = None
    scope = None
    auth_code = None

    token_url = "https://accounts.spotify.com/api/token"
    auth_url = 'https://accounts.spotify.com/authorize'

    def __init__(self, client_id, client_secret, *args,**kwargs):
        super().__init__(*args,**kwargs)
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth_code = auth_code
    
    def get_client_credentials(self):
        client_id = self.client_id
        client_secret = self.client_secret
        if client_secret == None or client_id == None:
            raise Exception("You must set client_id and client_secret")
        client_creds = f"{client_id}:{client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return client_creds_b64.decode()

    def get_token_header(self):
        client_creds_b64 = self.get_client_credentials()
        return {
            "Authorization" : f"Basic {client_creds_b64}"
        }

    def get_token_body(self):
        auth_code = self.auth_code
        return {
            "grant_type": "authorization_code",
            "code" : auth_code,
            "redirect_uri":"http://127.0.0.1:5000/"
        }

    def get_auth_code(self):
        client_id = self.client_id
        auth_url = self.auth_url
        auth_code_url = auth_url + '?response_type=code&client_id=' + client_id +\
            '&redirect_uri=' + 'http://127.0.0.1:5000/' + \
            '&scope=user-read-playback-state'
        return auth_code_url

    def perform_auth(self):
        token_url = self.token_url
        token_data = self.get_token_body()
        token_header = self.get_token_header()
        r = requests.post(token_url, data=token_data, headers=token_header)
        if not r.status_code in range(200,299):
            return False
        data = r.json()
        print(data)
        now = datetime.datetime.now()
        access_token = data["access_token"]
        expires_in = data['expires_in']
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token = access_token
        self.access_token_expires = expires 
        self.access_token_did_expire = expires < now 
        return True


spotify = SpotifyAPI(client_id, client_secret)
print(spotify.perform_auth())
SPOTIFY_ACCESS_TOKEN = spotify.access_token
print(SPOTIFY_ACCESS_TOKEN)

# print(spotify.access_token)
# SPOTIFY_GET_CURRENT_TRACK_URL = 'https://api.spotify.com/v1/me/player'

# def get_current_track(access_token):
#     response = requests.get(
#         SPOTIFY_GET_CURRENT_TRACK_URL,
#         headers={
#             "Authorization": f"Bearer {access_token}"
#         }
#     )
#     json_resp = response.json()

#     track_id = json_resp['item']['id']
#     track_name = json_resp['item']['name']
#     artists = [artist for artist in json_resp['item']['artists']]

#     link = json_resp['item']['external_urls']['spotify']

#     artist_names = ', '.join([artist['name'] for artist in artists])

#     current_track_info = {
#     	"id": track_id,
#     	"track_name": track_name,
#     	"artists": artist_names,
#     	"link": link
#     }

#     return current_track_info

# def main():
#     current_track_id = None
#     spotify = SpotifyAPI(client_id, client_secret)
#     spotify.perform_auth()
#     SPOTIFY_ACCESS_TOKEN = spotify.access_token
#     SPOTIFY_GET_CURRENT_TRACK_URL = 'https://api.spotify.com/v1/me/player'
#     current_track_info = get_current_track(SPOTIFY_ACCESS_TOKEN) 
#     print(current_track_info)

# spotify = SpotifyAPI(client_id, client_secret)
# spotify.perform_auth()
# print(spotify.access_token)








