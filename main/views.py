from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse

from main.forms import ContactForm, RegisterForm
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, logout, authenticate
from django.views.generic import CreateView
from django.views import View
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

def contact_us(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ContactForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender = form.cleaned_data['sender']
            cc_myself = form.cleaned_data['cc_myself']

            print(subject, message, sender, cc_myself)

            return HttpResponseRedirect(reverse('main:thank_you_contact_us'))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ContactForm()

    return render(request, 'pages/contact_us.html', {'form': form})

def thank_you_contact_us(request):
    context = {
        'title': 'Among Us!!!!!!!!!!!!!!!!!!!!'
    }
    return render(request, 'pages/thank_you_contact_us.html', context)

# def register_user(request):
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)

#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']

#             print(username, password)
#             try:
#                 user = User.objects.create_user(username, 'lmao@email.com',password)
#             except:
#                 # Send back to register page in case exception made when creating user
#                 return render(request, 'pages/register_user.html',
#                 # Also give context
#                 {'form': form, 'nameError': 'Sorry, username already in use probably ://'})
                
#             user.user_permissions.clear()

#             #author_group = Group.objects.get(name='authors')
#             #author_group.user_set.add(user.id)
            
#             return HttpResponseRedirect(reverse('main:thank_you_contact_us'))
        
#         else:
#             return render(request, 'pages/register_user.html', {'form': form})

#     else:
#         form = RegisterForm()
#     return render(request, 'pages/register_user.html', {'form': form})

class Register(View):
    def get(self, request):
        context = {
            'form':RegisterForm
        }
        return render(request, 'pages/register_user.html', context)

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        context = {
            'form':form
        }
        return render(request, 'pages/register_user.html', context)

def login_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            print(username, password)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('main:thank_you_contact_us'))
            else:
                print("u done fucked up now!")
            
    else:
        form = RegisterForm()
    return render(request, 'pages/login_user.html', {'form': form})

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')