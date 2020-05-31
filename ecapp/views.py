import re
import json
import requests
from django.conf import settings
from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework import permissions
from .forms import AddToCartForm, SellForm
from users.models import Friend, PointFluctuation
from users.forms import SearchForm, ProfileForm
from users.views import get_address
from snsapp.models import Article
from .models import Product, Sale
from .serializers import ProductSerializer


def index(request):
    search_form = SearchForm(request.POST or None)
    products = Product.objects.all()
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

            searched_products = []
            for result_user in result_users:
                products = Product.objects.filter(owner=result_user)
                for product in products:
                    searched_products.append(product)

            # ワード検索時の処理
            if keyword:
                products = []
                for product in searched_products:
                    name = product.name
                    owner = product.owner.username
                    description = product.description
                    if not description:
                        description = ''
                    text_list = [name, owner, description]
                    text = ' '.join(text_list)
                    if re.findall(keyword, text, re.IGNORECASE):
                        products.append(product)
            if not keyword:
                products = searched_products

    num = request.GET.get('page')
    if not num:
        num = 1
    products = Paginator(products, 12)
    products = products.get_page(num)
    context = {
        'search_form': search_form,
        'products': products
    }
    return render(request, 'ecapp/index.html', context)


def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        num = request.POST['num']
        num = int(num)
        if num == 0:
            messages.warning(request, '個数を選択してください')
            return redirect('ecapp:detail', product_id=product_id)
        if 'cart' in request.session:
            if str(product_id) in request.session['cart']:
                request.session['cart'][str(product_id)] += num
            else:
                request.session['cart'][str(product_id)] = num
        else:
            request.session['cart'] = {str(product_id): num}
        messages.success(request, f"{product.name}を{num}個カートに入れました！")
        return redirect('ecapp:cart')
    else:
        add_to_cart_form = AddToCartForm(product_id=product_id)
        context = {
            'product': product,
            'add_to_cart_form': add_to_cart_form,
        }
    return render(request, 'ecapp/detail.html', context)


def detail_from_article(request):
    product_id = request.GET.get('product_id')
    article_id = request.GET.get('article_id')
    if 'product_from_article' in request.session:
        request.session['product_from_article'][str(
            product_id)] = str(article_id)
    else:
        request.session['product_from_article'] = {
            str(product_id): str(article_id)}
    print(product_id)
    product_id = int(product_id)
    return detail(request, product_id)


@login_required
@require_POST
def toggle_fav_product_status(request):
    product = get_object_or_404(Product, pk=request.POST["product_id"])
    user = request.user
    if product in user.fav_products.all():
        user.fav_products.remove(product)
    else:
        user.fav_products.add(product)
    return redirect('ecapp:detail', product_id=product.id)


@login_required
def fav_products(request):
    user = request.user
    products = user.fav_products.all().order_by('-created_at')
    num = request.GET.get('page')
    if not num:
        num = 1
    products = Paginator(products, 12)
    products = products.get_page(num)
    return render(request, 'ecapp/index.html', {'products': products})


@login_required
def my_products(request):
    user = request.user
    products = Product.objects.filter(owner=user).order_by('-created_at')
    num = request.GET.get('page')
    if not num:
        num = 1
    products = Paginator(products, 12)
    products = products.get_page(num)
    return render(request, 'ecapp/index.html', {'products': products})


@login_required
def cart(request):
    user = request.user
    cart = request.session.get('cart', {})
    cart_products = dict()
    total_price = 0
    for product_id, num in cart.items():
        product = Product.objects.get(id=product_id)
        cart_products[product] = num
        total_price += product.price * num

    purchase_form = ProfileForm(request.POST, None)
    if request.method == 'POST':
        # 住所検索ボタンが押された場合
        if 'search_address' in request.POST:
            zip_code = request.POST['zip_code']
            address = get_address(zip_code)
            if not address:
                messages.warning(request, '住所を取得できませんでした。')
                return redirect('ecapp:cart')
            purchase_form = ProfileForm(
                initial={'zip_code': zip_code, 'address': address})
        # 購入ボタンが押された場合
        if 'buy_product' in request.POST:
            if not bool(cart):
                messages.warning(request, "カートは空です。")
                return redirect('ecapp:cart')
            if total_price > user.point:
                messages.warning(request, "所持ポイントが足りません。")
                return redirect('ecapp:cart')
            for product_id in cart:
                product = Product.objects.get(pk=product_id)
                if product.owner == user:
                    messages.warning(request, "自身が出品した商品は購入できません。")
                    return redirect('ecapp:cart')
            if not user.address:
                address = request.POST['address']
                if not address:
                    messages.warning(request, "住所の入力は必須です。")
                    return redirect('ecapp:cart')
                user.address = address
                user.save()

            for product_id, num in cart.items():
                if not Product.objects.filter(pk=product_id).exists():
                    del cart[product_id]
                product = Product.objects.get(pk=product_id)
                product.amount -= num
                product.save()
                sale = Sale(product=product, user=user,
                            amount=num, price=product.price)
                sale.save()
                # ポイント履歴を記録
                # 購入者
                sum = product.price * num
                PointFluctuation.objects.create(
                    user=user, event=f'{product.name}を{num}個購入', change=-sum)
                # 出品者
                owner = product.owner
                owner.point += sum
                owner.save()
                PointFluctuation.objects.create(
                    user=owner, event=f'{product.name}が{num}個売れた', change=sum)
                # 出品者にメール送信
                subject = '商品が購入されました'
                message = f'''商品　：　{product.name}　が　{num}個　購入されました。\n\n
                            購入者　：　{user.username}\n
                            住所　：　{user.address}\n\n
                            上記の住所に商品を届けてください。その後{sum}ポイントが付与されます。
                '''
                from_email = settings.DEFAULT_FROM_EMAIL
                owner.email_user(
                    subject=subject, message=message, from_email=from_email)
                # 紹介記事のリンクから購入された商品の場合、紹介者にもポイント付与
                products = request.session['product_from_article']
                if product_id in products:
                    article_id = products[str(product_id)]
                    article = Article.objects.get(id=article_id)
                    author = article.author
                    author.point += int(sum / 100)
                    PointFluctuation.objects.create(
                        user=author, event=f'記事："{article.content}" からの商品購入', change=int(sum/100))
                    del request.session['product_from_article'][str(
                        product_id)]
            user.point -= total_price
            user.save()
            del request.session['cart']
            messages.success(request, "商品の購入が完了しました！")
            return redirect('ecapp:cart')

    num = request.GET.get('page')
    if not num:
        num = 1
    products = []
    for product in cart_products:
        products.append(product)
    products = Paginator(products, 5)
    products = products.get_page(num)
    context = {
        'purchase_form': purchase_form,
        'cart_products': cart_products,
        'total_price': total_price,
        'products': products,
    }
    return render(request, 'ecapp/cart.html', context)


@login_required
@require_POST
def change_item_amount(request):
    product_id = request.POST["product_id"]
    cart_session = request.session['cart']
    if product_id in cart_session:
        if 'action_remove' in request.POST:
            cart_session[product_id] -= 1
        if 'action_add' in request.POST:
            product = Product.objects.get(id=product_id)
            if cart_session[product_id] < product.amount:
                cart_session[product_id] += 1
            else:
                messages.warning(request, '在庫数をご確認ください。')
        if cart_session[product_id] <= 0:
            del cart_session[product_id]
    return redirect('ecapp:cart')


@login_required
def order_history(request):
    user = request.user
    sales = Sale.objects.filter(user=user).order_by('-created_at')
    num = request.GET.get('page')
    sales = Paginator(sales, 5)
    sales = sales.get_page(num)
    return render(request, 'ecapp/order_history.html', {'sales': sales})


@login_required
def sell(request):
    if request.method == 'POST':
        sell_form = SellForm(request.POST, request.FILES)
        if sell_form.is_valid():
            product = sell_form.save(commit=False)
            product.owner = request.user
            product.save()
            messages.success(request, '商品を出品しました')
            return redirect('ecapp:my_products')
    else:
        sell_form = SellForm()
    return render(request, 'ecapp/sell.html', {'sell_form': sell_form})


@login_required
@require_POST
def delete(request, product_id):
    product = Product.objects.get(id=product_id)
    product.delete()
    return redirect('ecapp:index')


class ProductViewSet(viewsets.ModelViewSet):
    """API endpoint that allows users to be viewed or edited."""
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
