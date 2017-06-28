from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def login(request):
    msg = ''
    if request.method == "POST":
        user = authenticate(username=request.POST["username"], password=request.POST["password"])
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                msg = 'Login Realizado com sucesso!'
                return redirect('/')
            else:
                msg = "A conta está desabilitada."
        else:
            msg = "Usuário ou Senha estão incorretos."
    context = {
        'layout': 'materialize/index.html',
        'msg': msg
    }
    return render(request, 'login.html', context)

def logout(request):
    auth_logout(request)
    return redirect('/')

@login_required
def users(request):
    if not request.user.is_superuser:
        return redirect('/accounts/profile/')
    context = {
        'layout': 'materialize/index.html',
        'users': User.objects.order_by('first_name'),
        'breadcumb': [
            {'title' : 'Contas', 'url': 'accounts/'}
        ]
    }
    return render(request, 'users.html', context)

@login_required
def detail(request, id):
    if not request.user.is_superuser:
        return redirect('/accounts/profile/')
    user = get_object_or_404(User, pk=id)
    context = {
        'layout': 'materialize/index.html',
        'user': user,
        'breadcumb': [
            {'title' : 'Contas', 'url': 'accounts/'},
            {'title' : 'Perfis', 'url': 'accounts/users/'},
            {'title' : user.first_name + ' ' + user.last_name, 'url': 'accounts/users/' + str(user.id) + '/'},
        ]
    }
    return render(request, 'detail.html', context)

@login_required
def add(request):
    if not request.user.is_superuser:
        return redirect('/accounts/profile/')
    if request.method == "POST":
        user = User.objects.create_user(request.POST.get("username"), request.POST.get("email"), request.POST.get("password"))
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        if(request.POST.get('is_superuser')):
            user.is_superuser = True
        user.save()
        return redirect('/accounts/users/')
    context = {
        'layout': 'materialize/index.html',
        'breadcumb': [
            {'title' : 'Contas', 'url': 'accounts/'},
            {'title' : 'Perfis', 'url': 'accounts/users/'},
            {'title' : 'Adicionar', 'url': 'accounts/users/add/'},
        ]
    }
    return render(request, 'add.html', context)

@login_required
def edit(request, id):
    if not request.user.is_superuser:
        return redirect('/accounts/profile/')
    user = User.objects.get(pk=id)
    if request.method == "POST":
        User.objects.filter(pk=id).update(first_name=request.POST.get("first_name"),last_name=request.POST.get("last_name"),email=request.POST.get("email"), username=request.POST.get("username"))
        user = User.objects.get(pk=id)
        if request.POST.get("password"):
            user.set_password(request.POST.get("password"))
        if(request.POST.get('is_superuser')):
            user.is_superuser = True
        else:
            user.is_superuser = False
        user.save()
        return redirect('/accounts/users/')
    context = {
        'layout': 'materialize/index.html',
        'user': user,
        'breadcumb': [
            {'title' : 'Contas', 'url': 'accounts/'},
            {'title' : 'Perfis', 'url': 'accounts/users/'},
            {'title' : user.first_name + ' ' + user.last_name, 'url': 'accounts/users/' + str(user.id) + '/'},
            {'title' : 'Editar', 'url': 'accounts/users/' + str(user.id) + '/edit/'},
        ]
    }
    return render(request, 'edit.html', context)

@login_required
def delete(request, id):
    if not request.user.is_superuser:
        return redirect('/accounts/profile/')
    user = User.objects.get(pk=id)
    user.delete()
    return redirect('/accounts/users/')

@login_required
def active(request, id):
    if not request.user.is_superuser:
        return redirect('/accounts/profile/')
    user = User.objects.get(pk=id)
    user.is_active = True
    user.save()
    return redirect('/accounts/users/')

@login_required
def desactive(request, id):
    if not request.user.is_superuser:
        return redirect('/accounts/profile/')
    user = User.objects.get(pk=id)
    user.is_active = False
    user.save()
    return redirect('/accounts/users/')

@login_required
def profile(request):
    user = get_object_or_404(User, pk=request.user.id)
    context = {
        'layout': 'materialize/index.html',
        'user': user,
        'breadcumb': [
            {'title' : 'Contas', 'url': 'accounts/'},
            {'title' : 'Perfis', 'url': 'accounts/users/'},
            {'title' : user.first_name + ' ' + user.last_name, 'url': 'accounts/users/' + str(user.id) + '/'},
        ]
    }
    return render(request, 'profile.html', context)

@login_required
def profile_edit(request):
    if request.method == "POST":
        User.objects.filter(pk=request.user.id).update(first_name=request.POST.get("first_name"),last_name=request.POST.get("last_name"),email=request.POST.get("email"), username=request.POST.get("username"))
        user = User.objects.get(pk=request.user.id)
        if request.POST.get("password"):
            user.set_password(request.POST.get("password"))
        if(request.POST.get('is_superuser')):
            user.is_superuser = True
        else:
            user.is_superuser = False
        user.save()
        return redirect('/accounts/users/')
    user = User.objects.get(pk=request.user.id)
    context = {
        'layout': 'materialize/index.html',
        'user': user,
        'breadcumb': [
            {'title' : 'Contas', 'url': 'accounts/'},
            {'title' : 'Perfis', 'url': 'accounts/users/'},
            {'title' : user.first_name + ' ' + user.last_name, 'url': 'accounts/users/' + str(user.id) + '/'},
            {'title' : 'Editar', 'url': 'accounts/users/' + str(user.id) + '/edit/'},
        ]
    }
    return render(request, 'profile_edit.html', context)
