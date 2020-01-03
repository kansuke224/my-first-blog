from django.conf import settings
from django.db import models
from django.db.models import Max
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver
import uuid
import os

import cloudinary
from cloudinary.models import CloudinaryField

def get_image_path(instance, filename):
    prefix = 'receiptapp/'
    # max = Image.objects.all().aggregate(Max('id'))['id__max']
    # name = str(max + 1)
    name = str(uuid.uuid4()).replace('-', '')
    extension = os.path.splitext(filename)[-1]
    return prefix + name + extension


# modelには必要不可欠なフィールドと、そのデータの挙動を収める

class Receipt(models.Model):
    # receipt_id = models.AutoField(primary_key=True, default=0)
    receipt_date = models.DateTimeField(default=timezone.now)
    # 多 対 1 のリレーションのときは ForeingKeyが使える
    # ForeignKeyにはsaveするときにオブジェクトを渡す
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    # foods = models.ManyToManyField("Food", blank=True)
    image = models.OneToOneField("Image", on_delete=models.CASCADE, default=0)
    # Receipt.food_detail_set.all()

class Food(models.Model):
    # food_id = models.AutoField(primary_key=True, default=0)
    food_name = models.CharField(max_length=50, default="default_food")
    protein = models.FloatField()
    fat = models.FloatField()
    carb = models.FloatField()
    salt = models.FloatField()
    energy = models.FloatField()
    # receipt = models.ForeignKey("Receipt", on_delete=models.CASCADE)

class Fooddetail(models.Model):
    amount = models.PositiveSmallIntegerField()
    receipt = models.ForeignKey("Receipt", on_delete=models.CASCADE, default=0)
    food = models.ForeignKey("Food", on_delete=models.CASCADE, default=0)

class Image(models.Model):
    # image = models.ImageField(upload_to=get_image_path)
    image = CloudinaryField('image', blank=True, null=True)

# モデル削除後に`file_field`を削除する。
@receiver(post_delete, sender=Image)
def delete_file(sender, instance, **kwargs):
    instance.image.delete(False)
