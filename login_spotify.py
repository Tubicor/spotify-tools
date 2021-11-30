from credentials import client_id, client_secrect
import time

import spotipy
from spotipy.oauth2 import SpotifyOAuth

def save_to_txt(_string, filename):
    with open(filename,"w",encoding="utf-8") as file:
        file.write(f"{_string}")
def append_to_txt(_string, filename):
    with open(filename,"a",encoding="utf-8") as file:
        file.write(f"\n# {_string}")

def connect_with_spotipy_to_web_api():
    scope = "user-library-read"
    auth_manager = SpotifyOAuth(client_id= client_id, client_secret= client_secrect, redirect_uri= "https://localhost", scope=scope)
    sp = spotipy.Spotify(oauth_manager= auth_manager)

    return sp

def get_list_of_all_saved_songs(sp):
    # with first query get overall number of saved tracks
    index_saved_tracks = 0
    max_saved_tracks = -1
    limit = 50
    list_artist_track = list()
    while index_saved_tracks < max_saved_tracks or max_saved_tracks == -1:
        results = sp.current_user_saved_tracks(limit = limit ,offset=index_saved_tracks)
        if max_saved_tracks == -1:
            if type(results['total']) != int:
                raise Exception("Is not int line ~28")
            max_saved_tracks = int(results['total'])        
        for item in results['items']:
            list_artist_track.append(f"{ item['track']['artists'][0]['name']} - {item['track']['name']}")
        index_saved_tracks = index_saved_tracks + limit
        time.sleep(0.01)
        print("Scanned to Songindex: ", index_saved_tracks)
        # Json Format of result --> results['XXXX']
        # href: URL the GET was sent to
        # items: 
        #   added_at: date
        #   track:
        #       # album
                # artists
                # available_markets
                # disc_number
                # duration_ms
                # explicit
                # external_ids
                # external_urls
                # href
                # id
                # is_local
                # name
                # popularity
                # preview_url
                # track_number
                # type
                # uri
        # limit, next, offset: Parameter fo the GET Statement
        # previous: 
        # total: Total saved_songs
        # print(type(results['items'][1]))
        # for index, (key,item) in enumerate(results['items'][1]['track'].items()):
        #     print(f"Index: {key} ",item)
        #     save_to_txt(item, f"result {key}")
        #     append_to_txt(key, f"result track")
    return list_artist_track
        

if __name__ == "__main__":
        sp = connect_with_spotipy_to_web_api()
        list_songs = get_list_of_all_saved_songs(sp)
        print(list_songs)
        save_to_txt("\n".join(list_songs),"saved_songs.txt")