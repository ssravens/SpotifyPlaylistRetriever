"""Download songs from spotify playlist to a folder"""
import os
import re

from pytube import YouTube
from pytube.exceptions import VideoUnavailable
import moviepy.editor as mp
import urllib.request
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials

# load credentials from .env file
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID", "")
CLIENT_SECRET = os.getenv("CLIENT_SECRET", "")

# change for your target playlist
PLAYLIST_LINK = ""
SAVE_PATH = ""

# authenticate
client_credentials_manager = SpotifyClientCredentials(
    client_id=CLIENT_ID, client_secret=CLIENT_SECRET
)

# create spotify session object
session = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# get uri from https link
if match := re.match(r"https://open.spotify.com/playlist/(.*)\?", PLAYLIST_LINK):
    playlist_uri = match.groups()[0]
else:
    raise ValueError("Expected format: https://open.spotify.com/playlist/...")

# get list of tracks in a given playlist (note: max playlist length 100)
tracks = session.playlist_tracks(playlist_uri)["items"]

# extract name and artist, search on youtube for song (take 1st result), downloads mp4 to specified folder
result = []
urls = []
for track in tracks:
    name = track["track"]["name"]
    artists = ", ".join(
        [artist["name"] for artist in track["track"]["artists"]]
    )
    result = name + " " + artists
    search_result = result
    search_result = search_result.replace(" ", "+")
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_result)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    urls = ("https://www.youtube.com/watch?v=" + video_ids[0])
    yt = YouTube(str(urls))
    video = yt.streams.filter(only_audio=True).first()
    try:
        out_file = video.download(output_path=SAVE_PATH)
    except VideoUnavailable:
        continue
    # base, ext = os.path.splitext(out_file)
    # new_file = base + '.mp4'
    # os.rename(out_file, new_file)
    print(yt.title + " has been successfully downloaded.")
exit()