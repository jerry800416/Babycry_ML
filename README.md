偵測聲音分類器 ＆ OpenCV動作偵測<br>

聲音種類:男性說話聲、女性說話聲、寶寶哭聲、狗叫聲、貓叫聲

目前困難:
1.狗叫聲無法很好的分辨,所以demo.py裡不顯示
2.寶寶哭聲和貓叫聲無法很好的分辨,所以demo.py裡面不顯示貓叫聲
3.混合的音頻無法很好的辨識
4.無法收集到所有可能發生的音頻,以至於若發生非以上音頻的聲音,model會判斷失誤
5.譜減法降噪使用因環境而異,不太穩定,請斟酌是否要打開




收集與產生資料相關的檔案:
cancleNoise.py:用來讓原本的檔案直接降噪後產生新的檔案(開發測試用)
make_data:用來讓原本的檔案錄製產生新的含噪音的檔案
noise_data.py::用來讓原本的檔案錄製後在經過降噪處理產生新的檔案
playsound.py:循環播放音頻檔案




資料處理與訊號處理相關的檔案:
classifire.py: 當初網路上下載的檔案全部混雜在一起,只有用csv檔案做分類依據,這支檔案可以將每個不同的音頻建立個資資料夾並分類好
generater.py:用來產生高低頻率的聲音(開發測試用)
dbtest.py:用來測試頻率的檔案
high_filter.py:高頻濾波(開發測試用)
rename.py:檔案批量改名
sounddraw.py:讀取音頻檔案繪製三維頻譜圖




訓練相關檔案:
traindata資料夾:訓練資料存放處
makeLabel_trainModel:將訓練資料集貼標籤以及traininig model(使用CNN)
RNN.py:使用RNN訓練資料集




測試model相關檔案:
testdata資料夾:測試資料存放處
predict.py:訓練完model測試model準確度的檔案
test.py:訓練完model直接開啟錄音測試的檔案




完成品+lineBot+OpenCV動作偵測:
trueTest資料夾:demo.py錄音的檔案存放處
demo.py:演示用檔案(請開啟這隻檔案)




核心funcction檔案(import):
noise_filter:降噪function(譜減法)
preprocess.py:資料處理的function
record.py:錄音function




使用方法:
1.請先安裝完OpenCV3.4.1版
可參考這篇:https://1drv.ms/w/s!AqSCQ8Yo16yIga8Y5kcYJT8Yu_6gZg
2.pip3 install -r requirements.txt
3.python3 demo.py

