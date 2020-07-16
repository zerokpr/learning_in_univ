# 画像の輪郭を強調し、強調された画像を保存するプログラム
import cv2
import numpy as np
import os

wait_time = 0

# ソーベルフィルタ
def sobelfiltering(img, filter_size):
    dx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=filter_size)
    # display(dx.astype(np.uint8), 'dx')
    dy = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=filter_size)
    # display(dy.astype(np.uint8), 'dy')
    img = np.sqrt(dx ** 2 + dy ** 2).astype(np.uint8)
    return img

# 描画
# qキーで終了
def display(img, windowname):
    cv2.imshow(windowname, img)
    key = cv2.waitKey(wait_time)
    while True:
        if key == ord('q'):
            cv2.destroyAllWindows()
            return

# 入力処理
current_dir = os.getcwd()
img_name = input('Enter name of input image: ')
img_path = current_dir + '\\' + img_name
print(img_path)

img_BGR = cv2.imread(img_name, 1)
if img_BGR is None: # エラー処理
    print(img_path + ' was not found.') 
    exit()
#display(img_BGR, 'BGR')

img_HSV = cv2.cvtColor(img_BGR, cv2.COLOR_BGR2HSV)
#display(img_HSV, 'HSV')

img_MONO = img_HSV[:,:,2]
#display(img_MONO, 'MONO')

filter_size = input('\nEnter size of sobel filter: ')
img_SOBEL = sobelfiltering(img_MONO, int(filter_size))
#display(img_SOBEL, 'Sobelfiltered')

k=0.5
img_SOBEL = cv2.cvtColor(img_SOBEL, cv2.COLOR_GRAY2BGR)
img_Sharpness = cv2.addWeighted(img_HSV,1,img_SOBEL,k,0)
img_Sharpness = cv2.cvtColor(img_Sharpness, cv2.COLOR_HSV2BGR)
img_Sharpness = img_Sharpness.clip(0,255)
print(img_Sharpness.max())
display(img_Sharpness, 'Sharpness')

# 強調した画像を保存
save_name = input('\nEnter save name: ')
cv2.imwrite(save_name, img_Sharpness)
