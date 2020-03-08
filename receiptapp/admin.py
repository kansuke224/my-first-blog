from django.contrib import admin
from .models import Receipt,Food,Image,Fooddetail,Progress

# Register your models here.
admin.site.register(Receipt)
admin.site.register(Food)
admin.site.register(Image)
admin.site.register(Fooddetail)
admin.site.register(Progress)
