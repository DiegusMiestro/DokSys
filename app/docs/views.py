from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Document, Keyword
import datetime
from unicodedata import normalize
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

def urlize(txt):
    return normalize('NFKD', txt).encode('ASCII','ignore').decode('ASCII').lower().strip().replace(' ', '-')

@login_required
def index(request):
    context = {
        'layout': 'materialize/index.html',
        'documentations': Document.objects.order_by('-pub_date')[:5],
        'keywords': Keyword.objects.order_by('-pub_date')[:5],
        'breadcumb': [
            {'title' : 'Dashboard', 'url': '/'}
        ]
    }
    return render(request, 'index.html', context)


@login_required
def latest(request):
    qtde = 5
    context = {
        'layout': 'materialize/index.html',
        'documentations': Document.objects.order_by('-pub_date')[:qtde],
        'keywords': Keyword.objects.order_by('-pub_date')[:qtde],
        'breadcumb': [
            {'title' : 'Atualizações Recentes', 'url': 'latest/'}
        ]
    }
    return render(request, 'latest.html', context)

@login_required
def docs(request):
    context = {
        'layout': 'materialize/index.html',
        'documentations': Document.objects.order_by('-pub_date'),
        'breadcumb': [
            {'title' : 'Documentações', 'url': 'documentations/'}
        ]
    }
    return render(request, 'documentations/all.html', context)

@login_required
def doc_detail(request, id):
    document = get_object_or_404(Document, pk=id)
    context = {
        'layout': 'materialize/index.html',
        'document': document,
        'breadcumb': [
            {'title' : 'Documentações', 'url': 'documentations/'},
            {'title' : document.title, 'url': 'documentations/' + str(document.id) +'/'}
        ]
    }
    return render(request, 'documentations/detail.html', context)

@login_required
def doc_add(request):
    if request.method == "POST":
        title = request.POST.get('title')
        url = urlize(title)
        content = request.POST.get('content')
        pub_date=datetime.datetime.now()
        try:
            doc = Document.objects.create(title=title, url=url, content=content, user=request.user, pub_date=pub_date)
        except IntegrityError:
            doc = Document.objects.get(url=url)
        for word in request.POST.get('keywords').split(","):
            word_title = word.strip()
            word_url = urlize(word)
            try:
                keyword = Keyword.objects.get(url=word_url)
            except ObjectDoesNotExist:
                keyword = Keyword.objects.create(title=word_title, url=word_url, pub_date=pub_date)
            print(keyword)
            doc.keywords.add(keyword)
        return redirect('/documentations/')
    keywords = Keyword.objects.all()
    context = {
        'layout': 'materialize/index.html',
        'keywords': keywords,
        'breadcumb': [
            {'title' : 'Documentações', 'url': 'documentations/'},
            {'title' : 'Adicionar', 'url': 'documentations/add/'},
        ]
    }
    return render(request, 'documentations/add.html', context)

@login_required
def doc_edit(request, id):
    document = get_object_or_404(Document, pk=id)
    if request.method == "POST":
        Document.objects.filter(pk=id).update(title=request.POST.get('title'), url=urlize(request.POST.get('title')), content=request.POST.get('content'))
        pub_date=datetime.datetime.now()
        keywords_del = list(document.keywords.all())
        for word in request.POST.get('keywords').split(","):
            word_title = word.strip()
            word_url = urlize(word)
            try:
                keyword = Keyword.objects.get(url=word_url)
            except ObjectDoesNotExist:
                keyword = Keyword.objects.create(title=word_title, url=word_url, pub_date=pub_date)
            try:
                keywords_del.remove(keyword)
            except Exception as e:
                document.keywords.add(keyword)
        for k2d in keywords_del:
            document.keywords.remove(k2d)
        redirect('/documentations/' + str(document.id) + '/')
    context = {
        'layout': 'materialize/index.html',
        'document': document,
        'breadcumb': [
            {'title' : 'Documentações', 'url': 'documentations/'},
            {'title' : document.title, 'url': 'documentations/' + str(document.id) +'/'},
            {'title' : 'Edição', 'url' : 'documentations/' + str(document.id) + '/edit/'}
        ]
    }
    return render(request, 'documentations/edit.html', context)

@login_required
def doc_delete(request, id):
    documentation = Document.objects.get(pk=id)
    documentation.delete()
    return redirect('/documentations/')

@login_required
def words(request):
    context = {
        'layout': 'materialize/index.html',
        'keywords': Keyword.objects.order_by('title'),
        'breadcumb': [
            {'title' : 'Palavras Chaves', 'url': 'keywords/'}
        ]
    }
    return render(request, 'keywords/all.html', context)

@login_required
def word_detail(request, id):
    keyword = get_object_or_404(Keyword, pk=id)
    context = {
        'layout': 'materialize/index.html',
        'keyword': keyword,
        'breadcumb': [
            {'title' : 'Palavras-Chaves', 'url': 'keywords/'},
            {'title' : keyword.title, 'url': 'keywords/' + str(keyword.id) +'/'}
        ]
    }
    return render(request, 'keywords/detail.html', context)

@login_required
def word_edit(request, id):
    keyword = get_object_or_404(Keyword, pk=id)
    if request.method == "POST":
        Keyword.objects.filter(pk=id).update(title=request.POST.get('title'), url=urlize(request.POST.get('title')))
        redirect('/keywords/')
    context = {
        'layout': 'materialize/index.html',
        'keyword': keyword,
        'breadcumb': [
            {'title' : 'Palavras-Chaves', 'url': 'keywords/'},
            {'title' : keyword.title, 'url': 'keywords/' + str(keyword.id) +'/'},
            {'title' : 'Edição', 'url' : 'keywords/' + str(keyword.id) + '/edit/'}
        ]
    }
    return render(request, 'keywords/edit.html', context)

@login_required
def word_delete(request, id):
    keyword = Keyword.objects.get(pk=id)
    keyword.delete()
    return redirect('/keywords/')
