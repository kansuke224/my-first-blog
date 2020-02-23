from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('receipts/new', views.receipts_new, name='receipts_new'),
    path('receipts/food_select', views.receipts_food_select, name='receipts_food_select'),
    path('receipts/<int:receiptId>', views.receipts_detail, name='receipts_detail'),
    path('receipts/<int:receiptId>/delcheck', views.receipts_delcheck, name='receipts_delcheck'),
    path('receipts/foods_edit/<int:receiptId>/<int:foodId>/<int:detailId>', views.foods_edit, name='receipts_foods_edit'),
    path('receipts/foods_edit/food_select/<int:receiptId>/<int:foodId>/<int:detailId>', views.foods_edit_select, name='receipts_foods_edit_select'),
    path('receipts/foods_new/<int:receiptId>', views.foods_new, name='receipts_foods_new'),
    path('receipts/foods_new/food_select/<int:receiptId>', views.foods_new_select, name='receipts_foods_new_select'),
    path('receipts/foods_new/after_eat/<int:receiptId>', views.foods_after_eat, name='after_eat'),
    path('graph', views.graph, name='graph'),

    path('new', views.new, name='new'),
    path('newZero', views.newZero, name='newZero'),
    path('delete/<int:receiptId>', views.delete, name='delete'),
    path('receipts/analyse/', views.receipts_analyse, name='receipts_analyse'),
    path('receipts/image_to_text/', views.image_to_text, name='image_to_text'),
    path('food_new/<int:receiptId>', views.food_new, name='food_new'),
    path('food_edit/<int:receiptId>/<int:foodId>/<int:detailId>', views.food_edit, name='food_edit'),
    path('food_delete/<int:detailId>', views.food_delete, name='food_delete'),
    path('food_after_eat/<int:detailId>', views.food_after_eat, name='food_after_eat'),
    path('food_after_eat_new/<int:receiptId></int>/<int:detailId>', views.food_after_eat_new, name='food_after_eat_new'),
    path('image_new', views.image_new, name='image_new'),

    path('celery', views.celery),
]

from django.conf import settings
from django.conf.urls.static import static


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
