from django.shortcuts import render

def shipping_home(request):
    context = {}
    return render(request, 'front/shipping_home.html', context)

def carrier_home(request):
    context = {}
    return render(request, 'front/carrier_home.html', context)

def why_silyatrans(request):
    return render(request, 'front/why_silyatrans.html')

def carrier_page(request):
    context = {}
    return render(request, 'front/main_carrier.html', context)
