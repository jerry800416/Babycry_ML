import librosa
import os
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical
import numpy as np
from tqdm import tqdm
# import msaf


DATA_PATH = "./traindata"


# Input: Folder Path
# Output: Tuple (Label, Indices of the labels, one-hot encoded labels)
def get_labels(path=DATA_PATH):
    labels = os.listdir(path)
    label_indices = np.arange(0, len(labels))
    # print(labels)
    # print(label_indices)
    # print(to_categorical(label_indices))
    return labels, label_indices, to_categorical(label_indices)


# 取資料特徵值
def wav2mfcc(file_path, max_len=50):
    wave, sr = librosa.load(file_path, mono=True, sr=16000) 
    # sr:默認採樣率
    # mono:true 轉換為單聲道 
    # offset：在這段時間後開始閱讀（以秒為單位）
    # duration:只加載這麼多音頻（以秒為單位）
    # res_type：重新採樣類型
    # dtype ：數據類型
    wave = wave[::3] #重採樣1/3
    mfcc = librosa.feature.mfcc(wave, sr=16000)
    # mfcc = librosa.feature.chroma_cqt(wave, sr=44100) 
    # mfcc = msaf.features.PCP(wave, sr=None, hop_length=1024, n_bins=84, f_min=27.5, n_octaves=6)

    # If maximum length exceeds mfcc lengths then pad the remaining ones
    if (max_len > mfcc.shape[1]):
        pad_width = max_len - mfcc.shape[1]
        mfcc = np.pad(mfcc, pad_width=((0, 0), (0, pad_width)), mode='constant')

    # Else cutoff the remaining parts
    else:
        mfcc = mfcc[:, :max_len]
    
    return mfcc


#儲存資料、轉換檔案格式
def save_data_to_array(path=DATA_PATH, max_len=100):
    labels, _, _ = get_labels(path)


    for label in labels:
        try:
          # Init mfcc vectors
          mfcc_vectors = []

          wavfiles = [path + '/' + label + '/' + wavfile for wavfile in os.listdir(path + '/' + label)]
          
          #for wavfile in wavfiles:
          for wavfile in tqdm(wavfiles, "Saving vectors of label - '{}'".format(label)):
              mfcc = wav2mfcc(wavfile, max_len=max_len)
              mfcc_vectors.append(mfcc)
          np.save(label + '.npy', mfcc_vectors)
        except NotADirectoryError as e:
          #skip file
          print(e)


#分割資料集
def get_train_test(split_ratio=0.8, random_state=88):
    # Get available labels
    labels, indices, _ = get_labels(DATA_PATH)

    # Getting first arrays
    X = np.load(labels[0] + '.npy')
    y = np.zeros(X.shape[0])

    # Append all of the dataset into one single array, same goes for y
    for i, label in enumerate(labels[1:]):
        x = np.load(label + '.npy')
        X = np.vstack((X, x))
        y = np.append(y, np.full(x.shape[0], fill_value= (i + 1)))

    assert X.shape[0] == len(y)

    return train_test_split(X, y, test_size= (1 - split_ratio), random_state=random_state, shuffle=True)



# def prepare_dataset(path=DATA_PATH):
  
#     labels, _, _ = get_labels(path) 
#     data = {}
#     for label in labels:
          
#         print('#prepare_dataset label:', label)
        
#         try:
#           data[label] = {}
#           data[label]['path'] = [path  + '/' + label + '/' + wavfile for wavfile in os.listdir(path + '/' + label)]

#           vectors = []
          
#           print("data[label]['path']", data[label]['path'])

#           for wavfile in data[label]['path']:
#               wave, sr = librosa.load(wavfile, mono=True, sr=None)
#               # Downsampling
#               wave = wave[::3] #1/3
#               mfcc = librosa.feature.cqt(wave, sr=sr) #https://librosa.github.io/librosa/generated/librosa.feature.mfcc.html 
#               vectors.append(mfcc)

#           data[label]['mfcc'] = vectors
#         except NotADirectoryError as e:
#           #skip file
#           print(e)

#     return data


# def load_dataset(path=DATA_PATH):
#     data = prepare_dataset(path)

#     dataset = []

#     for key in data:
#         for mfcc in data[key]['mfcc']:
#             dataset.append((key, mfcc))

#     return dataset[:100]


# print(prepare_dataset(DATA_PATH))

