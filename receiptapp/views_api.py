import django_filters
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from rest_framework import serializers, generics
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .modules import receipt_tyuusyutu
from .modules import create_food
import cloudinary
from rest_framework.decorators import api_view, permission_classes

from .models import Receipt, Image, Food, Fooddetail
from django.contrib.auth.models import User

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
    user = UserSerializer()
    image = ImageSerializer()

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

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def new_image(request):
    user = request.user

    # swift から送られてきた画像をもとにimageを作成
    # request.FILES みたいな書き方かもしれない、後で直す
    image = Image(image = request.POST.get("image"))
    image.save()
    request.session['image_id'] = image.id

    # httpheaderを取得?
    # userAgent = request.META.get('HTTP_USER_AGENT', None)
    filename = image.url.replace("/media/receiptapp/", "")
    print(filename)

    # search_list = q.enqueue(background_process, filename=filename, isWord=False, word="")
    search_list = receipt_tyuusyutu.analyse(filename=filename, isWord=False, word="")[0]

    public_id = filename.split("/")[-1].replace(".jpg", "").replace(".png", "")
    cloudinary.uploader.destroy(public_id = public_id)

    for info_list in search_list:
        for info in info_list[0]:
            for i, v in enumerate(info):
                info[i] = str(v)
    context = {"user": user, "search_list": search_list}
    # jsonでlistを渡すことができるのか分からない todo
    return Response({"message": "Got some data!", "data": search_list})

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def new_receipt(request):
    user = request.user
    image = Image(image = Null)
    # receipt 保存の処理
    receipt = Receipt(user=user, image=image)
    # food に add する前に一度saveしないとerrorになる
    receipt.save()

    # create_foodに処理を記述
    create_food.create_food(request, receipt)
    return Response({"message": "Got some data!",})

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def test1(request):
    return Response({"title": request.POST.get("title")})

# 画像をcloudinaryに保存してurlを渡す  =>  swift     or        alamofireで直接画像を渡す
# apiでurlから画像を取得し解析  => django new_image
# データベースに保存をする => django new_image
# food_selectのためのデータをiphoneに返す => django new_image
# iphoneで選択する => swift
# apiでreceipt保存 => django new_receipt
# 一覧 => swift
