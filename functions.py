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
import spotipy
import spotipy.util


base_dir='F:/New Folder/'
song_df = pandas.read_csv(base_dir + 'song_df.csv')
users = song_df['user_id'].unique()
songs = song_df['song'].unique()

print("Hello Function")

####Spotify data
song_artist_df=pandas.DataFrame(columns=['song','artist'])
tracksList=[]
token = spotipy.util.prompt_for_user_token(username='sourya156', scope='playlist-modify-private,playlist-modify-public', client_id='9ab8af1e507a41f6a0afbedf41d4d4be', client_secret='b00a8f49b6544559a33dc0fbf1d9ba9d',redirect_uri='https://localhost:8080' )
spManager = spotipy.Spotify(auth=token)


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

def song_artist_df_generator(out_df):
    a = []
    b=[]
    for index,row in out_df.iterrows():
        x=str(row['song'])
        xx=x.split('-')
        a.append(xx[0])
        b.append(xx[1])
    song_artist_df['song']=a
    song_artist_df['artist']=b
    return song_artist_df

def searchTrack(spManager,tracksList,name,artist):
    song_str = name + " by " + artist
    print ("Searching for " + song_str)

    res = spManager.search(q='artist:'+ artist + ' track:' + name,type="track")

    tracks = res['tracks']['items']

    if len(tracks) < 1:
        print (song_str + " not found!")
        return

    track = res['tracks']['items'][0]
    tracksList.append(track['id'])
    print (song_str + ' added.')
    return tracksList



def create_playlist(song_artist_df,playlist_name='test'):

    for index,row in song_artist_df.iterrows():
        searchTrack(spManager, tracksList, song_artist_df.iloc[index].song, song_artist_df.iloc[index].artist)

    playlist = spManager.user_playlist_create('sourya156',playlist_name,False)

    spManager.user_playlist_add_tracks('sourya156',playlist['id'],tracksList)
    return playlist['external_urls']['spotify']

