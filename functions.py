import pandas
from sklearn.model_selection import train_test_split
import numpy as np
import time
from sklearn.externals import joblib
import Recommenders as Recommenders
import Evaluation as Evaluation

base_dir='F:/New Folder/'
song_df = pandas.read_csv(base_dir + 'song_df.csv')
users = song_df['user_id'].unique()
songs = song_df['song'].unique()

print("Heloo Function")

def load_data():
    global base_dir
    song_df=pandas.read_csv(base_dir+'song_df.csv')
    return song_df

def init_recommender(df):
    pm = Recommenders.popularity_recommender_py()
    pm.create(df, 'user_id', 'song')
    return pm