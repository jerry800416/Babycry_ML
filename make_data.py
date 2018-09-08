from record import *
import time

r = recoder()
noisedata = 0
while 1 :
    try:
        
        #開始錄音
        r.recoder()
        #存檔
        r.savewav("./{}.wav".format(noisedata))
        # mfcc = wav2mfcc('noise{}.wav'.format(noisedata))
        noisedata += 1
        # mfcc_reshaped = mfcc.reshape(1, 20, 11, 1)
        # print("labels=", get_labels())
        # print("predict=", np.argmax(model.predict(mfcc_reshaped)))
    except:
        continue

    time.sleep(1)