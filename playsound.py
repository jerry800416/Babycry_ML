import pyaudio
import wave

p=pyaudio.PyAudio()
chunk=1024  #2014kb
i = 0

while 1 :
    try:
        router = './data/cat/cat{}.wav'.format(i)
        print(router)
        wf=wave.open(router,'rb')
        stream=p.open(format=p.get_format_from_width(wf.getsampwidth()),channels=wf.getnchannels(),rate=wf.getframerate(),output=True)
        if i == 119:
            i = 0
        else:
            i+=1
        data = wf.readframes(chunk)  # 读取数据
        #print(data)

        while data != b'':  # 播放
            stream.write(data)
            data = wf.readframes(chunk)
            #print('while循环中！')
            #print(data)

        stream.stop_stream()   # 停止数据流
        stream.close()
        # p.terminate()  # 关闭 PyAudio
        
        print(i)

    except:
        if i == 159:
            i == 0
        else:
            i+=1
        continue