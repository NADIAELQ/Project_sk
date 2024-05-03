from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm 
from .form import ShipperForm, ShipperAddressForm
from .models import Shipper
from .auth_backend import CustomAuthBackend
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def signup(request):
    if request.method == 'POST':
        user_form = ShipperForm(request.POST)
        address_form = ShipperAddressForm(request.POST)
        if user_form.is_valid() and address_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            address = address_form.save(commit=False)
            address.shipper = user
            address.save()
            # Redirect to login page after signup
            return redirect('Shipperlogin')
    else:
        user_form = ShipperForm()
        address_form = ShipperAddressForm()
    return render(request, 'shippersignup.html', {'user_form': user_form, 'address_form': address_form})

def Shipperlogin(request):
    if request.method == 'POST':
        email = request.POST['email_address']
        password = request.POST['password']
        # user = authenticate(request, username=username, password=password)
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('Shipperhome')
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
    return render(request, 'shipperlogin.html')

@login_required
def home(request):
    return render(request, 'shipperhome.html')

def logout(request):
    auth_logout(request)  # Utilisez la fonction auth_logout de Django pour éviter le conflit
    return redirect('Shipperlogin')  # Rediriger vers la page de connexion après la déconnexion

def beforesignup(request):
    return render(request, 'beforesignup.html')


def accountsettings(request):
    email = request.user.email
    context = {
        'email': email
    }

    return render(request, 'accountsettings.html', context)


