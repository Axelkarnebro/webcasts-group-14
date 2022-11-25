from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from main.forms import ContactForm
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