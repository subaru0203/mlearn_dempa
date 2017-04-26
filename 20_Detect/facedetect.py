import cv2
import math
import numpy
import sys
import os

# カスケードファイルのパスを指定
cascade_file_face   = "haarcascade_frontalface_alt2.xml"
cascade_file_eye    = "haarcascade_eye.xml"

# 顔認識用特徴点ファイルを読み込む
cascade_face    = cv2.CascadeClassifier(cascade_file_face)
cascade_eye     = cv2.CascadeClassifier(cascade_file_eye)

def detect_face(img_file):
    # 画像の読み込み
    image = cv2.imread(img_file)
    rows, cols, colors = image.shape

    # グレースケールに変換
    image_gs = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 元画像の斜辺サイズの枠を作る
    hypot = int(math.hypot(rows, cols))
    frame = numpy.zeros((hypot, hypot), numpy.uint8)
    frame[int((hypot - rows) * 0.5):int((hypot + rows) * 0.5), int((hypot - cols) * 0.5):int((hypot + cols) * 0.5)] = image_gs

    # 各loopで違う角度の回転行列をかけた結果のものに対して検出を試み
    results = []
    for deg in range(-30, 31, 5):
        M = cv2.getRotationMatrix2D((hypot * 0.5, hypot * 0.5), -deg, 1.0)
        rotated = cv2.warpAffine(frame, M, (hypot, hypot))
        faces = cascade_face.detectMultiScale(rotated, scaleFactor=1.11, minNeighbors=3, minSize=(64, 64))
        # print(deg, len(faces))
        for i, (x, y, w, h) in enumerate(faces):
            face_cand = rotated[y:y + h, x:x + w]
            # cv2.imwrite("face_" + str(deg) + "_" + str(i) + ".jpg", face_cand)

            # 目検出
            eyes = cascade_eye.detectMultiScale(face_cand, scaleFactor=1.11, minNeighbors=3)
            if len(eyes) >= 2:
                result = {
                    'img': face_cand,
                    'deg': deg,
                }
                results.append(result)
                # print(deg, len(eyes))
                break

    return results

if __name__ == "__main__":
    param = sys.argv
    detect_face(param[1], '.', param[2])