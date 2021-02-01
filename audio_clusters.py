#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 10:56:23 2021

@author: karthikarumugam
"""


import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from joblib import dump, load


def get_kM_clusters():
    """
    Creates the K Means clustering model for the Spotify songs training database.

    Returns
    -------
    None.

    """
    
    all_track_info = pd.read_csv("data/all_playlists_track_info.csv")
    
    X = all_track_info.iloc[:,4:15].copy()
    
    #drop the mode and key columns
    X.drop(["key", "mode"], axis=1, inplace=True)
    
    # perform scale-fitting or normalization of the data
    scaler_wo_mode_key = StandardScaler()
    scaler_wo_mode_key.fit(X)
    
    # store the normalized data model
    dump(scaler_wo_mode_key, 'models/scaler_wo_mode_key.joblib')
    
    #Transform the training data
    X_scaled = scaler_wo_mode_key.transform(X)
    
    # create a K-means model from the training data
    my_audio_kmeans = KMeans(n_clusters=14,
                    init="k-means++",
                    n_init=3,
                    max_iter=40,
                    tol=0,
                    algorithm="full",
                    random_state=350)
    
    my_audio_kmeans.fit(X_scaled)
    
    dump(my_audio_kmeans, 'models/my_audio_kmeans.joblib')
    
    my_model_clusters = my_audio_kmeans.predict(X_scaled)
    
    my_model_clusters = pd.Series(my_model_clusters)
    
    my_model_clusters.to_csv("models/my_model_clusters.csv", index=False)
    

if __name__ == "__main__":
    
    get_kM_clusters()


