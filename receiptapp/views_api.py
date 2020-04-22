import django_filters
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from rest_framework import serializers, generics
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .modules import receipt_tyuusyutu2
from .modules import receipt_text2
from .modules import receipt_text3
from .modules import create_food
import cloudinary
from rest_framework.decorators import api_view, permission_classes
from rest_framework.decorators import renderer_classes
import json
from django.shortcuts import redirect
import cv2
import base64
from django.http import JsonResponse
from .forms import ImageForm

from .models import Receipt, Image, Food, Fooddetail, Progress
from django.contrib.auth.models import User

from django.views.decorators.csrf import csrf_exempt

import environ
import cloudinary

env = environ.Env()
env.read_env('.env')

cloudinary.config(
  cloud_name = env('CLOUD_NAME'),
  api_key = env('API_KEY'),
  api_secret = env('API_SECRET')
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

class ReceiptSerializer(serializers.ModelSerializer):
    # apiのカスタマイズ
    # 外部キーの数値のみが表示されるのではなく、参照先の情報を取得してほしい
    # userのserializerを上書き
    # user = UserSerializer()
    # image = ImageSerializer()

    class Meta:
        model = Receipt
        fields = '__all__'

# web api のメイン部分
# ModelViewSet => 自身かserializerで指定したモデルに対応するweb apiが6つ同時に有効になる
class ReceiptViewSet(viewsets.ModelViewSet):
    queryset = Receipt.objects.all()

    # listメソッドを上書き => listはreceiptsに対応する
    def list(self, request):
        queryset = Receipt.objects.filter(user = request.user)
        data = ReceiptSerializer(queryset, many=True).data
        return Response(status=200, data=data)

    serializer_class = ReceiptSerializer

    # filter, ?user=1 のようにパラメータを指定することでuserのprimarykeyが1のもののみを取得できる
    # filter_fields = ('user',)

    # authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ["post"]

    def create(self, request):
        image = Image(image = request.image)
        image.save()
        return Response(status=200, data={"msg": "ok"})

# Generic View => 特定のレコードに紐づくような処理
class UsernameGetView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, format=None):
        return Response(data={
            'username': request.user.username,
            },
            status=status.HTTP_200_OK)

@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def get_text(request):
    print("get_text")
    filename = request.POST.get("filename")
    username = request.POST.get("username")
    text = receipt_text2.convert(filename = filename, CUT=True)
    #request.session["filename"] = filename
    #request.session["img"] = img
    return Response(status=200, data=json.dumps({"text": text,"filename": filename}))

@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def receipts_analyse(request):
    filename = request.POST.get("filename")
    print(filename)
    img = receipt_text3.convert(filename, CUT=True)

    _, frame = cv2.imencode('.JPEG', img)
    print(frame)
    img_str = base64.b64encode(frame)
    b64str = "data:image/jpeg;base64," + str(img_str).replace("b'", "").replace("'", "")
    # print(b64str)
    # cloudinaryにbase64でupload
    public_id = filename.split("/")[-1].replace(".jpg", "").replace(".png", "") + "_rect_th"
    cloudinary.uploader.upload(b64str, public_id = public_id)

    # search_list = q.enqueue(background_process, filename=filename, isWord=False, word="")
    # sessionにsearch_listを保存する
    filename = filename[::-1].replace(".", ".ht_tcer_", 1)[::-1]
    # request.session["public_id"] = public_id
    # return redirect('/')
    return Response(status=200, data=json.dumps({"filename": filename, "public_id": public_id}))

@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def img_to_text(request):
    filename = request.POST.get("filename")
    text = receipt_text3.img_to_text(filename)
    print(text)
    public_id = request.POST.get("public_id")
    cloudinary.uploader.destroy(public_id = public_id)
    cloudinary.uploader.destroy(public_id = public_id.replace("_rect_th", ""))
    return Response(status=200, data=json.dumps({"text": text, "filename": filename}))

@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def get_search_list(request):
    print("get_search_list")
    filename = request.POST.get("filename")
    text = request.POST.get("text")
    search_list = receipt_tyuusyutu2.analyse(filename=filename, isWord=False, word="", text=text)[0]
    print(search_list)
    public_id = filename.split("/")[-1].replace(".jpg", "").replace(".png", "")
    cloudinary.uploader.destroy(public_id = public_id)

    name_list = []
    energy_list = []
    protein_list = []
    fat_list = []
    carb_list = []
    salt_list = []

    for i1, info_list in enumerate(search_list):
        name_list.append([])
        energy_list.append([])
        protein_list.append([])
        fat_list.append([])
        carb_list.append([])
        salt_list.append([])
        for info in info_list[0]:
            name_list[i1].append(info[0])
            energy_list[i1].append(info[1])
            protein_list[i1].append(info[2])
            fat_list[i1].append(info[3])
            carb_list[i1].append(info[4])
            salt_list[i1].append(info[5])
            for i2, v in enumerate(info):
                info[i2] = str(v)

    # 配列をjsonで返せるの？
    return Response(status=200, data=json.dumps([name_list, energy_list, protein_list, fat_list, carb_list, salt_list]))


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def new_receipt(request):
    user = request.user
    image = Image(image = None)
    image.save()
    # receipt 保存の処理
    receipt = Receipt(user=user, image=image)
    # food に add する前に一度saveしないとerrorになる
    receipt.save()
    print(request.POST.get("name_list"))
    # create_foodに処理を記述
    create_food.create_food_api(request.POST.get("name_list").split(",,"),
    request.POST.get("energy_list").split(",,"),
    request.POST.get("protein_list").split(",,"),
    request.POST.get("carb_list").split(",,"),
    request.POST.get("fat_list").split(",,"),
    request.POST.get("salt_list").split(",,"),
    request.POST.get("amount_list").split(",,"),
    receipt
    )
    return Response({"message": "receipt OK",})

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def test1(request):
    return Response({"title": request.POST.get("title")})






@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def get_food(request):
    receipt = Receipt.objects.get(id=int(request.POST.get("receipt_id")))
    details = receipt.fooddetail_set.all()
    foods_list = []
    for detail in details:
        foods_list.append(detail.food.food_name)
    return Response(status=200, data=json.dumps(foods_list))

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def get_month_receipts(request):
    print(request.POST.get("year"))
    print(request.POST)
    receipts = Receipt.objects.filter(
        user = request.user,
        receipt_date__year = int(request.POST.get("year")),
        receipt_date__month = int(request.POST.get("month"))
    )
    receipt_list = []
    for receipt in receipts:
        details = receipt.fooddetail_set.all()
        foodname_list = []
        for detail in details:
            foodname_list.append(detail.food.food_name)
        receipt_list.append([
                            receipt.id,
                            str(receipt.receipt_date),
                            foodname_list
                            ])
    return Response(status=200, data=json.dumps(receipt_list))







from django_celery_results.models import TaskResult
from mysite.tasks import add, get_search_list

# ajaxでこのapiを1秒間隔などで呼び出す？
# レシート解析は始めは15秒ほど待っても良いと思う
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def worker_result(request):
    print("worker_resultにajaxがきました")
    task_id = request.POST.get("task_id")
    try:
        tr = TaskResult.objects.get(task_id=task_id)
        result = tr.result
        tr.delete()
    except:
        result = 0
    return JsonResponse({"result": result})


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def worker_add(request):
    x = int(request.POST.get('input_a'))
    y = int(request.POST.get("input_b"))
    task = add.delay(x,y)
    task_id = task.id
    return JsonResponse({"task_id": task_id})


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def worker_analyse(request):
    print("worker_analyseにajaxがきました")
    form = ImageForm(request.POST, request.FILES)
    if not form.is_valid():
        raise ValueError('invalid form')
    post = form.save()
    post.save()

    task = get_search_list.delay(image_id = post.id)
    task_id = task.id

    return JsonResponse({"task_id": task_id})

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def get_progress(request):
    task_id = request.POST.get('task_id')
    progress = Progress.objects.get(task_id=task_id)
    return JsonResponse({"progress_no": progress.progress_no})
