from django.shortcuts import render

# Create your views here.
def home(request):
    context = {
        'title': 'Welcome to the best Django Tutorials'
    }
    return render(request, 'pages/home.html', context)

def about_us(request):
    context = {
        'title': 'Among Us'
    }
    return render(request, 'pages/about_us.html', context)
