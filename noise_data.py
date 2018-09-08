from record import *
import time
from noise_filter import *

r = recoder()
a = 0

while 1 :
    try:
         
        #開始錄音
        r.recoder()
        #存檔
        r.savewav("./makeData/noiseDog/noiseDog{}.wav".format(a))

        openFile = "./makeData/noiseDog/noiseDog{}.wav".format(a)
        endFile = "./makeData/cleanDog/cleanDog{}.wav".format(a)
        first = 0
        noise_filter(openFile,endFile,first)

        # mfcc = wav2mfcc('noise{}.wav'.format(noisedata))
        a += 1
        # mfcc_reshaped = mfcc.reshape(1, 20, 11, 1)
        # print("labels=", get_labels())
        # print("predict=", np.argmax(model.predict(mfcc_reshaped)))
    except:
        continue

    time.sleep(1)