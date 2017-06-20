from django.db import models
from django.contrib.auth.models import User

class Keyword(models.Model):
    title = models.CharField(max_length=30, unique=True)
    url = models.CharField(max_length=200, unique=True)
    pub_date = models.DateTimeField('date published')

class Document(models.Model):
    title = models.CharField(max_length=200, unique=True)
    url = models.URLField(max_length=200, unique=True)
    content = models.TextField()
    keywords = models.ManyToManyField(Keyword)
    user = models.ForeignKey(User)
    pub_date = models.DateTimeField('date published')

class History(models.Model):
    document = models.ForeignKey(Document)
    action = models.CharField(max_length=32)
    user = models.ForeignKey(User)
    pub_date = models.DateTimeField('date published')
