# A song recommender

A song recommendation algorithm based on musical tastes. The program asks for a user's favorite song title, and first searches it on the spotify database and confirms if the title of the song is connected with the relevant artist. The program also checks if the song appears in the top 100 songs on the US billboard and recommends another random song from the billboard list. Alternatively, if the song is not listed on the billboard, it uses audio features from the user's preferred song title and recommends 5 other songs related to the preferred song.

## Code

__extract_songs_features.ipynb__ - notebook for creating a database of audio features of songs extracted from Spotify.
__audio_clusters.py__ - the clustering algorithm for the song recommendation.
__song_genius.py__ - the main program with the user interface for selection and recommendation of songs.

## Models

Pickled models for the K-means clustering algorithm and parameters.

## Data
__all_playlists_track_info.csv__ - a database of audio features for songs extracted from Spotify.
__hot_100_songs.csv__ - the hot 100 songs on the US billboard.
