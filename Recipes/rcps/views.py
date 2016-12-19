from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.http.response import HttpResponse, Http404
from django.template.loader import get_template
from django.template import Context
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.template.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist
from django.forms import Form
import json
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Avg, Count
from rcps.models import Ingredient, Equipment, Recipe, Comment, Tag, Grade
from rcps.selections import find_recipes, most_commented_recipes


# Create your views here.


def index(request):
    context = {'username': auth.get_user(request)}
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
    ing_tuple = tuple((x for x in request.GET['ings'].split(',') if x))
    equip_tuple = tuple((x for x in request.GET['equips'].split(',') if x))
    equpment_is_allowed = request.GET['pres'] == '1'
    result = find_recipes(ing_tuple, equip_tuple, equpment_is_allowed)
    #response = ('id:{}\nname:{}\nlink:{}\n'.format(x.id, x.recipe_name, x.recipe_link) for x in result)
    #response = '\n------------------------\n'.join(response)
    return render(request, 'list.html', {
        'recipes': result,
        'ingredients': ing_tuple,
        'equipments': equip_tuple,
        'eia': equpment_is_allowed,
        'username': auth.get_user(request)
    })#HttpResponse(response)

def recipe(request, recipe_id):
    currect_recipe = Recipe.objects.get(pk=recipe_id)
    return render(request, 'recipe.html', {
        'recipe': currect_recipe,
        'username': auth.get_user(request)
    })

def send_comment(request):
    username = auth.get_user(request)
    if username:
        current_recipe = Recipe.objects.get(pk=request.POST['recipe_id'])
        new_comment = Comment(comment_author=username,
                              comment_recipe=current_recipe,
                              comment_text=request.POST['comment'])
        new_comment.save()
        return redirect('/recipe/{0}'.format(request.POST['recipe_id']))
    else:
        return HttpResponse('Unauthorized', status=401)

def user_page(request, user_id):
    current_user = User.objects.get(pk=user_id)
    return render(request, 'user_page.html', {
        'user': current_user,
        'username': auth.get_user(request)
    })

def tags(request):
    all_tags = Tag.objects.all()
    return render(request, 'tags.html', {
        'tags': all_tags,
        'username': auth.get_user(request)
    })

def tag(request, tag_id):
    current_tag = Tag.objects.get(pk=tag_id)
    recipes = current_tag.tag_recipes.all()
    return render(request, 'list.html', {
        'recipes': recipes,
        'tag': current_tag,
        'username': auth.get_user(request)
    })


def most_commented(request):
    recipes = most_commented_recipes()
    return render(request, 'list.html', {
        'recipes': recipes,
        'mostcommented': True,
        'username': auth.get_user(request)
    })

def by_rating(request):
    recipes_by_rating = Recipe.objects.raw('''
        with ratings as (
          SELECT DISTINCT
            r.id,
            case when avg(g.grade_stars) is null
              then 0
              else avg(g.grade_stars)
            end rating
          FROM rcps_recipe r
            left JOIN rcps_grade g ON r.id = g.grade_recipe_id
          group by r.id
        ) select rec.*
          from rcps_recipe rec
            join ratings rat on rec.id = rat.id
          ORDER BY rating DESC
    ''')
    return render(request, 'list.html', {
        'recipes': recipes_by_rating,
        'username': auth.get_user(request)
    })

def get_rating(request):
    res = Grade.objects.filter(grade_recipe=request.GET['id']).aggregate(avg=Avg('grade_stars'))
    if res['avg'] == None:
        return JsonResponse({'rating': 0})
    return JsonResponse({'rating': res['avg']})

def add_rating(request):
    rec = Recipe.objects.get(pk=request.GET['id'])
    value = request.GET['val']
    user = auth.get_user(request)
    gr, created = Grade.objects.get_or_create(grader=user, grade_recipe=rec)
    gr.grade_stars = value
    gr.save()
    return JsonResponse({'status': 'ok'})

def add_favourite(request):
    rec = Recipe.objects.get(pk=request.GET['id'])
    user = auth.get_user(request)
    if Grade.objects.filter(grader=user, grade_recipe=rec).exists():
        gr = Grade.objects.get(grader=user, grade_recipe=rec)
        gr.grade_favorite = not gr.grade_favorite
        gr.save()
    else:
        gr = Grade.objects.create(grader=user, grade_recipe=rec, grade_favorite=True)
    return JsonResponse({'status': 'ok'})

def check_favourite(request):
    rec = Recipe.objects.get(pk=request.GET['id'])
    user = auth.get_user(request)
    if Grade.objects.filter(grader=user, grade_recipe=rec).exists():
        gr = Grade.objects.get(grader=user, grade_recipe=rec)
        return JsonResponse({'fav': gr.grade_favorite})
    else:
        return JsonResponse({'fav': False})

def favourite(request):
    user = auth.get_user(request)
    favourite_recipes = Recipe.objects.raw('''
        select r.*
        from (select * from auth_user where id = {user_id}) u
        join rcps_grade g on u.id = g.grader_id
        join rcps_recipe r on g.grade_recipe_id = r.id
        where g.grade_favorite = true
        order by g.grade_stars
    '''.format(user_id=user.id))
    return render(request, 'list.html', {
        'recipes': favourite_recipes,
        'username': auth.get_user(request)
    })

def equipment(request):
    eqs = Equipment.objects.annotate(rec_num=Count('equipment_recipes')).order_by('-rec_num')
    return render(request, 'equipment.html', {
        'equipments': eqs,
        'username': auth.get_user(request)
    })

def by_equipment(request, equipment_id):
    eq = Equipment.objects.get(pk=equipment_id)
    recipes = eq.equipment_recipes.all()
    return render(request, 'list.html', {
        'recipes': recipes,
        'equipments': [eq],
        'eia': True,
        'username': auth.get_user(request)
    })