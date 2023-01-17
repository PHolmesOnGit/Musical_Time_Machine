# This project asks the user for a date as an input, and then it uses webscraping and requests to return a
# Spotify playlist of the top 100 songs on the date the user gives

import requests
import json
from bs4 import BeautifulSoup
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = os.environ["Client_ID"]
CLIENT_SECRET = os.environ["Client_Secret"]

sp = spotipy.Spotify()

scope = "playlist-modify-private"
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope=scope,
        redirect_uri="http://example.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]

musical_time_machine = input("What year do you want to travel to? Type in a date using YYYY-MM-DD Format: ")

top100_url = f"https://www.billboard.com/charts/hot-100/{musical_time_machine}/"
# Calling the URL, checking status, then turning it into soup
response = requests.request("GET", top100_url)
soup = BeautifulSoup(response.text, "html.parser")
# print(soup.prettify())
song_titles = soup.find_all("h3", class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 "
                                         "lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 "
                                         "u-line-height-normal@mobile-max a-truncate-ellipsis "
                                         "u-max-width-330 u-max-width-230@tablet-only")

artist_titles = soup.find_all("span", class_="c-label a-no-trucate a-font-primary-s lrv-u-font-size-14@mobile-max "
                                             "u-line-height-normal@mobile-max u-letter-spacing-0021 "
                                             "lrv-u-display-block a-truncate-ellipsis-2line u-max-width-330 "
                                             "u-max-width-230@tablet-only")

artist_list = [artist.getText().strip().split("Featuring")[0] for artist in artist_titles]
song_list = [song.getText().strip() for song in song_titles]
print(song_list)
print(artist_list)

song_uris = []
year = musical_time_machine.split("-")[0]
counter = 0

for song in song_list:
    result = sp.search(q=f"track:{song} artist:{artist_list[counter]}", type="track")
    print(song)
    print(artist_list[counter])
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")
    counter += 1


playlist = sp.user_playlist_create(user=user_id, name=f"{musical_time_machine} Billboard 100", public=False)
# print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)