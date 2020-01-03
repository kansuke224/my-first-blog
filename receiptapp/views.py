from django.shortcuts import render, redirect
from .modules import receipt_tyuusyutu
from .modules import create_food
from .forms import ImageForm
from .models import Receipt, Image, Food, Fooddetail
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

import datetime
from dateutil.relativedelta import relativedelta

import environ
import cloudinary

env = environ.Env()
env.read_env('.env')

cloudinary.config(
  cloud_name = env('CLOUD_NAME'),
  api_key = env('API_KEY'),
  api_secret = env('API_SECRET')
)


# Create your views here.
@login_required
def index(request):
    # del request.session["image_id"]
    if "image_id" in request.session:
        # Image のdbを消す処理
        image_id = request.session["image_id"]
        image = Image.objects.get(pk=image_id)
        # image.delete()
        del request.session["image_id"]
    isMsg = False
    msg = "00"
    if "msg" in request.session:
        isMsg = True
        msg = request.session["msg"]
        del request.session["msg"]

    # months = Receipt.objects.dates("receipt_date", "month", order="DESC")
    months = [
    datetime.date(2019, 1, 1),
    datetime.date(2019, 2, 1),
    datetime.date(2019, 3, 1),
    datetime.date(2019, 4, 1),
    datetime.date(2019, 5, 1),
    datetime.date(2019, 6, 1),
    datetime.date(2019, 7, 1),
    datetime.date(2019, 8, 1),
    datetime.date(2019, 9, 1),
    datetime.date(2019, 10, 1),
    datetime.date(2019, 11, 1),
    datetime.date(2019, 12, 1),
    datetime.date(2020, 1, 1),
    datetime.date(2020, 2, 1),
    datetime.date(2020, 3, 1),
    datetime.date(2020, 4, 1),
    datetime.date(2020, 5, 1),
    datetime.date(2020, 6, 1),
    datetime.date(2020, 7, 1),
    datetime.date(2020, 8, 1),
    datetime.date(2020, 9, 1),
    datetime.date(2020, 10, 1),
    datetime.date(2020, 11, 1),
    datetime.date(2020, 12, 1)
    ]

    month_list = []
    user = request.user

    for month in months:
        dates = Receipt.objects.filter(user = user, receipt_date__year = month.year, receipt_date__month = month.month).dates("receipt_date", "day", order="DESC")
        # date_list => [date(日付), [レシート(日付別),[detail_list]]]
        date_list = []
        for date in dates:
            receipts = Receipt.objects.filter(
                                                    user = user,
                                                    receipt_date__year = date.year,
                                                    receipt_date__month = date.month,
                                                    receipt_date__day = date.day
                                                )
            receipt_list = []
            for receipt in receipts:
                foods_list = []
                details = receipt.fooddetail_set.all()
                for detail in details:
                    foods_list.append(detail.food)
                receipt_list.append([receipt, details])
            date_list.append([date, receipt_list])
        month_list.append([month.year, month.month, date_list])

    year_list = [2019, 2020]
    context = {"user": user, "month_list": month_list,"receipts": receipts, "year_list":year_list, "msg": msg, "isMsg": isMsg}
    return render(request, "receiptapp/index.html", context)

def receipts_new(request):
    form = ImageForm()
    user = request.user
    context = {"user": user, 'form': form}
    return render(request, "receiptapp/receipts_new.html", context)

def receipts_food_select(request):
    image_id = request.session['image_id']
    image = Image.objects.get(pk=image_id).image.url
    print("replace")
    filename = image.replace("/media/receiptapp/", "")
    print(filename)
    search_list = receipt_tyuusyutu.analyse(filename=filename, isWord=False, word="")[0]
    public_id = filename.split("/")[-1].replace(".jpg", "").replace(".png", "")
    cloudinary.uploader.destroy(public_id = public_id)

    for info_list in search_list:
        for info in info_list[0]:
            for i, v in enumerate(info):
                info[i] = str(v)
    user = request.user
    context = {"user": user, "search_list": search_list}
    return render(request, "receiptapp/receipts_food_select.html", context)

def receipts_detail(request, receiptId):
    receipt = Receipt.objects.get(id=receiptId)
    foods_detail = receipt.fooddetail_set.all()
    user = request.user
    fd_arr = []
    for food_detail in foods_detail:
        fd_arr.append([food_detail.food, food_detail])
    food_list = []
    for fd in fd_arr:
        amount_num = fd[1].amount // 100
        seibun = [
                round(amount_num * fd[0].salt, 1),
                round(amount_num * fd[0].protein, 1),
                round(amount_num * fd[0].energy, 1),
                round(amount_num * fd[0].carb, 1),
                round(amount_num * fd[0].fat, 1)
                ]
        detail_list = [fd[0], fd[1], seibun]
        food_list.append(detail_list)
        # print(amount_num)
    context = {"user": user, "receipt": receipt, "food_list": food_list}
    print(fd_arr)
    return render(request, "receiptapp/receipts_detail.html", context)

def receipts_delcheck(request, receiptId):
    receipt = Receipt.objects.get(id=receiptId)
    foods = []
    for detail in receipt.fooddetail_set.all():
        foods.append(detail.food)
    user = request.user
    context = {"user": user, "receipt": receipt, "foods": foods}
    return render(request, "receiptapp/receipts_delcheck.html", context)

def foods_edit(request, receiptId, foodId, detailId):
    food = Food.objects.get(id = foodId)
    detail = Fooddetail.objects.get(id = detailId)
    context = {"food_name": food.food_name, "amount": detail.amount, "receiptId": receiptId, "foodId": foodId, "detailId": detailId}
    return render(request, "receiptapp/foods_edit.html", context)

def foods_edit_select(request, receiptId, foodId, detailId):
    # request の postからsearch_word と amountのデータを取得
    food_name = request.POST.get("food_name")
    amount = int(request.POST.get("amount")) * 100
    search_list = receipt_tyuusyutu.analyse(filename="", isWord=True, word=food_name)[0]
    context = {"search_list": search_list, "amount": amount, "amount_num": request.POST.get("amount"), "receiptId": receiptId, "foodId": foodId, "detailId": detailId}
    return render(request, "receiptapp/foods_edit_select.html", context)

def foods_new(request, receiptId):
    context = {"receiptId" :receiptId,}
    return render(request, "receiptapp/foods_new.html", context)

def foods_new_select(request, receiptId):
    # request の postからsearch_word と amountのデータを取得
    food_name = request.POST.get("food_name")
    amount = int(request.POST.get("amount")) * 100
    search_list = receipt_tyuusyutu.analyse(filename="", isWord=True, word=food_name)[0]
    context = {"search_list": search_list, "amount": amount, "amount_num": request.POST.get("amount"), "receiptId" :receiptId}
    return render(request, "receiptapp/foods_new_select.html", context)

def graph(request):
    # 必要な情報
    JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
    UCT = datetime.timezone(datetime.timedelta(hours=+0), 'UCT')
    user = request.user
    today = datetime.datetime.now(JST)
    print(today)
    one_week_ago = today - datetime.timedelta(days=6)
    one_month_ago = today - relativedelta(months=1)

    receipts = Receipt.objects.filter(
                                        user = user,
                                        receipt_date__range = (one_week_ago, today)
                                    )
    datetime_arr = [one_week_ago + datetime.timedelta(days=day) for day in range(7)]
    date_arr = []
    for d in datetime_arr:
        date_arr.append(str(d.month) + "月" + str(d.day) + "日")
    zero_arr = [0.0, 0.0, 0.0, 0.0, 0.0]
    sum_arr = [zero_arr, zero_arr, zero_arr, zero_arr, zero_arr, zero_arr, zero_arr]
    for receipt in receipts:
        day = receipt.receipt_date.astimezone(JST)
        print(today.replace(hour=0,minute=0,second=0,microsecond=0))
        print(day.replace(hour=0,minute=0,second=0,microsecond=0))
        index = 6 - (today.replace(hour=0,minute=0,second=0,microsecond=0) - day.replace(hour=0,minute=0,second=0,microsecond=0)).days

        print(index)
        details = receipt.fooddetail_set.all()
        sum_salt = 0.0
        sum_protein = 0.0
        sum_energy = 0.0
        sum_carb = 0.0
        sum_fat = 0.0
        for detail in details:
            amount = detail.amount
            amount_num = amount // 100
            salt = detail.food.salt
            sum_salt += round(salt * amount_num, 1)
            protein = detail.food.protein
            sum_protein += round(protein * amount_num, 1)
            energy = detail.food.energy
            sum_energy += round(energy * amount_num, 1)
            carb = detail.food.carb
            sum_carb += round(carb * amount_num, 1)
            fat = detail.food.fat
            sum_fat += round(fat* amount_num, 1)
        sum_arr[index] = [sum_salt, sum_protein, sum_energy, sum_carb, sum_fat]
    context = {"sum_arr": sum_arr, "date_arr": date_arr}
    print(date_arr)
    print(sum_arr)
    return render(request, "receiptapp/graph.html", context)



# WEB APIの処理
def new(request, *args, **kwargs):
    # 新規レシート投稿
    user = request.user
    image_id = request.session['image_id']
    image = Image.objects.get(pk=image_id)
    # receipt 保存の処理
    receipt = Receipt(user=user, image=image)
    # food に add する前に一度saveしないとerrorになる
    receipt.save()

    # create_foodに処理を記述
    create_food.create_food(request, receipt)

    # image_id session の削除
    del request.session["image_id"]
    receiptId = receipt.id
    return redirect('/receipts/' + str(receiptId))

def delete(request, receiptId):
    # レシート情報削除
    Receipt.objects.filter(id=receiptId).delete()
    request.session["msg"] = "レシートを削除しました"
    return redirect('/')

def food_new(request, receiptId):
    receipt = Receipt.objects.get(id=receiptId)
    create_food.create_food(request, receipt)
    return redirect('/receipts/' + str(receiptId))

def food_edit(request, receiptId, foodId, detailId):
    # 食べ物情報編集
    # receipt の foodsからfoodIdでremoveした後にaddして、foods_detailを新たに作成
    receipt = Receipt.objects.get(id=receiptId)
    food = Food.objects.get(id=foodId)
    # 対応するdetailもdeleteする
    Fooddetail.objects.filter(id=detailId).delete()
    # 、detailを作る処理など
    create_food.create_food(request, receipt)
    return redirect('/receipts/' + str(receiptId))

def food_delete(request, detailId):
    # 食べ物情報削除(detailを削除)
    detail = Fooddetail.objects.get(id=detailId)
    receiptId = detail.receipt.id
    detail.delete()
    return redirect('/receipts/' + str(receiptId))

def image_new(request, *args, **kwargs):
    form = ImageForm(request.POST, request.FILES)
    if not form.is_valid():
        raise ValueError('invalid form')
    post = form.save()
    post.save()
    print(post.id)
    print(post.image.url)
    request.session['image_id'] = post.id
    print(request.session['image_id'])

    return redirect('/receipts/food_select')
