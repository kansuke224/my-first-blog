from django import forms

from .models import Post # 同じ階層のmodelsファイルからPostクラスをimport

class PostForm(forms.ModelForm):

    class Meta: # フォームを作るときにどのモデルを使うかを django に伝える
        model = Post
        fields = ("title", "text",)
