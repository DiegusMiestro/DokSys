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
        'documentations': Document.objects.order_by('-pub_date'),
        'breadcumb': [
            {'title' : 'Documentações', 'url': 'documentations/'}
        ]
    }
    return render(request, 'index.html', context)

@login_required
def latest(request):
    context = {
        'layout': 'materialize/latest.html',
        'documents_latest': Document.objects.order_by('-pub_date')[:5],
        'keyword_latest': Keyword.objects.order_by('-pub_date')[:5],
        'breadcumb': [
            {'title' : 'Documentações', 'url': 'documentations/'},
            {'title' : 'Recentes', 'url': 'documentations/latest/'}
        ]
    }
    return render(request, 'index.html', context)

@login_required
def detail(request, id):
    document = get_object_or_404(Document, pk=id)
    context = {
        'layout': 'materialize/index.html',
        'document': document,
        'breadcumb': [
            {'title' : 'Documentações', 'url': 'documentations/'},
            {'title' : document.title, 'url': 'documentations/' + str(document.id) +'/'}
        ]
    }
    return render(request, 'detail.html', context)

@login_required
def add(request):
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
    return render(request, 'add.html', context)

@login_required
def edit(request, id):
    document = get_object_or_404(Document, pk=id)
    if request.method == "POST":
        Document.objects.filter(pk=id).update(title=request.POST.get('title'), url=urlize(request.POST.get('title')), content=request.POST.get('content'))
        pub_date=datetime.datetime.now()
        keywords_old = list(document.keywords.all())
        keywords_new = []
        for word in request.POST.get('keywords').split(","):
            word_title = word.strip()
            word_url = urlize(word)
            try:
                keyword = Keyword.objects.get(url=word_url)
            except ObjectDoesNotExist:
                keyword = Keyword.objects.create(title=word_title, url=word_url, pub_date=pub_date)
            try:
                keywords_old.remove(keyword)
            except Exception as e:
                document.keywords.add(keyword)
                print('Add Keyword to Documetation')
            keywords_new.append(keyword)
            # import pdb; pdb.set_trace()
            # Falta remover as Keywords que não quer mais
            # No momento apenas adiciona novas, independentes de já existirem ou não.
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
    return render(request, 'edit.html', context)
