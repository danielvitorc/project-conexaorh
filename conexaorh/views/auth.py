from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            # Redirecionamento de acordo com o tipo de usuário
            if user.user_type == 'gestor':
                return redirect('gestor_page')
            elif user.user_type == 'diretor':
                return redirect('diretor_page')
            elif user.user_type == 'presidente':
                return redirect('presidente_page')
            elif user.user_type == 'rh':
                return redirect('rh_page')
            elif user.user_type == 'complice':
                return redirect('complice_page')
            else:
                return redirect('home')
    else:
        form = AuthenticationForm(request)
    return render(request, 'conexaorh/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')