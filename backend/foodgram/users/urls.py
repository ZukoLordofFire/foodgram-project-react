from django.contrib.auth.views import (
    LogoutView,
    LoginView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    PasswordChangeView,
    PasswordChangeDoneView,
)
from django.urls import path

from users.views import TokenView, RegisterView

app_name = 'authentication'

urlpatterns = [
    path('auth/token/', TokenView.as_view(), name='get_token'),
    path('auth/signup/', RegisterView.as_view(), name='create_user'),
    path('logout/',
         LogoutView.as_view(template_name='users/logged_out.html'),
         name='logout'),
    path('login/',
         LoginView.as_view(template_name='users/login.html'),
         name='login'
         ),
    path('password_reset/',
         PasswordResetView.as_view(
            template_name='users/password_reset_form.html'),
         name='password_reset'
         ),
    path('password_reset/done/',
         PasswordResetDoneView.as_view(
            template_name='users/password_reset_done.html'),
         name='password_reset_done',
         ),
    path('reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
            template_name='users/password_reset_confirm.html'),
         name='auth/reset/<uidb64>/<toke>'
         ),
    path('reset/done/',
         PasswordResetCompleteView.as_view(
            template_name='users/password_reset_complete.html'),
         name='reset_done'
         ),
    path('password_change/',
         PasswordChangeView.as_view(
            template_name='users/password_change_form.html'),
         name='password_change'
         ),
    path('password_change_done/',
         PasswordChangeDoneView.as_view(
            template_name='users/password_change_done.html'),
         name='change_done'
         ),
]
