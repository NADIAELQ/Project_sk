from django.shortcuts import render

def shipping_home(request):
    context = {}
    return render(request, 'shipping_home.html', context)

def carrier_home(request):
    context = {}
    return render(request, 'carrier_home.html', context)
