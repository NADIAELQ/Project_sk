from django.shortcuts import render

def shipping_home(request):

    context = {}
    return render(request, 'shipping_home.html', context)
