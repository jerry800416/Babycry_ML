import cv2
import time
import keras
import numpy as np
import threading            #多執行緒
import datetime

from keras.models import load_model
from scipy.io import wavfile
from scipy import signal

from noise_filter import *  #降噪function
from record import *        #錄音function
from preprocess import *    #整理資料function

from linebot import (
    LineBotApi, WebhookHandler
)                                     #Linebot
from linebot.exceptions import (
    InvalidSignatureError
)                                      #Linebot
from linebot.models import *            #Linebot


########################################################################################

#參數設定
key = None                   # 判定是否關閉程式
switch = False               # 判定d
result = ''                  # 預測結果接收參數
pt2 = 0                      # 判定時間,以避免一直line訊息 
# line API key
line_bot_api = LineBotApi('pTY9J+buz1s5ll/W5am0X8/Pm0s1NG1q5zp7etGVxFJMlNvuCC3BEatzG1vYSv4pIpyyO8y3CJKwa8CBe/7xIbneIJSOPM4gzt29ptfdakki13LhBaqzuy+EVcR6f2LMFGGyS5zV2RtO9AmwCi/3TwdB04t89/1O/w1cDnyilFU=')

#錄音加上預測
def predict():
  model = load_model('ASR.h5') #讀取model
  #無窮迴圈
  while 1 :
    try:
      if switch == True:
        r = recoder() #實例化錄音程式
        #開始錄音
        print('偵測到動作,開始錄音!')
        r.recoder()
        #偵測聲音響度
        noise = r.dbtest()
        print('響度',noise)
        if noise > 3000 :
          #存檔
          openFile = './trueTest/recorder0.wav'
          # endFile = './trueTest/filter_recorder{}.wav'.format(first)
          r.savewav('./trueTest/recorder0.wav')
          #去噪(背景相減法)
          # noise_filter(openFile,endFile,first)
          #將音頻做特徵值的提取
          mfcc = wav2mfcc(openFile)
          mfcc_reshaped = mfcc.reshape(1, 20, 50, 1)
          # 定義信心指數顯示格式
          confidence = np.max(model.predict(mfcc_reshaped))*100
          confidence = '%.2f' % confidence
          # label = 所有分類類別(提取自preprocess中function)
          label = get_labels()[0]
          # model 預測
          results = np.argmax(model.predict(mfcc_reshaped))
          # 計算現在時間
          pt = int(datetime.datetime.now().strftime("%M"))
          # if label[results]  == 'dog':
          #   label[results]  = 'noise'
          #因為現在還不能很好的分辨貓叫和嬰兒哭聲,所以先寫死,之後在修改(TODO)
          if label[results]  == 'cat':
            label[results]  = 'babycry'
            #時間判斷,若前後小於3分鐘,就不會發送line通知
            if pt -pt2 > 3 :
              send_alarm()
              global pt2
              pt2 = int(datetime.datetime.now().strftime("%M"))
          if label[results]  == 'babycry':
            pt = int(datetime.datetime.now().strftime("%M"))
            if pt -pt2 > 3 :
              send_alarm()
              global pt2
              pt2 = int(datetime.datetime.now().strftime("%M"))
          global pt2
          global result
          #若信心指數小於30% 將會顯示I don't know
          if float(confidence) < 30:            
            result = 'I don\'t know'
          else:
            result = label[results]+'  confidence:'+confidence+'%'
            #預測出結果後會停止錄音,除非偵測到新的動作產生
          global switch
          switch = False
          # print(result)
        else:
          #如果響度小於3000,直接判定成silence
          result = 'silence'
          global switch
          switch = False
        #打印出預測結果和信心度
        print(result)
      else :
        continue

      #中斷指令
      global key
      #print(key)
      if key == ord('q'):
        #print('key')
        break
    except:
      continue

# 寄送line訊息
def send_alarm(): 
	pt = datetime.datetime.now().strftime("%H:%M:%S")
  #line 接收訊息的user developer ID
	line_bot_api.multicast(['U2311c55d2df0337059d20c7bce8fdc9f', 'U493e1e22128374c5acbecd583eb411fa', 'Uefbad5d2ac551bab8ad9329c51d97929','U7af0a3144cd9250d245004b1b2b34e70'], TextSendMessage(text='Baby is crying...' + pt + '.'))

# 建立一個子執行緒(錄音)
t = threading.Thread(target = predict)

# 執行子執行緒
t.start()

# 主執行緒繼續執行
# 開啟網路攝影機
cap = cv2.VideoCapture(0)

# 設定影像尺寸
width = 900
height = 675

# 設定擷取影像的尺寸大小
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

# 計算畫面面積
area = width * height

# 初始化平均影像
ret, frame = cap.read()
#均值慮波(影像平滑化、模糊化)kernal = 4*4
avg = cv2.blur(frame, (4, 4))
#將初始影像轉化為32位數浮點數
avg_float = np.float32(avg)
a = 0
#影像輸出
while(cap.isOpened()):
  #讀取一幅影格
  ret, frame = cap.read()
  #若讀取至影片結尾，則跳出
  if ret == False:
    break
  #均值慮波(影像平滑化、模糊化)kernal = 4*4
  blur = cv2.blur(frame, (4, 4))
  # 計算目前影格與平均影像的差異值
  diff = cv2.absdiff(avg, blur)
  # 將圖片轉為灰階
  gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
  # 篩選出變動程度大於閥值的區域
  ret, thresh = cv2.threshold(gray, 25, 255, cv2.THRESH_BINARY)
  # 使用型態轉換函數去除雜訊
  kernel = np.ones((5, 5), np.uint8)
  thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
  thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)
  # 產生等高線
  cntImg, cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  for c in cnts:
    # 忽略太小的區域
    if cv2.contourArea(c) < 2500:
      continue
    # 偵測到物體，可以自己加上處理的程式碼在這裡...
    global switch
    switch = True
    # 計算等高線的外框範圍
    (x, y, w, h) = cv2.boundingRect(c)
    # 畫出外框
    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 5)
  #如果錄音開關有打開 在畫面左上角顯示recording
  if switch == True:
    cv2.putText(frame, "recording!!!", (10, 30),cv2.FONT_HERSHEY_TRIPLEX, 1.0, (255, 0, 255), 2)
  #如果預測結果不等於空(代表有結果),在畫面左上角顯示預測結果
  if result != '' :
    b = 40
    #print('result:',result)
    if  b > 0 or switch == False:
      cv2.putText(frame, "{}".format(result), (10, 80),cv2.FONT_HERSHEY_TRIPLEX, 1.0, (255, 0, 255), 2)
      b -= 1
    else :
      global result
      result = ''
  # 畫出等高線（除錯用）
  #cv2.drawContours(frame, cnts, -1, (0, 255, 255), 5)
  # 顯示偵測結果影像
  cv2.imshow('frame', frame)
  global key
  key = cv2.waitKey(1) & 0xFF
  if key == ord('q'):
    break
  # 更新平均影像(背景影像)
  cv2.accumulateWeighted(blur, avg_float, 0.1)
  avg = cv2.convertScaleAbs(avg_float)

cap.release()
cv2.destroyAllWindows()


