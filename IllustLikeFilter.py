# 入力画像にイラストのような処理をかけるプログラム

import cv2
import numpy as np
import os

# cv2ウィンドウが開かれているかをチェックする
BackendError = type('BackendError', (Exception,), {})
def isVisible(winname):
    try:
        ret = cv2.getWindowProperty(
            winname, cv2.WND_PROP_VISIBLE
            )

        if ret == -1:
            raise BackendError('Use Qt as backend to check whether window is visible or not.')

        return bool(ret)

    except cv2.error:
        return False

# 描画
# qキーで終了
# closeキーを押しても終了する
def display(img, windowname = '.'):
    cv2.imshow(windowname, img)
    key = cv2.waitKey(0)
    while True:
        if key == ord('q'):
            cv2.destroyAllWindows()
            return
        
        if not isVisible(windowname):
            return

# 画像の輪郭線を抽出する
# 引数:BGRの画像
# 戻り値:BGR形式の画像
def stressEdge(bgr_src):
    gray_src = cv2.cvtColor(bgr_src, cv2.COLOR_BGR2GRAY)
    blur_src = cv2.GaussianBlur(gray_src, (5,5), 2)
    ret = cv2.adaptiveThreshold(blur_src, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 5, 2)
    ret = cv2.cvtColor(ret, cv2.COLOR_GRAY2BGR)
    return ret

# 減色処理をする
# 引数img:bgr画像, k:減色後の色数
# 戻り値:bgr画像
def subImgColor(img, k):
    z = img.reshape((-1,3))
    z = np.float32(z)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
    ret, label, center = cv2.kmeans(z, k, None, criteria, 32, cv2.KMEANS_RANDOM_CENTERS)

    center = np.uint8(center)
    ret = center[label.flatten()]

    return ret.reshape((img.shape))


def main():
    # 入力処理
    current_dir = os.getcwd()
    img_name = input("Enter name of input name: ")
    img_path = current_dir + "\\" + img_name
    img = cv2.imread(img_name, 1)

    # 画像処理
    edge_line = stressEdge(img)
    decleased_color_img = subImgColor(img, 32)
    img = cv2.addWeighted(edge_line, 0.3, decleased_color_img, 1.0, 0)

    # 処理した画像を表示
    display(img, "processed img")

    # 処理した画像を保存
    shouldSave = input("Do you wanna save? (Yes / Other)")
    if shouldSave == "Yes":
        save_name = input("Write image's name: ")
        cv2.imwrite(save_name, img)
    
    print("Good bye!")

    return 0

if __name__ == "__main__":
    main()
