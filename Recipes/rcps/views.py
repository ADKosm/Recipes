from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.http.response import HttpResponse, Http404
from django.template.loader import get_template
from django.template import Context
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.template.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist
from django.forms import Form
import json
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index.html', {})
   # context['username'] = auth.get_user(request).username

def liveIng(request):
    # TODO: найти в базе ингредиенты, начинающиеся с указанного префикса
    # 'prefix' -- то, что успел ввести пользователь, и требуется дополнить
    return JsonResponse({"vars": ["мозг", "молоко", "мондарин", "морс", request.GET['prefix'] ]})

def liveEq(request):
    # TODO: аналогично с  liveIng, только для инструментов
    return JsonResponse({"vars": ["кастрюля", "пароварка", "комбайнер", "ступка", request.GET['prefix'] ]})

def login(request):
    context = {}
    context.update(csrf(request))
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            context['login_error'] = "This user doesn't exist"
            return render_to_response('login.html', context)

    else:
        return render_to_response('login.html', context)


def logout(request):
    auth.logout(request)
    return redirect("/")


def register(request):
    context = {}
    context.update(csrf(request))
    context['form'] = UserCreationForm()
    if request.POST:
        registration_form = UserCreationForm(request.POST)
        if registration_form.is_valid():
            newuser = registration_form.save()
            registration = auth.authenticate(username=registration_form.cleaned_data['username'],
                                             password=registration_form.cleaned_data['password2'])
            auth.login(request, registration)

            return redirect('/')
        else:
            context['form'] = registration_form
    return render_to_response('register.html', context)

def search(request):
    # TODO: поиск рецептов по базе для указанных ингрединентов и оборудования
    # все данные хранятся в CSV с запятой на конце
    # ings -> ингредиенты
    # equips -> инструменты
    # pres -> 1 ==  в наличии, 0 == не в наличии
    return HttpResponse( request.GET['ings'] + " | " + request.GET['equips'] + " | " + request.GET['pres'])