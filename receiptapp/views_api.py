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
import json
from django.shortcuts import redirect

from .models import Receipt, Image, Food, Fooddetail
from django.contrib.auth.models import User

from django.views.decorators.csrf import csrf_exempt

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
def img_to_text(request):
    filename = request.session["filename"]
    img = request.session["img"]
    text = receipt_text3.img_to_text(img)
    print(text)
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

    # create_foodに処理を記述
    create_food.create_food_api(request.POST.get("name_list"),
    request.POST.get("energy_list"),
    request.POST.get("protein_list"),
    request.POST.get("carb_list"),
    request.POST.get("name_list"),
    request.POST.get("name_list")
    )
    return Response({"message": "receipt OK",})

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def test1(request):
    return Response({"title": request.POST.get("title")})


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def get_food(request):
    receipt = Receipt.objects.get(request["receipt_id"])
    details = receipt.fooddetail_set.all()
    for detail in details:
        foods_list.append(detail.food)

# 画像をcloudinaryに保存してfilenameを渡す  =>  swift
# またkeyとかをcloudinaryに教えてあげないといけない
# 保存自体は簡単そう


# post "filename"


# filenameからtext.convertをしてtextを取得
# filenamさえ正しければここはクリア


# post "text"

# textからanalyseをしてsearch_listを取得、swiftに返す
# search_listをわかりやすいように渡す
# [foodnamelist, foodnamelist2]みたいなかんじに加工して送ってもいいかも(uipickerで扱いやすくなるから)
# 詳細な成分はnew_receiptまで渡すためにresponseに含めないといけない


# iphoneで選択する => swift
# search_listをnew_receiptに送信
# post "search_list"

# apiでreceipt保存 => django new_receipt
# crerate_foodがうまくうごくかどうか
# requestの形をwebと同じにすればうまく動くはず
# 難しそうだったらcreate_food2を作る

# 一覧 => swift
# redirect?
