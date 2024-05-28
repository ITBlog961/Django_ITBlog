from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator
from django.http import HttpResponse 
from django.shortcuts import render, redirect
from blog.models import *
from .forms import *

menu = [{'title': 'Про сайт', 'url_name': 'about'},
        {'title': 'Додати статтю', 'url_name': 'add_page'},
        {'title': "Зворотній зв'язок", 'url_name': 'contact'},
        ]

def index(request):
    posts = Articles.objects.filter(is_published=True)
    cats = Category.objects.all()
    paginator = Paginator(posts, 3)  

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'cats': cats,
        'menu': get_menu(request),
        'title': 'Головна',
        'cat_selected': 0,
        }
    return render(request, 'blog/index_.html', context=context)

def logout_view(request):
    logout(request)
    return redirect('home')

def about(request):
    cats = Category.objects.all()
    context = {
        'menu': get_menu(request),
        'cats': cats,
        'title': 'Про сайт',
        'cat_selected': 0,
        }
    return render(request, 'blog/about.html', context=context)

def addpage(request):
    cats = Category.objects.all()
    if request.user.is_authenticated:
        if request.method == "POST":
            form = AddPostForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('home')
        else:
            form = AddPostForm()
        return render(request, 'blog/add_page.html', {'form': form, 'menu': get_menu(request), 'title': 'Додати статтю', 'cat_selected': 0, 'cats': cats,})
    else:
        return render(request, 'blog/add_page_error.html', {'menu': get_menu(request), 'title': 'Додати статтю', 'cat_selected': 0, 'cats': cats,})

def contact(request):
    cats = Category.objects.all()
    context = {
        'cats': cats,
        'menu': get_menu(request),
        'title': "Зворотній зв'язок",
        'cat_selected': 0,
        }
    return render(request, 'blog/contact.html', context=context)

def show_post(request, post_id):
    post = Articles.objects.get(pk=post_id)
    cats = Category.objects.all()
    context = {
        'article': post,
        'cats': cats,
        'menu': get_menu(request),
        'title': post.title,
        'cat_selected': post.cat_id,
        }
    return render(request, 'blog/article_details.html', context=context)

def show_category(request, cat_id):
    posts = Articles.objects.filter(cat_id=cat_id, is_published = True)
    cats = Category.objects.all()
    cat = Category.objects.get(pk=cat_id)
    paginator = Paginator(posts, 3)  

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'cats': cats,
        'menu': get_menu(request),
        'title': cat,
        'cat_selected': cat_id,
        }
    return render(request, 'blog/index_.html', context=context)


def login_or_register(request):
    cats = Category.objects.all()
    if request.method == 'POST':
        if 'login' in request.POST:
            login_form = AuthenticationForm(request, data=request.POST)
            register_form = RegisterForm()
            if login_form.is_valid():
                username = login_form.cleaned_data.get('username')
                password = login_form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home')
        elif 'register' in request.POST:
            register_form = RegisterForm(request.POST)
            login_form = AuthenticationForm()
            if register_form.is_valid():
                register_form.save()
                username = register_form.cleaned_data.get('username')
                password = register_form.cleaned_data.get('password1')
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect('home')
    else:
        login_form = AuthenticationForm()
        register_form = RegisterForm()
    
    return render(request, 'blog/login_or_register.html', {'cats': cats, 'cat_selected': 0,
                                                           'login_form': login_form, 'register_form': register_form,
                                                           'menu': get_menu(request), 'title': 'Увійти/Реєстрація'})

def get_menu(request):
    if request.user.is_authenticated:
        return menu + [{'title': 'Вийти', 'url_name': 'logout'}]
    else:
        return menu + [{'title': 'Увійти/Реєстрація', 'url_name': 'login_or_register'}]
