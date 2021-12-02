from logging import lastResort
from credentials import client_id, client_secrect


import time
import json
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

def testMethode():
    pass

def get_list_of_saved_songs(sp, offset=0, total_songs=None):

    # returns list
    list_artist_track = list()

    # check for invalid values in parameter
    if offset <= 0:
        raise Exception("Wrong offset")
    if total_songs <= 0:
        raise Exception("Wrong total songs")

    # index to iterate over saved tracks
    index = 0 + offset
    # last index to query
    last_index = index + total_songs
    last_index_must_be_set_to_max = False
    if total_songs is None:
        last_index_must_be_set_to_max = True
    
    #limit query_size to max of 50 (limit of API query) 
    query_size = total_songs if total_songs < 50 else 50

    # iterate while index is smaller than last index or if last index is yet to be set
    while index < last_index or last_index_must_be_set_to_max:
        # query with api for saved songs
        results = sp.current_user_saved_tracks(limit = query_size, offset=index)
        # check for max_possible index and correct it to max if given is greater or nothing is given
        if last_index_must_be_set_to_max or last_index > int(results['total']):
            last_index = results['total']
            last_index_must_be_set_to_max = False
        # iterate over results
        for item in results['items']:
            list_artist_track.append(f"{ item['track']['artists'][0]['name']} - {item['track']['name']}")
        # increment index for possible further querys
        index = index + query_size
        time.sleep(0.001) #TODO
        print("Scanned to Songindex: ", index)
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
        list_songs = get_list_of_saved_songs(sp, offset=666, total_songs=1)
        print(list_songs)
        save_to_txt("\n".join(list_songs),"saved_songs.txt")