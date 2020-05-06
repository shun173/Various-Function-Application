import re
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import Article, Good
from .forms import ArticleForm
from users.models import Friend, PointFluctuation
from users.forms import SearchForm
from ecapp.models import Product


def index(request):
    search_form = SearchForm(request.POST or None)
    articles = Article.objects.all().order_by('-created_at')
    # 検索フォーム
    if request.method == 'POST':
        if search_form.is_valid():
            user = request.user
            select = search_form.cleaned_data['select']
            keyword = search_form.cleaned_data['keyword']

            # ユーザー選択時の処理
            if select == '友人のみ':
                result_users = []
                for friend_instance in Friend.objects.filter(owner=user):
                    friend = friend_instance.friends
                    result_users.append(friend)
            if select == '全体':
                user_model = get_user_model()
                result_users = user_model.objects.all()

            searched_articles = []
            for result_user in result_users:
                articles = Article.objects.filter(author=result_user)
                for article in articles:
                    searched_articles.append(article)

            # ワード検索時の処理
            if keyword:
                articles = []
                for article in searched_articles:
                    author = article.author.username
                    content = article.content
                    product = article.product
                    if product:
                        product = product.name
                    else:
                        product = ''
                    text_list = [author, content, product]
                    text = ' '.join(text_list)
                    if re.findall(keyword, text, re.IGNORECASE):
                        articles.append(article)
            if not keyword:
                articles = searched_articles

    context = {
        'search_form': search_form,
        'articles': articles
    }
    return render(request, 'snsapp/index.html', context)


@login_required
def my_articles(request):
    user = request.user
    articles = Article.objects.filter(author=user)
    return render(request, 'snsapp/index.html', {'articles': articles})


@login_required
def post_article(request):
    if request.method == 'POST':
        author = request.user
        content = request.POST['content']
        product_id = request.POST['product']
        if product_id:
            product = Product.objects.get(pk=product_id)
            article = Article.objects.create(
                author=author, content=content, product=product)
        else:
            article = Article.objects.create(author=author, content=content)
        article.save()
        messages.success(request, '記事を投稿しました')
        return redirect('snsapp:index')
    else:
        user_id = request.user.id
        article_form = ArticleForm(user_id=user_id)
    return render(request, 'snsapp/post_article.html', {'article_form': article_form})


@login_required
def good(request, pk):
    user = request.user
    article = Article.objects.get(pk=pk)

    # 送信元アプリの判別
    ref_url = request.META['HTTP_REFERER']
    if 'snsapp' in ref_url:
        app = 'snsapp'
    else:
        app = 'users'

    # ユーザーが既にgoodを押していたときは何もせずリダイレクト
    if Good.objects.filter(pusher=user).filter(article=article):
        messages.warning(request, '既にgoodを押した記事です')
        return redirect(f'{app}:index')

    # good_countを増やす
    article.good_count += 1
    article.save()

    # ポイント履歴を記録
    point_fluctuation = PointFluctuation(
        user=article.author, event=f'記事"{article.content}"にgoodが押されました', change=1)
    point_fluctuation.save()

    # goodを記録
    good = Good.objects.create(pusher=user, article=article)
    good.save()
    messages.success(request, '記事にgoodしました')
    return redirect(f'{app}:index')
