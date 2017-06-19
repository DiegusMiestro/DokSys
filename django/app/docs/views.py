from django.shortcuts import render, get_object_or_404
from .models import Document, Keyword

def index(request):
    context = {'latest': Document.objects.order_by('-pub_date')[:5]}
    return render(request, 'index.html', context)

def detail(request, id):
    document = get_object_or_404(Document, pk=id)
    return render(request, 'detail.html', {'document': document})

def add(request):
    keyword = Keyword.objects.all()
    return render(request, 'add.html', {})
