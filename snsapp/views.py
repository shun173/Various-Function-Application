from django.shortcuts import render


def index(request):
    return render(request, 'snsapp/sns_index.html')
