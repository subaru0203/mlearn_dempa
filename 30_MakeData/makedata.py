import numpy as np
import glob
from PIL import Image
from sklearn import cross_validation

# 分類対象のカテゴリーを選ぶ
root_dir = "./image"
categories = ["moga", "ayane", "nemu"]
nb_classes = len(categories)
image_size = 128

# フォルダごとの画像データを読み込む
X = [] # 画像データ
Y = [] # ラベルデータ

for idx, cat in enumerate(categories):
    image_dir = root_dir + "/" + cat
    files = glob.glob(image_dir + "/*.jpg")
    print("---", cat, "を処理中")
    for i, f in enumerate(files):
        # print(i, f)
        img = Image.open(f)
        # img = img.resize((image_size, image_size))
        img.thumbnail((image_size, image_size), Image.ANTIALIAS)
        # list, tupleなどを引数にndarray生成
        # PILのImageオブジェクトを配列に変換する
        data = np.asarray(img)

        if data.shape == (image_size, image_size):
            X.append(data)
            Y.append(idx)
        else:
            print("NG", data.shape)

X = np.array(X)
Y = np.array(Y)

# 学習データとテストデータを分ける
X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, Y)
xy = (X_train, X_test, y_train, y_test)
np.save("./image/dempa.npy", xy)
print("ok,", len(Y))
