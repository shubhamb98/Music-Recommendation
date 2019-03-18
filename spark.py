import os
from pyspark.sql.types import *
from pyspark.sql import functions as F

# list directories
base_dir = 'F:/New folder/'
triplets_filename = base_dir + 'train_triplets.txt'

base_dir2 = 'F:/New folder/'
songs2tracks_filename = base_dir2 + 'taste_profile_song_to_tracks.txt'

base_dir3 = 'F:/New folder/'
metadata_filename = base_dir3 + 'Track_metadata.csv'

if os.path.sep != '/':
    # Handle Windows.
    triplets_filename = triplets_filename.replace('/', os.path.sep)
    songs2tracks_filename = songs2tracks_filename.replace('/', os.path.sep)
    metadata_filename = metadata_filename.replace('/', os.path.sep)

# Create schema so the cluster only runs through the data once
plays_df_schema = StructType(
    [StructField('userId', StringType()),
     StructField('songId', StringType()),
     StructField('Plays', IntegerType())]
)

songs2tracks_df_schema = StructType(
    [StructField('songId', StringType()),
     StructField('trackId', StringType())]
)

metadata_df_schema = StructType([
StructField('artist_id', StringType()),
    StructField('artist_name', StringType()),
    StructField('songId', StringType()),
    StructField('title', StringType()),

   ]
)

#####################
from pyspark import SparkContext
sc =SparkContext()
from pyspark.sql import SQLContext
sqlContext = SQLContext(sc)
##################
# load in data
raw_plays_df = sqlContext.read.format('com.databricks.spark.csv') \
    .options(delimiter='\t', header=True, inferSchema=False) \
    .schema(plays_df_schema) \
    .load(triplets_filename)

songs2tracks_df = sqlContext.read.format('com.databricks.spark.csv') \
    .options(delimiter='\t', header=True, inferSchema=False) \
    .schema(songs2tracks_df_schema) \
    .load(songs2tracks_filename)

metadata_df = sqlContext.read.format('com.databricks.spark.csv') \
    .options(delimiter=',', header=True, inferSchema=False) \
    .schema(metadata_df_schema) \
    .load(metadata_filename)

# change ids from strings to integers
userId_change = raw_plays_df.select('userId').distinct().select('userId',
                                                                F.monotonically_increasing_id().alias('new_userId'))
songId_change = raw_plays_df.select('songId').distinct().select('songId',
                                                                F.monotonically_increasing_id().alias('new_songId'))

# get total unique users and songs
unique_users = userId_change.count()
unique_songs = songId_change.count()
print('Number of unique users: {0}'.format(unique_users))
print('Number of unique songs: {0}'.format(unique_songs))

# join dataframes
raw_plays_df_with_int_ids = raw_plays_df.join(userId_change, 'userId').join(songId_change, 'songId')

# remove half users to make more manageable
raw_plays_df_with_int_ids = raw_plays_df_with_int_ids.filter(raw_plays_df_with_int_ids.new_userId < unique_users / 2)

# cache
raw_plays_df_with_int_ids.cache()
raw_plays_df_with_int_ids.show(5)

songs2tracks_df.cache()
songs2tracks_df.show(5)

metadata_df.cache()
metadata_df.show(5)




song_ids_with_total_listens = raw_plays_df_with_int_ids.groupBy('songId') \
                                                       .agg(F.count(raw_plays_df_with_int_ids.Plays).alias('User_Count'),
                                                            F.sum(raw_plays_df_with_int_ids.Plays).alias('Total_Plays')) \
                                                       .orderBy('Total_Plays', ascending = False)

print ('song_ids_with_total_listens:')
song_ids_with_total_listens.show(3, truncate=False)

# Join with metadata to get artist and song title
song_names_with_plays_df = song_ids_with_total_listens.join(metadata_df, 'songId' ) \
                                                      .select('artist_name', 'title', 'songId', 'User_Count','Total_Plays') \
                                                      .orderBy('Total_Plays', ascending = False)

print ('song_names_with_plays_df:')
song_names_with_plays_df.show(20, truncate = False)



##########################COLLABORATIVE FILTERING########################

seed = 1800009193
(split_60_df, split_a_20_df, split_b_20_df) = raw_plays_df_with_int_ids.randomSplit([0.6, 0.2, 0.2], seed = seed)

# Let's cache these datasets for performance
training_df = split_60_df.cache()
validation_df = split_a_20_df.cache()
test_df = split_b_20_df.cache()

print('Training: {0}, validation: {1}, test: {2}\n'.format(
  training_df.count(), validation_df.count(), test_df.count())
)
training_df.show(3)
validation_df.show(3)
test_df.show(3)


validation_df = validation_df.withColumn("Plays", validation_df["Plays"].cast(DoubleType()))
