from django.contrib.auth.decorators import login_required
from django.contrib.sites import requests
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
import requests

from .forms import AddPostForm, UploadFileForm
from .models import Packagedb, Category, UploadFiles

# Create your views here.


menu = [
    {'title': 'Device IN/OUT', 'url_name': 'about'},
    {'title': 'Add page', 'url_name': 'addpage'},
    {'title': 'Contact', 'url_name': 'contact'},
]

data_db = [
    {'id': 1, 'title': 'first article', 'content': 'text of first article', 'is_published': True},
    {'id': 2, 'title': 'second article', 'content': 'text of second article', 'is_published': False},
    {'id': 3, 'title': 'third article', 'content': 'text of third article', 'is_published': True}
]


def index(request):
    posts = Packagedb.published.all()
    data = {
        'title': 'index page',
        'menu': menu,
        'posts': posts,
        'cat_selected': 0,
    }

    return render(request, 'index.html', context=data)


def handle_uploaded_file(f):
    with open(f"uploads/{f.name}", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


@login_required
def about(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            fp = UploadFiles(file=form.cleaned_data['file'])
            fp.save()

    else:
        form = UploadFileForm()

    return render(request, 'about.html', {'title': 'about', 'form': form})


def show_post(request, post_slug):
    post = get_object_or_404(Packagedb, slug=post_slug)
    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'cat_selected': 1,
    }
    return render(request, 'post.html', context=data)


@login_required
def add_page(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            # #print(form.cleaned_data)
            # try:
            #     Packagedb.objects.create(**form.cleaned_data)
            #     return redirect('home')
            # except:
            #     form.add_error(None, 'Error adding post')
            form.save()
            return redirect('home')
    else:
        form = AddPostForm()

    data = {
        'title': 'add page',
        'menu': menu,
        'form': form
    }
    return render(request, 'add_page.html', data)


def contact(request):
    return HttpResponse("Contact <br> page ")


def login(request):
    return HttpResponse("Login page")


def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Packagedb.published.filter(cat_id=category.pk)
    data = {
        'title': f'Рубрика: {category.name}',
        'menu': menu,
        'posts': posts,
        'cat_selected': category.pk,
    }

    return render(request, 'index.html', context=data)


def send_command_to_pico(request):
    pico_url = 'http://192.168.31.40:82/?relay1=on'

    response = requests.get(pico_url)
    if response.status_code == 200:
        return HttpResponse('Command successfully sent to Raspberry Pi Pico')
    else:
        return HttpResponse('Error sending the command to Raspberry Pi Pico', status=500)
