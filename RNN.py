# 導入函式庫
from preprocess import * 
import keras
import tensorflow as tf
from keras.models import Sequential ,load_model
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
from keras.utils import to_categorical

#執行貼標籤function
# save_data_to_array(path='./traindata')

# 載入 data 資料夾的訓練資料，並自動分為『訓練組』及『測試組』
X_train, X_test, y_train, y_test = get_train_test()
X_train = X_train.reshape(X_train.shape[0], 20, 100)
X_test = X_test.reshape(X_test.shape[0], 20, 100)

# 類別變數轉為one-hot encoding
y_train_hot = to_categorical(y_train) 
y_test_hot = to_categorical(y_test)
print("X_train.shape=", X_train.shape)

# 建立簡單的線性執行的模型
# model = Sequential()
model = tf.keras.Sequential()
model.add(tf.keras.layers.GRU(512, activation=tf.nn.relu, input_shape=X_train.shape[1:], return_sequences=True)) #compare return_sequences=True
model.add(tf.keras.layers.GRU(256, activation=tf.nn.relu, return_sequences=True))
model.add(tf.keras.layers.Dropout(0.25))
model.add(tf.keras.layers.GRU(128, activation=tf.nn.relu))
model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(640, activation=tf.nn.relu))
model.add(tf.keras.layers.Dropout(0.25))
model.add(tf.keras.layers.Dense(320, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(160, activation=tf.nn.relu))
model.add(tf.keras.layers.Dropout(0.25))
model.add(tf.keras.layers.Dense(80, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(40, activation=tf.nn.relu))
model.add(tf.keras.layers.Dropout(0.25))
model.add(tf.keras.layers.Dense(20, activation=tf.nn.relu))
# model.add(Dense(320, activation=tf.nn.relu))
# model.add(Dense(160, activation=tf.nn.relu))
# model.add(Dense(80, activation=tf.nn.relu))
# model.add(Dense(40, activation=tf.nn.relu))
# model.add(Dense(20, activation=tf.nn.relu))
model.add(tf.keras.layers.Dense(4, activation=tf.nn.softmax))
model.summary()

# # 建立卷積層，filter=32,即 output size, Kernal Size: 2x2, activation function 採用 relu
# model.add(Conv2D(32, kernel_size=(2, 2), activation='relu', input_shape=(20, 50, 1)))
# # 建立池化層，池化大小=2x2，取最大值
# model.add(keras.layers.MaxPool2D(pool_size=(2, 2)))
# # Dropout層隨機斷開輸入神經元，防止過度擬合，斷開比例:0.25
# model.add(keras.layers.Dropout(0.25))
# model.add(keras.layers.Conv2D(64, activation='relu',kernel_size=(2, 2)))
# model.add(keras.layers.MaxPool2D(pool_size=(2, 2)))
# model.add(keras.layers.Dropout(0.25))
# model.add(keras.layers.Conv2D(128, activation='relu',kernel_size=(2, 2)))
# model.add(keras.layers.MaxPool2D(pool_size=(2, 2)))
# model.add(keras.layers.Dropout(0.25))
# model.add(keras.layers.Conv2D(256, activation='relu',kernel_size=(2, 2)))
# model.add(keras.layers.MaxPool2D(pool_size=(2, 2)))
# model.add(keras.layers.Dropout(0.25))
# model.add(keras.layers.Conv2D(512, activation='relu',kernel_size=(2, 2)))
# model.add(keras.layers.MaxPool2D(pool_size=(2, 2)))
# model.add(keras.layers.Dropout(0.25))

# Flatten層把多維的輸入一維化，常用在從卷積層到全連接層的過渡。
# model.add(Flatten())
# 全連接層: 128個output
# model.add(Dense(5120, activation='relu')) 
# model.add(Dropout(0.25))
# model.add(Dense(1280, activation='relu'))
# model.add(Dense(1280, activation='relu'))
# model.add(Dense(640, activation='relu'))
# model.add(Dense(320, activation='relu'))
# model.add(Dense(160, activation='relu'))
# model.add(Dense(80, activation='relu'))
# model.add(Dense(40, activation='relu'))
# model.add(Dense(20, activation='relu'))
#model.add(Dense(10, activation='relu'))
# Add output layer
# model.add(Dense(5, activation='softmax'))
#印出模型結構
print(model.summary())
# 編譯: 選擇損失函數、優化方法及成效衡量方式
# model.compile(loss=keras.losses.categorical_crossentropy,
#               optimizer=keras.optimizers.Adadelta(),
#               metrics=['accuracy'])
model.compile(loss='categorical_crossentropy', 
              optimizer='adam', metrics=['accuracy'] ) #optimizer='rmsprop'
# BATCH_SIZE = 128
# EPOCHS = 50
# model.fit(train_images, train_labels, epochs=EPOCHS,batch_size=BATCH_SIZE, validation_data=(test_images, test_labels))
# 進行訓練, 訓練過程會存在 train_history 變數中
model.fit(X_train, y_train_hot, batch_size=64, epochs=300, verbose=1, validation_data=(X_test, y_test_hot))

X_train = X_train.reshape(X_train.shape[0], 20, 100)
X_test = X_test.reshape(X_test.shape[0], 20, 100)
score = model.evaluate(X_test, y_test_hot, verbose=1)

# 模型存檔
model.save('ASR.h5')