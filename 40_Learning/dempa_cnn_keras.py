import numpy as np
from keras.models import Sequential
# from keras.layers import Convolution2D, MaxPooling2D
from keras.layers import Convolution1D, MaxPooling1D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.utils import np_utils

# 分類対象のカテゴリ
root_dir = "./image/"
categories = ["moga", "ayane", "nemu"]
nb_classes = len(categories)
image_size = 128

def main():
    # データをロード
    X_train, X_test, y_train, y_test = np.load("./dempa.npy")
    print(X_train.shape)

    # データを正規化
    X_train = X_train.astype("float") / 256
    X_test  = X_test.astype("float") / 256
    y_train = np_utils.to_categorical(y_train, nb_classes)
    y_test  = np_utils.to_categorical(y_test, nb_classes)

    # モデルを訓練し評価する
    model = model_train(X_train, y_train)
    model_eval(model, X_test, y_test)


# モデルを構築
def build_model(in_shape):
    model = Sequential()

    # model.add(Convolution2D(32, 3, 3, border_mode='same', input_shape=(in_shape[0], in_shape[1], 1)))
    model.add(Convolution1D(32, 3, border_mode='same', input_shape=in_shape))
    model.add(Activation('relu'))
    # model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(MaxPooling1D(pool_length=2))
    model.add(Dropout(0.25))

    # model.add(Convolution2D(64, 3, 3, border_mode='same'))
    model.add(Convolution1D(64, 3, border_mode='same'))
    model.add(Activation('relu'))
    # model.add(Convolution2D(64, 3, 3))
    # model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Convolution1D(64, 3))
    model.add(MaxPooling1D(pool_length=2))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(nb_classes))
    model.add(Activation('softmax'))

    model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

    return model


# モデルを訓練
def model_train(X, y):
    model = build_model(X.shape[1:])
    model.fit(X, y, batch_size=32, nb_epoch=30)

    # モデルを保存
    hdf5_file = "./dempa-model.hdf5"
    model.save_weights(hdf5_file)
    return model


# モデルを評価
def model_eval(model, X, y):
    score = model.evaluate(X, y)
    print('\nloss=', score[0])
    print('accuracy=', score[1])


if __name__ == "__main__":
    main()
