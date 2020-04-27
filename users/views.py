from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils import timezone

from django.contrib.auth import get_user_model
from snsapp.models import Article
from ecapp.models import Product
from .forms import CustomUserCreationForm


def index(request):
    return render(request, 'users/index.html')


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
