# Tensorflow 2.0
# CNN (합성곱 신경망)
# mnist data 분류하기
# reference : https://www.tensorflow.org/tutorials/images/cnn?hl=ko

import tensorflow as tf
from tensorflow.keras import datasets, layers, models

# mnist 데이터 로드
## x_train : (60000,28,28),  y_train : (60000,)
## x_test : (10000,28,28),   y_test : (10000,)
(x_train, y_train), (x_test, y_test) = datasets.mnist.load_data()

# CNN은 (이미지 높이, 이미지 너비, 컬러 채널) 크기의 텐서를 입력으로 받기 때문에 데이터 형태를 바꿔준다.
# ((batch size, 이미지 높이, 이미지 너비, 컬러채널))
x_train = x_train.reshape((60000, 28, 28, 1))
x_test = x_test.reshape((10000, 28, 28, 1))

# RGB 채널 값은 [0,255] 범위에 있음. 신경망에 이상적이지 않음, 입력값을 작게 만들어야 함
# 따라서 [0,1]로 Normalization
x_train, x_test = x_train / 255.0, x_test / 255.0

# 합성곱 층 정의
## Sequential()
## 하나의 입력 텐서와 하나의 출력 텐서가 있는 일반 레이어 스택
## 다중 입력, 다중 출력이 있는 경우, 레이어를 공유해야하는 경우, 비선형 토폴로지 쓰는 경우 부적합
model = models.Sequential()
## Conv2D(filters, kernel_size, ...)
## data shape (28,28,1) > (26,26,32)
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)))
## data shape (26,26,32) > (13,13,32)
model.add(layers.MaxPooling2D((2, 2)))
## data shape (13,13,32) > (11,11,64) * input channel 수와 관계 없이 filter 수 만큼 output channel
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
## data shape (11,11,64) > (5,5,64)
model.add(layers.MaxPooling2D((2, 2)))
## data shape (5,5,64) > (3,3,64)
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
# flatten : 3D 출력을 1D로 펼치는 layer
# data shape (64,3,3) = (576)
model.add(layers.Flatten())
# Dense(units) : output space의 차원
# data shape (576) > (64)
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(10, activation='softmax'))

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.fit(x_train, y_train, epochs=5)

test_loss, test_acc = model.evaluate(x_test, y_test, verbose=2)
