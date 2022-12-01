"""Download songs from spotify playlist to a folder"""
import os
import re

from pytube import YouTube
import PySimpleGUI as sg
import moviepy.editor as mp
import urllib.request
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials



def extract():
    # load data from user input
    CLIENT_ID = values[0]
    CLIENT_SECRET = values[1]
    PLAYLIST_LINK = values[2]
    SAVE_PATH = values[3]
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
        except:
            print("Failed to download")
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp4'
        os.rename(out_file, new_file)
        print(yt.title + " has been successfully downloaded.")

form = sg.FlexForm('Playlist Retriever')
layout = [
          [sg.Text('Please enter your Client ID, Client Secret, and Playlist URL')],
          [sg.Text('Client ID', size=(15, 1)), sg.InputText()],
          [sg.Text('Client Secret', size=(15, 1)), sg.InputText()],
          [sg.Text('Playlist URL', size=(15, 1)), sg.InputText()],
          [sg.Text('Choose A Folder', size=(35, 1))],
          [sg.Text('Your Folder', size=(15, 1), auto_size_text=False, justification='right'),
           sg.InputText(), sg.FolderBrowse()],
          [sg.Submit(), sg.Cancel()]
         ]
window = sg.Window('Playlist Retriever', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break

    if event == 'Submit':
        extract()

window.close()
exit()

if __name__ == '__extract__':
    extract()
