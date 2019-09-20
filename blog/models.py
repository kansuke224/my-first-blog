from django.db import models
from django.utils import timezone


class Post(models.Model): # models.Model クラスを継承することでこのクラスをデータベースに保存するようにdjangoに示している
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE) # 他のモデルへのリンク（？）
    title = models.CharField(max_length=200) # CharField 制限ありのテキスト
    text = models.TextField() # TestField 制限なしのテキスト
    # 日付とか時間とか
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
