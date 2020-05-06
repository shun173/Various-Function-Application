import json
import requests
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import Friend, PointFluctuation, Questionnaire
from snsapp.models import Article
from ecapp.models import Product
from .forms import CustomUserCreationForm, QuestionnaireForm, ProfileForm


def index(request):
    articles = Article.objects.all().order_by('-created_at')
    products = Product.objects.all().order_by('-id')
    context = {
        'articles': articles,
        'products': products,
    }
    return render(request, 'users/index.html', context)


@login_required
def my_page(request):
    return render(request, 'users/my_page.html')


@login_required
def edit_profile(request):
    user = request.user
    # プロフィールが更新されたとき
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST)
        if profile_form.is_valid():
            user.username = profile_form.cleaned_data['username']
            user.email = profile_form.cleaned_data['email']
            # 住所検索されたとき
            if 'search_address' in request.POST:
                zip_code = request.POST['zip_code']
                address = get_address(zip_code)
                profile_form = ProfileForm(
                    initial={'username': user.username, 'email': user.email, 'zip_code': zip_code, 'address': address})
                if not address:
                    messages.warning(request, "住所を取得できませんでした")
                    return redirect('users:edit_profile')
                return render(request, 'users/edit_profile.html', {'profile_form': profile_form})
            user.address = profile_form.cleaned_data['address']
            user.save()
            return redirect('users:my_page')
    profile_form = ProfileForm(
        initial={'username': user.username, 'email': user.email, 'address': user.address})
    return render(request, 'users/edit_profile.html', {'profile_form': profile_form})


def user_detail(request, user_id):
    user_model = get_user_model()
    user = user_model.objects.get(id=user_id)
    articles = Article.objects.filter(author=user)
    products = Product.objects.filter(owner=user)
    context = {
        'user': user,
        'articles': articles,
        'products': products,
    }
    return render(request, 'users/user_detail.html', context)


@login_required
def friend_list(request):
    user = request.user
    friend_instances = Friend.objects.filter(owner=user)
    friends = []
    for friend_instance in friend_instances:
        friend = friend_instance.friends
        friends.append(friend)
    return render(request, 'users/friend_list.html', {'friends': friends})


@login_required
def point_history(request):
    user = request.user
    point_fluctuations = PointFluctuation.objects.filter(user=user)
    return render(request, 'users/point_history.html', {'point_fluctuations': point_fluctuations})


@login_required
def questionnaire(request):
    user = request.user
    # アンケート回答済みのユーザーはリダイレクト
    questionnaire = Questionnaire.objects.filter(user=user)
    if questionnaire:
        messages.warning(request, '既にアンケートに回答済みです')
        return redirect('users:index')

    questionnaire_form = QuestionnaireForm(request.POST or None)
    if questionnaire_form.is_valid():
        content = questionnaire_form.cleaned_data['content']
        evaluation = questionnaire_form.cleaned_data['evaluation']
        # ポイント付与
        user.point += 300
        user.save()
        point_fluctuations = PointFluctuation(
            user=user, event='アンケートに回答', change=300)
        point_fluctuations.save()

        questionnaire = Questionnaire(
            user=user, content=content, evaluation=evaluation)
        questionnaire.save()
        # 開発者にメール送信
        subject = 'アンケート結果'
        message = f'評価　：　{evaluation}\n\n{content}'
        developer = get_user_model().objects.get(id=1)
        from_email = settings.DEFAULT_FROM_EMAIL
        developer.email_user(
            subject=subject, message=message, from_email=from_email)

        messages.success(request, 'アンケートにご協力いただきありがとうございます。300ポイントが付与されました。')
        return redirect('users:index')
    return render(request, 'users/questionnaire.html', {'questionnaire_form': questionnaire_form})


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid:
            new_user = form.save()
            input_email = form.cleaned_data['email']
            input_password = form.cleaned_data['password1']
            new_user = authenticate(
                email=input_email, password=input_password)
            if new_user is not None:
                login(request, new_user)
                return redirect('users:index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})


def get_address(zip_code):
    REQUEST_URL = f'http://zipcloud.ibsnet.co.jp/api/search?zipcode={zip_code}'
    address = ''
    response = requests.get(REQUEST_URL, timeout=5)
    response = json.loads(response.text)
    result, api_status = response['results'], response['status']
    if api_status == 200 and result != None:
        result = result[0]
        address = result['address1'] + result['address2'] + result['address3']
    return address


@receiver(user_logged_in)
def user_loged_in_callback(sender, request, user, **kwargs):
    """ログインした際に呼ばれる"""
    user.last_login = timezone.now()
    user.save()
