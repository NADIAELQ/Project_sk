from django.shortcuts import render

def shipping_home(request):
<<<<<<< HEAD
=======
    # You can pass additional context to the template if needed
>>>>>>> d79ccde41d39efea4e165b37d6f6e1ee63a726fc
    context = {}
    return render(request, 'shipping_home.html', context)
