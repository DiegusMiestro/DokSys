from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Document, Keyword

@login_required
def index(request):
    context = {
        'layout': 'materialize/index.html',
        'documents_latest': Document.objects.order_by('-pub_date')[:5],
        'keyword_latest': Keyword.objects.order_by('-pub_date')[:5],
        'breadcumb': [
            {'title' : 'Documentos', 'url': 'documents/'}
        ]
    }
    return render(request, 'index.html', context)

@login_required
def latest(request):
    context = {
        'layout': 'materialize/latest.html',
        'latest': Document.objects.order_by('-pub_date'),
        'breadcumb': [
            {'title' : 'Documentos', 'url': 'documents/'},
            {'title' : 'Recentes', 'url': 'documents/latest/'}
        ]
    }
    return render(request, 'index.html', context)

@login_required
def detail(request, id):
    context = {
        'layout': 'materialize/index.html',
        'document': get_object_or_404(Document, pk=id)
    }
    return render(request, 'detail.html', context)

@login_required
def add(request):
    keywords = Keyword.objects.all()
    context = {
        'layout': 'materialize/index.html',
        'keywords': keywords
    }
    return render(request, 'add.html', context)
