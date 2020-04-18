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
            print("new_user is created")
            input_email = form.cleaned_data['email']
            input_password = form.cleaned_data['password1']
            new_user = authenticate(
                email=input_email, password=input_password)
            print("new_user is authenticated")
            if new_user is not None:
                print("new_user is not None")
                login(request, new_user)
                return redirect('users:index')
        else:
            print("new_user is not valid")
            message = "無効な値が入力されました。"
            return render(request, 'users/signup.html', {'message': message})
    else:
        print("method = GET")
        form = CustomUserCreationForm()
    print("new_user is None")
    return render(request, 'users/signup.html', {'form': form})
