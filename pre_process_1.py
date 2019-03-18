import pandas
from sklearn.model_selection import train_test_split
import numpy as np
import time
from sklearn.externals import joblib
import Recommenders as Recommenders
import Evaluation as Evaluation
base_dir1='F:/New Folder/Collaborative-Filtering-Million-Song-Dataset-master/'
base_dir='F:/New folder/'#Collaborative-Filtering-Million-Song-Dataset-master/
song_df_1 = pandas.read_csv(base_dir1+'train_triplets.txt',header=None)
song_df_1.columns = ['user_id', 'song_id', 'listen_count']

#songs_metadata_file = 'https://static.turi.com/datasets/millionsong/song_data.csv'
song_df_2 =  pandas.read_csv(base_dir+'song_data.csv')

#Merge the two dataframes above to create input dataframe for recommender systems
song_df = pandas.merge(song_df_1, song_df_2.drop_duplicates(['song_id']), on="song_id", how="left")



song_df.head()
len(song_df)
#song_df = song_df.head(10000)

#Merge song title and artist_name columns to make a merged column
song_df['song'] = song_df['title'].map(str) + " - " + song_df['artist_name']
song_df.to_csv(base_dir+'song_df_all.csv')

def most_popular():

    song_grouped = song_df.groupby(['song']).agg({'listen_count': 'count'}).reset_index()
    grouped_sum = song_grouped['listen_count'].sum()
    song_grouped['percentage']  = song_grouped['listen_count'].div(grouped_sum)*100
    return song_grouped.sort_values(['listen_count', 'song'], ascending = [0,1])

def load_data():
    global base_dir
    song_df=pandas.read_csv(base_dir+'song_df.csv')
    return song_df

def init_recommender(df):
    pm = Recommenders.popularity_recommender_py()
    pm.create(df, 'user_id', 'song')
    return pm


#unique users
users = song_df['user_id'].unique()
len(users)


###Fill in the code here
songs = song_df['song'].unique()
len(songs)


#split
train_data, test_data = train_test_split(song_df, test_size = 0.20, random_state=0)
print(train_data.head(5))

def popularity_based(user_id):
    song_df=load_data()
    users = song_df['user_id'].unique()
    songs = song_df['song'].unique()
    train_data, test_data = train_test_split(song_df, test_size=0.20, random_state=0)
    pm=init_recommender(train_data)
    return pm.recommend(user_id)


user_id = users[5]
pm.recommend(user_id)

user_id = users[8]
pm.recommend(user_id)


#def item_similarity(user_id):
is_model = Recommenders.item_similarity_recommender_py()
is_model.create(train_data, 'user_id', 'song')


user_id = users[5]
user_items = is_model.get_user_items(user_id)
#
print("------------------------------------------------------------------------------------")
print("Training data songs for the user userid: %s:" % user_id)
print("------------------------------------------------------------------------------------")

for user_item in user_items:
    print(user_item)

print("----------------------------------------------------------------------")
print("Recommendation process going on:")
print("----------------------------------------------------------------------")

#Recommend songs for the user using personalized model
is_model.recommend(user_id)


#recommend based on item
#def similar_songs(song)
is_model = Recommenders.item_similarity_recommender_py()
is_model.create(train_data, 'user_id', 'song')
is_model.get_similar_items(['U Smile - Justin Bieber'])
