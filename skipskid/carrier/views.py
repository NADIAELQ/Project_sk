# # from django.shortcuts import render, redirect
# # from django.contrib.auth import authenticate, login, logout
# # from django.http import *
# # from django.views.generic import TemplateView
# # from django.conf import settings

# # class LoginView(request):
# #     if request.method == 'POST':
# #         username = request.POST["username"]
# #         password = request.POST["password"]
# #         user = authenticate(request, username=username, password=password)
# #         if user is not None:
# #             login(request, user)
# #             return redirect('home')
# #     return render(request, 'templates/front/login.html')

# from django.shortcuts import render, redirect  # Importation de fonctions pour rendre les modèles et rediriger les utilisateurs
# from django.contrib.auth.forms import UserCreationForm  # Importation du formulaire de création d'utilisateur fourni par Django
# from django.contrib.auth.decorators import login_required  # Décorateur pour limiter l'accès aux utilisateurs connectés uniquement
# from django.contrib import messages  # Module pour afficher des messages à l'utilisateur
# from .models import Carrier  # Importation du modèle Carrier défini dans le même dossier que ce fichier de vue

# def register(request):
#     if request.method == 'POST':  # Vérifie si la requête est de type POST (l'utilisateur a soumis le formulaire)
#         form = UserCreationForm(request.POST)  # Crée une instance du formulaire de création d'utilisateur avec les données POST
#         if form.is_valid():  # Vérifie si le formulaire est valide (tous les champs sont correctement remplis)
#             form.save()  # Enregistre l'utilisateur dans la base de données
#             messages.success(request, 'Your account has been created! You are now able to log in')  # Affiche un message de succès à l'utilisateur
#             return redirect('login')  # Redirige l'utilisateur vers la page de connexion
#     else:
#         form = UserCreationForm()  # Crée une instance vide du formulaire de création d'utilisateur pour affichage
#     return render(request, 'register.html', {'form': form})  # Rend la page de création de compte avec le formulaire

# @login_required  # Limite l'accès à cette vue aux utilisateurs connectés uniquement
# def profile(request):
#     user = request.user  # Récupère l'utilisateur actuel
#     carrier = Carrier.objects.get(email=user.email)  # Récupère le profil du transporteur associé à l'utilisateur
#     context = {
#         'carrier': carrier  # Contexte contenant les informations du transporteur pour être affichées dans le modèle de profil
#     }
#     return render(request, 'profile.html', context)  # Rend la page de profil avec les informations du transporteur


from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm 
from .form import CustomUserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def inscription(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('connexion')
    else:
        form = CustomUserCreationForm()
    return render(request, 'inscription.html', {'form': form})

def connexion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('acceuil')
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
    return render(request, 'connexion.html')

@login_required
def acceuil(request):
    return render(request, 'acceuil.html')

def deconnexion(request):
    logout(request)
    return redirect('connexion')
