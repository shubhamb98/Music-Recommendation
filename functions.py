import pandas
from sklearn.model_selection import train_test_split
import numpy as np
import time
from sklearn.externals import joblib
import Recommenders as Recommenders
import Evaluation as Evaluation
import subprocess,os
import extract_and_store_spectrograms
import label_image

base_dir='F:/New Folder/'
song_df = pandas.read_csv(base_dir + 'song_df.csv')
users = song_df['user_id'].unique()
songs = song_df['song'].unique()

print("Hello Function")

def load_data():
    global base_dir
    song_df=pandas.read_csv(base_dir+'song_df.csv')
    return song_df

def init_recommender(df):
    pm = Recommenders.popularity_recommender_py()
    pm.create(df, 'user_id', 'song')
    return pm

def popularity_based(user_id=users[1]):
    global song_df
    global users
    global songs
    pm=init_recommender(song_df)
    return pm.recommend(user_id)

def item_similarity(user_id):
    global song_df
    global users
    global songs
    is_model = Recommenders.item_similarity_recommender_py()
    is_model.create(song_df, 'user_id', 'song')
    x=is_model.recommend(user_id)
    return x

def similar_songs(song):
    global song_df
    global users
    global songs
    is_model = Recommenders.item_similarity_recommender_py()
    is_model.create(song_df, 'user_id', 'song')
    x=is_model.get_similar_items([song])
    return x


def cnn_model(filename):
    base_path='C:/Users/HP/Desktop/Music-Recommendation/uploads'
    #path=base_path+file
    os.chdir(base_path)
    os.system('2_mp3_to_wav.sh')
    extract_and_store_spectrograms.wav_to_image()
    jpeg_path=base_path+'/'+filename+'.jpeg'
    os.chdir('C:/Users/HP/Desktop/Music-Recommendation/')
    x=label_image.cnn_pred(jpeg_path)
    return x



