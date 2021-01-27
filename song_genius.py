#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 16:11:07 2021

@author: karthikarumugam
"""

# import the libraries
import pandas as pd
import random
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id="06d4d3c9cc864dba9b53fc580484930f",
    client_secret="9be1835fc8074231a8b09a1ac9b74ed0"))


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
    hot_songs = pd.read_csv("data/hot_100_songs.csv").drop("Unnamed: 0", axis=1)["song"]

    # Drop the NAs in the pandas data series
    hot_songs.dropna(inplace=True)
    
    # Convert the series to a list
    hot_song_list = hot_songs.to_list()
    
    # Check if the song entered by the user is in the hot_songs_list
    if song_title in hot_song_list:
        # remove the user song from the list
        hot_song_list.remove(song_title)
        
        # get a random index to pick a song from the list
        random_index = random.randint(0, len(hot_song_list))
        
        return hot_song_list[random_index]
    else:
        return None
    

# x =  get_hot_song("Go Crazie")

# if x == None:
#     print("Song not found")
# else:
#     print(x)
    

def get_audio_features(song_title):
    """
    

    Parameters
    ----------
    song_title : string
        The title of the string entered by the user.

    Returns
    -------
    Dictionary of audio features for the song_title extracted from spotify

    """
    
    result = sp.search(song_title, limit=1)
    
    return sp.audio_features(result["tracks"]["items"][0]["uri"])


#print(get_audio_features("Go Crazy"))
