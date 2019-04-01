import spotipy
import spotipy.util
import pandas
import functions
# results = spotify.search(q='artist:' + name, type='artist')
# print (results)

song_artist_df=pandas.DataFrame(columns=['song','artist'])
tracksList=[]
token = spotipy.util.prompt_for_user_token(username='sourya156', scope='playlist-modify-private,playlist-modify-public', client_id='9ab8af1e507a41f6a0afbedf41d4d4be', client_secret='b00a8f49b6544559a33dc0fbf1d9ba9d',redirect_uri='https://localhost:8080' )
spManager = spotipy.Spotify(auth=token)


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

sdf=functions.item_similarity(functions.users[4])
saf=song_artist_df_generator(sdf)
res=create_playlist(saf,playlist_name='yo')