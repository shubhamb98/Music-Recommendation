import pandas as pd
import numpy as np
base_dir='F:/New folder/'
song_df=pd.read_csv(base_dir+'song_df.csv')
print('HEojfdsklghndsjlkfgjds')
def most_popular():

    song_grouped = song_df.groupby(['song']).agg({'listen_count': 'count'}).reset_index()
    grouped_sum = song_grouped['listen_count'].sum()
    song_grouped['percentage']  = song_grouped['listen_count'].div(grouped_sum)*100
    return song_grouped.sort_values(['listen_count', 'song'], ascending = [0,1])