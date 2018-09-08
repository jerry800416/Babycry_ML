from record import *
from preprocess import *
import time
import keras
from keras.models import load_model
from scipy.io import wavfile
from scipy import signal
from noise_filter import *


#讀取model
model = load_model('ASR.h5')
#編譯
# model.compile(loss=keras.losses.categorical_crossentropy,
#               optimizer=keras.optimizers.Adadelta(),
#               metrics=['accuracy'])
# model.summary()
#實例化錄音程式
r = recoder() 
first = 0 
#無窮迴圈
while 1 :
    # try:
    #開始錄音
    r.recoder()
    #存檔
    r.savewav("./trueTest/recorder{}.wav".format(first))

    #high-pass filter 高通濾波
    # sr, x = wavfile.read('test.wav')      # 16-bit mono 44.1 khz  
    # b = signal.firwin(10001, cutoff=1000, fs=sr, pass_zero=False)
    # x = signal.lfilter(b, [1.0], x)
    #x = signal.filtfilt(b, [1.0], x)
    # wavfile.write('test2.wav', sr, x.astype(np.int16))

    openFile = './trueTest/recorder{}.wav'.format(first)
    # endFile = './trueTest/filter_recorder{}.wav'.format(first)
    #去噪(背景相減法)
    # noise_filter(openFile,endFile,first)
    #print(first)
    mfcc = wav2mfcc(openFile)
    mfcc_reshaped = mfcc.reshape(1, 20, 50, 1)
    #print(mfcc_reshaped)
    confidence = np.max(model.predict(mfcc_reshaped))
    #print(confidence)
    label = get_labels()[0]
    results = np.argmax(model.predict(mfcc_reshaped))
    #print("labels=", label)
    if label[results]  == 'dog':
        print("predict=", 'noise',"信心",confidence*100,"%")
    elif label[results]  == 'cat':
        print("predict=", 'babycry',"信心",confidence*100,"%")
    else :
        print("predict=", label[results],"信心",confidence*100,"%")
    #if np.argmax(model.predict(mfcc_reshaped)) == 4:
    first += 1
    print(first)

# except:
#     continue

    time.sleep(1) 


