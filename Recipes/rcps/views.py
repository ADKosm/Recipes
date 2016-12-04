from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def index(request):
    context = {
        'name': "POTOMOK"
    }
    return render(request, 'index.html', context)

def hello(request):
    return HttpResponse("YOOOOOOU")
