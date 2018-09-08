from noise_filter import *
import time

first = 0
while 1 :
    try: 
        openFile = './testdata/celphone/celphone10.wav'.format(first)
        endFile = './testdata/celphone/celphone12.wav'.format(first)
        #去噪(背景相減法)
        noise_filter(openFile,endFile,first)
        #time.sleep(5) 
        if first != 103 :
            first += 1
            print(first)
            # time.sleep(5) 
        else:
            break
    except:
        first += 1
        print(first)
        continue
    time.sleep(1)



# while 1 :
#     openFile = './traindata/dog/dog{}.wav'.format(first)
#     endFile = './traindata/dog/clean_dog{}.wav'.format(first)
#     #去噪(背景相減法)
#     noise_filter(openFile,endFile,first)
#     #time.sleep(5) 
#     if first != 792 :
#         first += 1
#         print(first)
#         # time.sleep(5) 
#     else:
#         break
#     time.sleep(1)

# openFile = './traindata/dog/dog0.wav'.format(first)
# endFile = './traindata/dog/cleandog0.wav'.format(first)
# noise_filter(openFile,endFile,first)