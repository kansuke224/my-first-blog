from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post # . はカレントディレクトリにあることを示している
from .forms import PostForm
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

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid(): # is_valid()関数 => フォームが正しい形がどうかをチェックしてくれる
            post = form.save(commit=False) # title と text しか入ってない, form を使えるようにいったん commit=false(まだ保存しないという意味)でpost変数に格納する
            post.author = request.user # 投稿者を request.user にする
            post.published_date = timezone.now() # 公開日時を今の時間にする
            post.save() # 今度こそPostを保存
            return redirect('post_detail', pk=post.pk) # 投稿の詳細にリダイレクト, views 内の post_detailメソッドを呼ぶ
    else:
        form = PostForm()
    return render(request, "blog/post_edit.html", {"form": form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk) # 編集したいPOSTモデルを取得する
    if request.method == "POST": # saveボタンを押したときにこちらの条件分岐が true になる
        form = PostForm(request.POST, instance=post) #PostFormのインスタンスを作るときはPostをinstanceに渡す 保存をしたいとき
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect("post_detail", pk=post.pk)
    else: # 編集ボタンからアクセスしてきた時はこっちにとおされる
        form = PostForm(instance=post) # 編集だけしたいとき
    return render(request, "blog/post_edit.html", {"form": form})
