import numpy as np
import os
import glob
import matplotlib.pyplot as plt
import cv2
# from .. import mysite.settings.BASE_DIR
# from ..mysite.settings import BASE_DIR
import pyocr
from PIL import Image
import re
import sys
import pathlib
# base.pyのあるディレクトリの絶対パスを取得
current_dir = pathlib.Path(__file__).resolve().parent
# モジュールのあるパスを追加
sys.path.append( str(current_dir) + '/../' )
from mysite.settings import BASE_DIR

def imread(filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8):
    try:
        n = np.fromfile(filename, dtype)
        img = cv2.imdecode(n, flags)
        return img
    except Exception as e:
        print(e)
        return None

def imwrite(filename, img, params=None):
    try:
        ext = os.path.splitext(filename)[1]
        result, n = cv2.imencode(ext, img, params)

        if result:
            with open(filename, mode='w+b') as f:
                n.tofile(f)
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False


def transform_by4(img, points):
  """
  4点を指定してトリミングする。
  source:http://blanktar.jp/blog/2015/07/python-opencv-crop-box.html
  """

  points = points[np.argsort(points, axis = 0)[:,1]]
# yが小さいもの順に並び替え。
  top = points[np.argsort(points[:2],axis = 0)[:, 0]]
# 前半二つは四角形の上。xで並び替えると左右も分かる。
  bottom = points[2:][np.argsort(points[2:],axis=0)[:,0]]
# 後半二つは四角形の下。同じくxで並び替え。
  points = np.vstack((top, bottom) )
# 分離した二つを再結合。

  width = (np.abs(points[0][0]-points[1][0])+\
                np.abs(points[2][0]-points[3][0]))/2.0
  height = (np.abs(points[0][1]-points[2][1])+\
                np.abs(points[1][1]-points[3][1]))/2.0
  width = int(width)
  height = int(height)
  points2 = np.float32([[0,0],[width, 0],[0,height],[width,height]])
  points1 = np.float32(points)
  M = cv2.getPerspectiveTransform(points1,points2)
# 変換前の座標と変換後の座標の対応を渡すと、透視変換行列を作ってくれる。
  return cv2.warpPerspective(img,M,(width, height)) # 透視変換行列を使って切り抜く。
# matplotlibで正常に画像が表示できるための関数。（モノクロ画像に対して）
def show_img(img):
    plt.figure()
    tmp = np.tile(img.reshape(img.shape[0],img.shape[1], -1),\
                  reps=3)
    plt.imshow(tmp)
    plt.show()

def cont_edge(im, filename):
    im_size = im.shape[0] * im.shape[1]
    im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    # cv2.imwrite(BASE_DIR + "/receiptapp/media/receiptapp/" + filename + '_gray.jpg', im_gray)
    print(filename + '_gray.jpg')
    im_blur = cv2.fastNlMeansDenoising(im_gray) # 画像のノイズを取り除く
    _, im_th = cv2.threshold(im_blur, 127, 255, cv2.THRESH_BINARY)
    # 以下のコマンドで2値化をする
    #im_th = cv2.adaptiveThreshold(im_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, 5)
    # im_th = cv2.Canny(im_blur, 50, 200)
    th_filename = "{:s}_th.jpg".format(filename)
    # 2値化させた画像を表示させる。
    # show_img(im_th)
    print(th_filename)
    # 画像の保存
    # cv2.imwrite(BASE_DIR + "/receiptapp/media/receiptapp/" + th_filename, im_th)
    print(filename + '_th.jpg')

    cnts, hierarchy = cv2.findContours(im_th, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # 輪郭の抽出
    # 輪郭画像、輪郭、階層情報の順に並んでいる。
    cnts.sort(key=cv2.contourArea, reverse=True)
    # 抽出された輪郭の面積が大きい順にソートをかける
    cnt = cnts[1]
    img = cv2.drawContours(im_th, [cnt], -1, (0,255,0), 3)
    # cv2.imwrite(BASE_DIR + "/receiptapp/media/receiptapp/" + filename+"_drawcont.jpg", img)
    im_line = im.copy()
    warp = None
    flag = 1
    # 以下のループで抽出された輪郭を描画する
    for c in cnts[1:]:
        arclen = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02*arclen, True)
    # 輪郭を少ない点で表現（臨界点は0.02*arclen)
        if len(approx) == 4:
            cv2.drawContours(im_line, [approx], -1, (0, 0, 255), 2)
            if flag: # 1番面積が大きいものがレシートの輪郭だと考えられるのでその輪郭情報を保存
                warp = approx.copy()
                flag = 0
        else:
            cv2.drawContours(im_line, [approx], -1, (0, 255, 0), 2)
        for pos in approx:
            cv2.circle(im_line, tuple(pos[0]), 4, (255, 0, 0))
    # レシートと思われる輪郭の面積を算出。
    # 正しくレシートの輪郭を認識できないことがあるため、元の画像に対してある一定以上の大きさでないとトリミングをしないようにした。
    area = cv2.contourArea(warp)
    print("area = ", area)
    if area > im_size//5:
        print("now cutting....")
        im_rect = transform_by4(im, warp[:, 0, :])
        # cv2.imwrite(BASE_DIR + "/receiptapp/media/receiptapp/" + filename + '_rect.jpg', im_rect)
    else:
        return im
    # 切り取った画像の表示
    plt.figure()
    plt.imshow(im_line)
    # cv2.imwrite(BASE_DIR + "/receiptapp/media/receiptapp/" + filename + '_line.jpg', im_line)
    print("warp = \n",warp[:, 0, :])
    print(filename + '_rect.jp')
    return im_rect


def convert(filename = None, capture = False, CUT=False):
    if filename == None and capture == False:
        pass
    elif capture == True:
        # Webカメラで読み込むこともやりたかったがUbuntuがうまく認識してくれず、断念。
        cap = cv2.VideoCapture(0)
    elif filename:
        im = cv2.imread(BASE_DIR + "/receiptapp/media/receiptapp/" + filename)
    if im is None:
        # 読み込みに失敗した場合は printする が返るようにする
        print('failed to load image.')
        print("use pyplot.imread")
        im = plt.imread(BASE_DIR + "/receiptapp/media/receiptapp/" + filename)
        im = im[..., ::-1] # RGB --> BGR
    print(filename)
    filename = filename[:-4]
    print(im)
    print(filename)
    # 拡張子を取り除いた形で記録する
    if CUT:
        im = cont_edge(im, filename)
    # print(im.shape)
    im_rect_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    print(filename+'_rect_gray.jpg')
    im_rect_blur = cv2.fastNlMeansDenoising(im_rect_gray)
    im_rect_th = cv2.adaptiveThreshold(im_rect_blur, 255, \
                                      cv2.ADAPTIVE_THRESH_MEAN_C,\
                                      cv2.THRESH_BINARY, 63, 20)

    rect_th_filename = "{:s}_rect_th.jpg".format(filename)
    imwrite(BASE_DIR + "/receiptapp/media/receiptapp/" + rect_th_filename, im_rect_th)
    print(rect_th_filename)
    # show_img(im_rect_th)
# 既存のoutput.txtファイルが存在すればそれを消去して新たにoutput.txtを作成
# 文字認識についてはGoogleのAPIを利用させてもらった。
    if glob.glob('output.txt'):
        os.remove('output.txt')
    # 以下のコメントを外せばtesseractでの実行もできる。
    # tesseractのインストールは
    # rect_th_filename = "{:s}_rect_th.jpg".format(filename)
    # os.system("tesseract {:s} output -l jpn".format(rect_th_filename))
    os.system("tesseract {:s} output -l jpn".format(rect_th_filename))
    # text = open("output.txt").read().replace('ー', '1').replace('\\', '¥')
    img = Image.open(BASE_DIR + "/receiptapp/media/receiptapp/" + rect_th_filename)
    tools = pyocr.get_available_tools()
    if len(tools) == 0:
        print("No OCR tool found")
        sys.exit(1)

    tool = tools[0]
    text = tool.image_to_string(
            img,
            lang="jpn",
            builder=pyocr.builders.TextBuilder(tesseract_layout=6)
    )
    text = re.sub('([あ-んア-ン一-龥ー])[ 　]((?=[あ-んア-ン一-龥ー]))',r'\1\2', text)
    print (text)
    # print(text)

    # rect_th のファイルを削除
    os.remove(BASE_DIR + "/receiptapp/media/receiptapp/" + rect_th_filename)

    return text

# convert("./r-sample1.jpg")
