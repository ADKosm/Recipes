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

# Create your views here.

def index(request):
    context = {
        'name': "POTOMOK"
    }
    context['username'] = auth.get_user(request).username
    return render(request, 'index.html', context)


def hello(request):
    return HttpResponse("YOOOOOOU")

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
