from django.urls import path

from .views import home, about_us, contact_us, thank_you_contact_us, register_user, login_user, logout_user

app_name = 'main'

urlpatterns = [
    path('', home, name='home'),
    path('about-us',about_us, name='about_us'),
    path('contact-us', contact_us, name='contact_us'),
    path('thank-you-contact-us', thank_you_contact_us, name='thank_you_contact_us'),
    path('register/', register_user, name='register_user'),
    path('login/', login_user, name='login_user'),
    path('logout/', logout_user, name='logout_user')
]
