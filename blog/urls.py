from django.urls import path # django の path 関数
from . import views # ブログアプリのすべてのビューをインポート
urlpatterns = [
    path("", views.post_list, name="post_list"),
    # post_list という view をルートurl("/")に割り当てる
    # name="post_list" は、viewを識別するために使われるURLの名前(?)
    path("post/<int:pk>", views.post_detail, name="post_detail")
]
