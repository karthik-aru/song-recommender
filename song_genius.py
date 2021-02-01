#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 16:11:07 2021

@author: karthikarumugam
"""

# import the libraries
import pandas as pd
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from joblib import dump, load

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id="xxxxxxxxxxxxxxxxxxxx",
    client_secret="xxxxxxxxxxxxxxxxxxxxxxxxxx"))
 
# collecting the local database of spotify tracks with modeling information
all_track_info = pd.read_csv("data/all_playlists_track_info.csv")

def get_hot_song(song_title):
    """
    
    Parameters
    ----------
    song_title : string
        The song name entered by the user

    Returns
    -------
    string
        Returns another song from the hot 100 billboard songs.

    """
    
    #Extract the list of songs from the hot_100_songs.csv table
    hot_songs = pd.read_csv("data/hot_100_songs.csv").drop("Unnamed: 0", axis=1)

    
    # Check if the song entered by the user is in the hot_songs_list
    if song_title in hot_songs["song"].values:
        # remove the user song from the list
        hot_song_list = hot_songs[hot_songs["song"] != song_title]
        
        # get a random index to pick a song from the list
        random_hot_song = hot_song_list.sample(n=1, axis=0)
        
        return random_hot_song.loc[random_hot_song.index[0], "song"] + " by " + random_hot_song.loc[random_hot_song.index[0], "artist"]
    else:
        return "song not found"
    

#print(get_hot_song("Go Crazy"))


def get_audio_features(uri):
    """
    

    Parameters
    ----------
    song_title : string
        The uri of the song track entered by the user.

    Returns
    -------
    Returns a numpy array of audio features for the song track extracted 
    from spotify based on the uri.

    """
    
    #extracting the audio features numbers for danceability, energy, key, 
    #loudness, mode, speechiness, acousticness, instrumentalness, liveness, 
    #valence and tempo
    result = list(sp.audio_features(uri)[0].values())[:11]
    
    #removing the mode and key features
    del result[4]
    del result[2]
    
    # convert the list to a numpy array to reshape it.
    result = np.array(result)
    result = result.reshape(1, -1)
    
    return result


#print(get_audio_features("spotify:track:4vircrVSGNJsFavtLUF29K"))
    
def get_spotify_song_rec(uri_audio_features):
    """
    Accepts a numpy array with the audio features from the uri requested by 
    the user and returns a list of song urls that the user may like.

    Parameters
    ----------
    uri_audio_feature : numpy array
        Acceots a numoy array ocons.

    Returns
    -------
    Returns a list of 5 strings containing external urls of spotify tracks.

    """
    

    
    # collect the clusters column from the K-means modeling
    my_song_clusters = pd.read_csv("models/my_model_clusters.csv")
    my_song_clusters = my_song_clusters.squeeze(axis=1)
    
    #concatenate the clusters with the all_track_info
    all_track_info["cluster"] = my_song_clusters
    
    # Load the transformer for the model
    scaler_wo_mode_key = load('models/scaler_wo_mode_key.joblib')
    
    # transform the uri_audio_features to fit the model
    uri_af_scaled = scaler_wo_mode_key.transform(uri_audio_features)
    
    # Load the k-Means fitted model to get cluster information
    my_kmeans_model = load("models/my_audio_kmeans.joblib")
    
    # Predict the cluster info for the user-selected uri
    cluster_no = my_kmeans_model.predict(uri_af_scaled)[0]
    
    songs_with_cluster_no = all_track_info[all_track_info["cluster"] == cluster_no]
    
    five_songs = songs_with_cluster_no.sample(n=5, axis=0)
    
    return five_songs["uri"].tolist()


#x = get_audio_features("spotify:track:6gZVQvQZOFpzIy3HblJ20F")

#print(get_spotify_song_rec(x))


def get_song_uri(song_title):
    
    song_uri = ""
    search_res = sp.search(song_title, limit=5)
    
    while True:
        if len(search_res["tracks"]["items"]) == 0:
            print("I could not find the song.")
            song_title = input("Would you like to try again with a different title?")
        else:
            print("We found matches for this song with several artists")
            artist_index = 1
            for item in search_res["tracks"]["items"]:
                print(str(artist_index) + ". " + item["artists"][0]["name"])
                artist_index += 1
            artist_choice = int(input("Please pick an artist (1-5): "))
            song_uri = search_res["tracks"]["items"][artist_choice-1]["uri"]
            break

    return song_uri

#print(get_song_uri("Hi Ho Silver"))

def get_song_title():
    
    """

    Returns
    -------
    A string containing the uri for a given song.

    """
    
    song_title = input("Please enter the title of your favourite song: ")
    
    # look for a song in the hot 100 billboard
    hot_song = get_hot_song(song_title.title())

    # give a recommendation from the hot 100 songs     
    if hot_song == "song not found":
        spotify_uri = get_song_uri(song_title)
        song_features = get_audio_features(spotify_uri)
        song_rec = get_spotify_song_rec(song_features)
        
        print("You might also like to listen to:")
        for song in song_rec:
            song_info = all_track_info[all_track_info["uri"] == song]
            rec_song_title = song_info.loc[song_info.index[0], "song_title"]
            rec_song_artists = song_info.loc[song_info.index[0], "artists"]
            rec_song_url = song_info.loc[song_info.index[0], "external_url"]
            print("------------------------------------------------")
            print(rec_song_title + " by "+ rec_song_artists)
            print("Check it out at:", rec_song_url)
            print("------------------------------------------------")
            #webbrowser.open(rec_song_url)
    else:
        print("Hey that's a hot song trending on the billboard.")
        print("------------------------------------------------")
        print("You might like to listen to another hot song:\n" + hot_song)
    
if __name__ == "__main__":
    
    get_song_title()
