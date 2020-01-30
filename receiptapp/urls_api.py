from rest_framework import routers
from . import views_api
from django.urls import path
from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token


router = routers.DefaultRouter()
router.register('receipts', views_api.ReceiptViewSet)
router.register('images', views_api.ImageViewSet)
urlpatterns = [
    path('token/', obtain_jwt_token),
    path('test1/', views_api.test1, name='test1'),
    path('new_image/', views_api.new_image, name='new_image'),
    path('get_text/', views_api.get_text, name='get_text'),
    path('get_search_list/', views_api.get_search_list, name='get_search_list'),
    url(r'^mypage/$', views_api.UsernameGetView.as_view()),
    ]

urlpatterns += router.urls


# eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNTc5NzQ1MTgwLCJlbWFpbCI6ImVzYWthLm5hb2hpcm9AZ21haWwuY29tIn0.RE8-zqtLzeJ55dPgOeMG0aQOcGA7IixjFvqKXLSfBfs"
# curl -X GET http://127.0.0.1:8000/api/mypage/ -H "Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNTc5NjcwMDcwLCJlbWFpbCI6ImthbnN1a2UyMjQyMjRAZ21haWwuY29tIn0.ETFng6lQMK5unPZyB-R0c_oA3jsF-NbO8_Y_CmcBoJ0"


# curl -X GET https://healthreceiptapp.herokuapp.com/api/receipts/ -H "Authorization: JWT

# curl -X POST http://127.0.0.1:8000/api/test1/ -d "title=receipts_api_test!!!" -H "Authorization: JWT










# eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo2LCJ1c2VybmFtZSI6Im5hb2RhaSIsImV4cCI6MTU3OTY3MTUzMCwiZW1haWwiOiIifQ.2IQc_pPWVl3GNXGILVKJAQPiuhzhaBXjaVfCEieUC0U
