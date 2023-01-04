from django.urls import path, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetCompleteView, PasswordResetDoneView, PasswordResetConfirmView

from .views import home, about_us, contact_us, thank_you_contact_us, Register, upcoming_events, reset_password

app_name = 'main'

urlpatterns = [
    path('', home, name='home'),
    path('about-us',about_us, name='about_us'),
    path('upcoming-events', upcoming_events, name='upcoming_events'),
    path('contact-us', contact_us, name='contact_us'),
    path('thank-you-contact-us', thank_you_contact_us, name='thank_you_contact_us'),
    path('register/', Register.as_view(), name='register_user'),
    path('login/', LoginView.as_view(template_name='pages/login_user.html'), name='login_user'),
    path('logout/', LogoutView.as_view(), name='logout_user'),
    path('reset-password-done', PasswordResetDoneView.as_view(template_name='pages/reset_password_done.html'), name='reset_password_done'),
    path('reset-password-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='pages/reset_password_confirm.html', success_url=reverse_lazy('main:reset_password_complete')), name='reset_password_confirm'),
    path('reset-password-complete', PasswordResetCompleteView.as_view(template_name='pages/reset_password_complete.html'), name='reset_password_complete'),
    path('reset-password', reset_password, name='reset_password')
]
