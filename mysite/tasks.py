from __future__ import absolute_import, unicode_literals
from celery import shared_task
import time

@shared_task
def add(x, y):
    print("処理中")
    z = x + y
    print("0秒")
    time.sleep(10)
    print("10秒")
    time.sleep(10)
    print("20秒")
    time.sleep(10)
    print("30秒")
    time.sleep(10)
    print("40秒")
    print("処理完了")
    return z

@shared_task
def get_search_list(image_id):
    search_list = []
    image = Image.objects.get(pk=image_id).image.url
    filename = image
    print(filename)
    text = receipt_text3.convert2(filename, CUT=True)

    search_list = receipt_tyuusyutu2.analyse(filename=filename, isWord=False, word="", text=text)[0]

    public_id = filename.split("/")[-1].replace(".jpg", "").replace(".png", "")
    cloudinary.uploader.destroy(public_id = public_id)
    cloudinary.uploader.destroy(public_id = public_id.replace("_rect_th", ""))

    name_list = []

    for i1, info_list in enumerate(search_list):
        name_list.append([])
        # info_list[0] => [info, info, info]
        for info in info_list[0]:
            # info => [v, v, v, v]
            for i2, v in enumerate(info):
                info[i2] = str(v)
            name_list[i1].append(info[0])
    user = request.user
    context = {"user": user, "search_list": search_list, "count": len(search_list)}

    return [search_list, count]
