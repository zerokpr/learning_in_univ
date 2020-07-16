# カメラから入力される映像で、顔の部分にモザイクをかけるプログラム
import numpy as np
import cv2

# srcで指定した画像にモザイクをかける
# 戻り値：モザイクを掛けた画像
def mosaic(src, ratio=0.05):
    small = cv2.resize(src, None, fx=ratio, fy=ratio, interpolation=cv2.INTER_NEAREST)
    return cv2.resize(small, src.shape[:2][::-1], interpolation=cv2.INTER_NEAREST)

# srcで(x,y,width,height)の範囲にモザイクをかける
# 戻り値：一部にモザイクをかけた画像
def mosaic_area(src, x, y, width, height, ratio=0.05):
    dst = src.copy()
    dst[y:y + height, x:x + width] = mosaic(dst[y:y + height, x:x + width], ratio)
    return dst

cap = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

while True:
    ret, frame = cap.read()
    if ret == False:
        break
    print(ret)

    img_GRAY = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(img_GRAY, 1.3, 5)

    if 0 < len(faces):
        for (x,y,w,h) in faces:
            frame = mosaic_area(frame, x, y, w, h)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255))  

    cv2.imshow("test", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.waitKey(0)
cv2.destroyAllWindows()
