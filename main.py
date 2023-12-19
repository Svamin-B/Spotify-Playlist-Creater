import requests
import spotipy
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = "54b98ce24b0c4a479018187fd839a90d"
CLIENT_SEC = "da596d96c83848f78cb6a3459271c844"
REDIRECT_URI = "http://example.com"

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
year = date.split("-")[0]
print(year)

response = requests.get(url=f"https://www.billboard.com/charts/hot-100/{date}/")
web_page = response.text

soup = BeautifulSoup(web_page, "lxml")


titles = soup.select("li ul li h3")
a = [title.getText().strip() for title in titles]
print(a)

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SEC,
        show_dialog=True,
    ))


user_id = sp.current_user()["id"]

song_uris = []
for title in titles:
    title = str(title).split(">")[1]
    title = title.split("<")[0]
    translator = str.maketrans({chr(10): '', chr(9): ''})
    title = str(title).translate(translator)
    print(title)
    result = sp.search(q=f"track:{title} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{title} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False, description=f"Top 100 songs on this date: {date}")
playlist_id = playlist["id"]
sp.playlist_add_items(playlist_id=playlist_id, items=song_uris)

