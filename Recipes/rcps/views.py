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
from rcps.models import Ingredient, Equipment, Recipe


def index(request):
    context = {'username': auth.get_user(request).username}
    return render(request, 'index.html', context)

def liveIng(request):
    vars = Ingredient.objects.filter(ingredient_name__startswith=request.GET['prefix'])[:5]
    return JsonResponse({"vars": [x.ingredient_name for x in vars]})

def liveEq(request):
    vars = Equipment.objects.filter(equipment_name__startswith=request.GET['prefix'])[:5]
    return JsonResponse({"vars": [x.equipment_name for x in vars]})

def login(request):
    print("=======LOGIN==============")
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
    print("================LOGOUT===============")
    auth.logout(request)
    return redirect("/")


def register(request):
    context = {}
    context.update(csrf(request))
    context['form'] = UserCreationForm().as_p()
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
    ingredient_names = [x for x in request.GET['ings'].split(',') if x]
    equipment_names = [x for x in request.GET['equips'].split(',') if x]

    forbidden_ingredients = \
        Ingredient.objects.exclude(ingredient_name__in=ingredient_names).values_list('id', flat=True)
    forbidden_equipment = None
    if request.GET['equips'] == 1:
        forbidden_equipment = Equipment.objects.exclude(equipment_name__in=equipment_names)
    else:
        forbidden_equipment = Equipment.objects.filter(equipment_name__in=equipment_names)
    forbidden_equipment = forbidden_equipment.values_list('id', flat=True)


    return HttpResponse( request.GET['ings'] + " | " + request.GET['equips'] + " | " + request.GET['pres'])