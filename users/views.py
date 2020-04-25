from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm


def index(request):
    return render(request, 'users/index.html')


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
