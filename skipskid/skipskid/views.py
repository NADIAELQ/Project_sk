from django.shortcuts import render

def shipping_home(request):
    # You can pass additional context to the template if needed
    context = {}
    return render(request, 'shipping_home.html', context)
