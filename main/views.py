from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from article.models import Upcoming_Event

from main.forms import ContactForm, RegisterForm
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import PasswordResetForm
from django.views.generic import CreateView
from django.views import View

from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

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

def upcoming_events(request):
    context = {
        'title': 'Upcoming Events',
        'events': Upcoming_Event.objects.all().order_by('date')
    }
    return render(request, 'pages/upcoming_events.html', context)

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

def reset_password(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "registration/resetpasswordemail.txt"
                    c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'axel.karnebro@gmail.com' , [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("/reset_password_done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="registration/password_reset.html", context={"password_reset_form":password_reset_form})


def check_username(request):
    if request.method == 'POST':
        name = request.POST['username']

        user = User.objects.filter(Q(username=name))
        if user.exists():
            return HttpResponse("This name is taken!")
        else:
            return HttpResponse("This name is free!")
        
