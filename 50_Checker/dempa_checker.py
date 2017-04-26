import dempa_cnn_keras as dempa
import facedetect
import cv2
import sys, os
import numpy as np
import webbrowser

# コマンドラインからファイル名取得
if len(sys.argv) != 2:
    print("dempa_checker.py (ファイル名)")
    quit()

image_size = 128
categories = ["最上もが", "藤咲彩音", "夢眠ねむ"]

# 入力画像から顔検出を行う
param = sys.argv
face_results = facedetect.detect_face(param[1])
#print(len(face_results))

if len(face_results) == 0:
    print("顔検出失敗")
    quit()

# 顔画像をリサイズしてnumpy形式に変換
X = []
for result in face_results:
    # in_data = np.copy(result['img'])
    in_data = cv2.resize(result['img'], (image_size, image_size))
    # print(str(result['deg']))
    # cv2.imwrite("face_"+str(result['deg'])+".jpg", in_data)
    X.append(in_data)
X = np.array(X)

# CNNモデルを構成
model = dempa.build_model(X.shape[1:])
model.load_weights("./dempa-model.hdf5")

# 検出した顔画像をデータ予測を行う
p_result = []
pre = model.predict(X)
for i, p in enumerate(pre):
    print(i, ":", p)
    p_result.append(p)

p_result = np.array(p_result)
p_result = p_result.sum(axis=0)
# print(p_result)
idx = p_result.argmax()

# レポート作成
html = ""
html += """
    <h3>入力:{0}</h3>
    <div>
        <p><img src="{1}" width=300></p>
        <p>メンバー名:{2}</p>
    </div>
""".format(os.path.basename(param[1]), param[1], categories[idx])

# レポート保存
html = """
    <!DOCTYPE html>
    <html lang="ja">
    <meta charset="utf-8">
    <body style='text-align:center;'>
    <style> p {{ margin:0; padding:0; }} </style>
        {0}
    </body>
    </html>
""".format(html)

with open("dempa-result.html", "w") as f:
    f.write(html)

# レポートを開く
report = os.path.abspath("./dempa-result.html")
report = "file:///" + report
webbrowser.open(report)
