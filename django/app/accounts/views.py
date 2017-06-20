from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

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
