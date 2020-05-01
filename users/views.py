from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from django.contrib.auth import get_user_model
from .models import Friend, PointFluctuation
from snsapp.models import Article
from ecapp.models import Product
from .forms import CustomUserCreationForm, QuestionnaireForm


def index(request):
    articles = Article.objects.all().order_by('-created_at')
    products = Product.objects.all().order_by('-id')
    context = {
        'articles': articles,
        'products': products,
    }
    return render(request, 'users/index.html', context)


def my_page(request):
    return render(request, 'users/my_page.html')


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
    questionnaire_form = QuestionnaireForm()
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


@receiver(user_logged_in)
def user_loged_in_callback(sender, request, user, **kwargs):
    """ログインした際に呼ばれる"""
    user.last_login = timezone.now()
    user.save()
