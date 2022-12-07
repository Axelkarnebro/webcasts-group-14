from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import home, about_us, contact_us, thank_you_contact_us, login_user, logout_user, Register

app_name = 'main'

urlpatterns = [
    path('', home, name='home'),
    path('about-us',about_us, name='about_us'),
    path('contact-us', contact_us, name='contact_us'),
    path('thank-you-contact-us', thank_you_contact_us, name='thank_you_contact_us'),
    path('register/', Register.as_view(), name='register_user'),
    path('login/', LoginView.as_view(template_name='pages/login_user.html'), name='login_user'),
    path('logout/', LogoutView.as_view(), name='logout_user')
]
