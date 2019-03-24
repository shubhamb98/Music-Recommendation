

import librosa
import numpy as np
import os
import scipy.misc

from PIL import Image


def extract_feature(file_name):
    '''
    extract_feature returns the features as specified by melspectrogram for each sound file
    '''
    Y, sample_rate =librosa.load(file_name,sr=2108)
    
    #features = librosa.feature.mfcc(y=Y, sr=sample_rate, n_mfcc=120)
    features = librosa.feature.melspectrogram(y=Y, sr=sample_rate, n_mels=120)

    return features


# Define directory where sound files are stored within '/wav_files_TOTAL/' folder
root = "C:/Users/HP/Desktop/Music-Recommendation/uploads/"
def wav_to_image():
    os.chdir(root)
    filenames=[]
    for file in os.listdir('.'):
        if file.endswith(".wav"):
            filenames.append((os.path.join("", file)))
    print(len(filenames))

    for wav_file in filenames:
        name=str(os.path.splitext(wav_file)[0])
        exists = os.path.isfile(root +name+'.jpeg')
        if not exists:
            print(wav_file)
            npy = extract_feature(os.path.abspath(wav_file))
            dest = root  + name
            scipy.misc.imsave(dest+'.jpeg', npy)
            print(dest)


