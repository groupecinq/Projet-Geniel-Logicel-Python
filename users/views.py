from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, messages
from django.contrib.auth.decorators import login_required, permission_required
from .models import Profil

def connexion(request):
  if request.method == 'POST':
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        messages.success(request, f'Bienvenue, {user.username} !')
        return redirect('dashboard:accueil')
    else:
             messages.error(request, 'Identifiant ou mot de passe incorrect.')
  return render(request, 'users/login.html')
  
@login_required
@permission_required('users.change_profil')
def modifier_role(request, user_id):
    profil = get_object_or_404(Profil, user_id=user_id)
    if request.method == 'POST':
        nouveau_role = request.POST.get('role')
        profil.role = nouveau_role
        profil.save()
        messages.success(request, 'Rôle mis à jour avec succès.')
        return redirect('users:liste')
    return render(request, 'users/modifier_role.html', {'profil': profil})
