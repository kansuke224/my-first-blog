from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post # . はカレントディレクトリにあることを示している
# import するとき .py 拡張子は必要ない

# Create your views here.
def post_list(request): # request を引数にとる
    # 変数postsはクエリセットを参照している
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by("published_date")
    return render(request, "blog/post_list.html", {"posts": posts}) # render関数をreturn
    # 名前と値をセットにしてテンプレートに渡したい引数を第三引数の map に記述する

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, "blog/post_detail.html", {"post": post})
