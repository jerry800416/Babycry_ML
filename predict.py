from preprocess import *
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
from keras.utils import to_categorical
from keras.models import load_model

#讀取model
model = load_model('ASR.h5')
#編譯
# model.compile(loss=keras.losses.categorical_crossentropy,
#               optimizer=keras.optimizers.Adadelta(), 
#               metrics=['accuracy'])
# model.summary()

i = 0

# 預測(prediction)
while 1 :
    mfcc = wav2mfcc('./testdata/cel/cel{}.wav'.format(i))
    #mfcc = wav2mfcc('./dataset(5)/babycry/4-59579-B-20.wav'.format(i))
    if i != 24:
        i += 1
    else:
        break

    mfcc_reshaped = mfcc.reshape(1, 20, 50, 1)
    confidence = np.max(model.predict(mfcc_reshaped))
    label = get_labels()[0]
    results = np.argmax(model.predict(mfcc_reshaped))
    #print("labels=", label)
    print("predict=", label[results],"信心",confidence*100,"%")
    #print(model.predict(mfcc_reshaped))
    
    #print("信心",confidence)
