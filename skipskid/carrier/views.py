from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm 
from .form import CarrierForm
from .auth_backend import CustomAuthBackend
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .form import CarrierForm, CarrierAddressForm

def signup(request):
    if request.method == 'POST':
        user_form = CarrierForm(request.POST)
        address_form = CarrierAddressForm(request.POST)
        if user_form.is_valid() and address_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            address = address_form.save(commit=False)
            address.carrier = user
            address.save()
            # Redirect to login page after signup
            return redirect('login')
    else:
        user_form = CarrierForm()
        address_form = CarrierAddressForm()
    return render(request, 'signup.html', {'user_form': user_form, 'address_form': address_form})

def Carrierlogin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        # user = authenticate(request, username=username, password=password)
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
    return render(request, 'login.html')

@login_required
def home(request):
    return render(request, 'home.html')

def logout(request):
    auth_logout(request)  # Utilisez la fonction auth_logout de Django pour éviter le conflit
    return redirect('login')  # Rediriger vers la page de connexion après la déconnexion

def beforesignup(request):
    return render(request, 'beforesignup.html')


def accountsettings(request):
    email = request.user.email
    context = {
        'email': email
    }

    return render(request, 'accountsettings.html', context)


def homepage(request):
    return render(request, 'homepage.html')
