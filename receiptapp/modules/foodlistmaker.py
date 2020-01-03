import pandas as pd
import re
import jaconv

data = pd.read_excel("data/syokuzai.xlsx", skiprows=[0, 1, 2, 3, 4, 5, 6, 7, 8])
# エクセルファイルのいらないところはとばす
a = data.iloc[:, 3]

#　記号を取り除き、ひらがなとカタカナに変換した食材を入れる
syokuzai_list = set()
for i in range(len(a)):
    tmp = re.sub(r'[＜＞\［\］\（\）]',' ', a[i])
    tmp = tmp.split()
    for j in range(len(tmp)):
        tmp1 = jaconv.hira2kata(tmp[j])
        tmp2 = jaconv.kata2hira(tmp[j])
        syokuzai_list.add(tmp1)
        syokuzai_list.add(tmp2)

f = open('data/food_list.txt', 'w') # food_list.txtというファイル名で保存
for x in syokuzai_list:
    f.write(str(x) + "\n")
f.close()
