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
    # receipts_analyse部分
    image_id = request.session['image_id']
    image = Image.objects.get(pk=image_id).image.url
    filename = image
    print(filename)
    img = receipt_text3.convert(filename, CUT=True)

    return search_list
