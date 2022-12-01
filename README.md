# Spotify Playlist Retriever
This program retrieves your chosen Spotify playlist and searches Youtube for each song, then downloads them to a folder.

## Why?
If you're broke like me or just don't want to pay for Spotify, you can use this app to listen to songs for free easily (just use a free music player and scan your songs folder)

## What's needed?
- pytube
- spotipy

Install these by running:

pip install pytube

pip install spotipy



## How to Use
To make use of the spotipy package, you need to create an app at the developer.spotify.com website. For this, follow these steps:

1. Browse to https://developer.spotify.com/dashboard/applications.

2. Log in with your Spotify account.

3. Click on ‘Create an app’.

4. Pick an ‘App name’ and ‘App description’ of your choice and mark the checkboxes.

5. After creation, you see your ‘Client Id’ and you can click on ‘Show client secret` to unhide your ’Client secret’.

### PlaylistRetriever.py

Edit the CLIENT_ID and CLIENT_SECRET values in the .env file.

Copy your chosen playlist link and paste it into PLAYLIST_LINK

Put your chosen directory into SAVE_PATH

### If you don't know how to work with code, just run PlaylistRetrieverGUI.py

Enter your Client ID, Client Secret, Playlist URL, and Choose a Folder, then click Submit