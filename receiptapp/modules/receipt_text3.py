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
import urllib
import numpy as np

def url_to_image(url):
	# download the image, convert it to a NumPy array, and then read
	# it into OpenCV format
	resp = urllib.request.urlopen(url)
	image = np.asarray(bytearray(resp.read()), dtype="uint8")
	image = cv2.imdecode(image, cv2.IMREAD_COLOR)

	# return the image
	return image

def cv2pil(image):
    ''' OpenCV型 -> PIL型 '''
    new_image = image.copy()
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB)
    elif new_image.shape[2] == 4:  # 透過
        new_image = cv2.cvtColor(new_image, cv2.COLOR_BGRA2RGBA)
    new_image = Image.fromarray(new_image)
    return new_image

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
    print(filename + '_gray.jpg')
    im_blur = cv2.fastNlMeansDenoising(im_gray) # 画像のノイズを取り除く
    # _, im_th = cv2.threshold(im_gray, 127, 255, cv2.THRESH_BINARY)
    im_th = cv2.adaptiveThreshold(im_blur, 255, \
                                      cv2.ADAPTIVE_THRESH_MEAN_C,\
                                      cv2.THRESH_BINARY, 63, 20)

    # 2値化処理まで終了
    th_filename = "{:s}_th.jpg".format(filename)
    print(th_filename)
    # cv2.imwrite(BASE_DIR + "/receiptapp/media/receiptapp/" + filename.split("/")[-1] + '_th.jpg', im_th)

    cnts, hierarchy = cv2.findContours(im_th, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # 輪郭の抽出
    # 輪郭画像、輪郭、階層情報の順に並んでいる。
    cnts.sort(key=cv2.contourArea, reverse=True)
    # 抽出された輪郭の面積が大きい順にソートをかける
    cnt = cnts[1]
    img = cv2.drawContours(im_th, [cnt], -1, (255,0,0), 3)
    im_line = cv2.cvtColor(im_th.copy(), cv2.COLOR_GRAY2BGR)
    #im_line_b = np.zeros(im_line.shape)
    warp = None
    flag = 1
    # 以下のループで抽出された輪郭を描画する
    for c in cnts[1:]:
		# 周囲長
        arclen = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02*arclen, True)
    # 輪郭を少ない点で表現（臨界点は0.02*arclen)
        if len(approx) == 4:
			# drqwContours(image, 輪郭情報, 2引数のどの輪郭を指定するのか、全輪郭を描画するなら-1, )
            cv2.drawContours(im_line, [approx], -1, (0, 0, 255), 10)
            #cv2.drawContours(im_line_b, [approx], -1, (0, 0, 255), 2)
            # cnts[1]が2番目に大きい輪郭 => つまりレシートの輪郭情報になるはず
            if flag: # 1番面積が大きいものがレシートの輪郭だと考えられるのでその輪郭情報を保存
                warp = approx.copy()
                flag = 0
        """
        else:
            print("else")
            #cv2.drawContours(im_line, [approx], -1, (0, 255, 0), 2)
            #cv2.drawContours(im_line_b, [approx], -1, (0, 255, 0), 2)
        for pos in approx:
            # circle(image, 円の中心座標, 半径, 色)
            cv2.circle(im_line, tuple(pos[0]), 4, (255, 0, 0))
            #cv2.circle(im_line_b, tuple(pos[0]), 4, (255, 0, 0))
        """
    # レシートと思われる輪郭の面積を算出。
    # 正しくレシートの輪郭を認識できないことがあるため、元の画像に対してある一定以上の大きさでないとトリミングをしないようにした。
    # cv2.imwrite(BASE_DIR + "/receiptapp/media/receiptapp/" + filename.split("/")[-1] + '_line.jpg', im_line)
    area = cv2.contourArea(warp)
    print("area = ", area)
    print("im_size =", im_size)
    if area > im_size//5:
        print("now cutting....")
        im_rect_th = transform_by4(im_th, warp[:, 0, :])
    else:
        return im_th
    # 切り取った画像の表示
    # plt.figure()
    # plt.imshow(im_line)
    #cv2.imwrite(BASE_DIR + "/receiptapp/media/receiptapp/" + filename.split("/")[-1] + '_line.jpg', im_line)
    #cv2.imwrite(BASE_DIR + "/receiptapp/media/receiptapp/" + filename.split("/")[-1] + '_line_b.jpg', im_line_b)
    print("warp = \n",warp[:, 0, :])
    print(filename + '_rect.jpg')
    return im_rect_th


def convert(filename = None, capture = False, CUT=False):
    print(filename)
    im = url_to_image(filename)
    if im is None:
        # 読み込みに失敗した場合は printする
        print('failed to load image.')
        print("use pyplot.imread")
        # im = plt.imread(BASE_DIR + "/receiptapp/media/receiptapp/" + filename)
        # cloudinary用のpath
        im = plt.imread(filename)
        im = im[..., ::-1] # RGB --> BGR
    filename = filename[:-4]
    # 拡張子を取り除いた形で記録する
    print("CUT")
    """
    im = cont_edge(im, filename)
    # print(im.shape)
    im_rect_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    print(filename+'_rect_gray.jpg')
    cv2.imwrite(BASE_DIR + "/receiptapp/media/receiptapp/" + filename.split("/")[-1] + 'rect_gray.jpg', im_rect_gray)
    im_rect_blur = cv2.fastNlMeansDenoising(im_rect_gray)
    cv2.imwrite(BASE_DIR + "/receiptapp/media/receiptapp/" + filename.split("/")[-1] + 'rect_blur.jpg', im_rect_blur)
    im_rect_th = cv2.adaptiveThreshold(im_rect_blur, 255, \
                                      cv2.ADAPTIVE_THRESH_MEAN_C,\
                                      cv2.THRESH_BINARY, 63, 20)
    """
    im_rect_th = cont_edge(im, filename)
    # cv2.imwrite(BASE_DIR + "/receiptapp/media/receiptapp/" + filename.split("/")[-1] + 'rect_th.jpg', im_rect_th)
    rect_th_filename = "{:s}_rect_th.jpg".format(filename)
    print(rect_th_filename)
    # os.system("tesseract '{:s}' output -l jpn".format(rect_th_filename))
    # img = cv2pil(im_rect_th)

    return im_rect_th

# convert("./r-sample1.jpg")

def img_to_text(filename):
    print(filename)
    im_rect_th = url_to_image(filename)
    img = cv2pil(im_rect_th)
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
    # print (text)
    # print(text)

    # rect_th のファイルを削除
    # os.remove(BASE_DIR + "/receiptapp/media/receiptapp/" + rect_th_filename)

    return text.replace("※", "").replace("＊", "").replace("*", "")


def convert_ajax(filename = None, capture = False, CUT=False, task_id="task_id"):
    print(filename)
    im = url_to_image(filename)
    if im is None:
        # 読み込みに失敗した場合は printする
        print('failed to load image.')
        print("use pyplot.imread")
        # im = plt.imread(BASE_DIR + "/receiptapp/media/receiptapp/" + filename)
        # cloudinary用のpath
        im = plt.imread(filename)
        im = im[..., ::-1] # RGB --> BGR
    filename = filename[:-4]
    # 拡張子を取り除いた形で記録する
    print("CUT")

    # 2
    progress_update(task_id=task_id, progress_no=2)

    im_rect_th = cont_edge(im, filename)
    # cv2.imwrite(BASE_DIR + "/receiptapp/media/receiptapp/" + filename.split("/")[-1] + 'rect_th.jpg', im_rect_th)

    # 3
    progress_update(task_id=task_id, progress_no=3)

    img = cv2pil(im_rect_th)
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

    # 4
    progress_update(task_id=task_id, progress_no=4)

    return text.replace("※", "").replace("＊", "").replace("*", "")

import sys
sys.path.append('../../')

from receiptapp.models import Progress

def progress_update(task_id, progress_no):
    progress = Progress.objects.get(task_id=task_id)
    progress.progress_no = progress_no
    progress.save()
