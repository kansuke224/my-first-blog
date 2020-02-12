
import numpy as np
import os
import cv2
from . import receipt_text
import matplotlib.pyplot as plt
import pandas as pd
import re
import sys
from mysite.settings import BASE_DIR
# sys.argv  コマンドライン引数を受け取れる
# python receipt_tyuusyutu.py の場合indexは0まで
# pic_name = sys.argv[1]



def word_search(filename, text):
    # 本番用です
    # convertから渡されたtextをしよう
    # data2 = receipt_text.convert(filename, CUT=True)
    data2 = text
    # レシートデータから文字データを抽出する。出力ファイルは`output.txt`

    # あらかじめ作っておいたfood_list.txtを呼び出す。
    f = open(BASE_DIR + '/receiptapp/data/food_list.txt', encoding='cp932')
    data1 = f.read()
    f.close()
    lines = data1.split('\n')
    # print(data1)
    # output.txt からテキストをもってくるぱたーんの時の処理
    # filename = "output.txt"
    # f = open(filename, encoding="utf8")
    # data2 = f.read()

    receipt_data = data2.split()
    print("read data txt is \n ",receipt_data)
    # レシートから読み込んだ文字列を、空白文字で区切ったlistを表示
    search_words = []

    # 食材リストと照らし合わせてリストに照合するものがレシートのデータに存在すれば
    # その食材をsearch_wordsに加える

    for word in lines:
        for receipt in receipt_data:
            if len(receipt) <= 1:
                continue
            # receipt.replace("※", "")
            if word in receipt:
                if len(word) <= 1:
                    continue
                search_words.append(word)
                print("True")
                continue
            if len(receipt) >= 3 and receipt in word:
                print("BTrue")
                search_words.append(word)

    return search_words


def analyse(filename, isWord, word, text):

    if isWord:
        search_words = []
        search_words.append(word)
    else:
        search_words = word_search(filename, text)

    # テスト用
    # search_words = ["うどん", "ラー油", "もも"]


    print(search_words)
    # search_words を使って xlsxのデータから栄養情報を取り出す
    search_info = []
    # 3 食品名 D
    # 5 エネルギー(kcal) F
    # 10 脂質 K
    # 16 炭水化物 Q
    # 8 タンパク質 I
    # 28 亜鉛
    # 56 食塩相当量 BE
    data = pd.read_excel(BASE_DIR + "/receiptapp/data/syokuzai2.xlsx",
    skiprows=[0, 1, 2, 3, 4, 5, 6, 7, 126], header=None, index_col=None, usecols=[3, 5, 8, 10, 16, 56])
    for word in search_words:
        # print(data[data["食品名"].str.contains(word, na=False)])
        search_info.append(data[data[3].str.contains(word, na=False)])

    search_list = []
    for df in search_info:
        search_list.append([df.values.tolist(),len(df)])

    len_list = []
    for df in search_info:
        len_list.append(len(df))

    # print(search_words)
    # print(search_info)
    # search_words.sort(key=len, reverse=True)
    # search_info.sort(key=len, reverse=True)
    # search_words = search_words[:3]
    # print("search_words is ....", search_words, "\n")
    # print("search_info is ....", search_info, "\n")
    return [search_list, len_list]
