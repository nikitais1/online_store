from django.urls import path
from users.apps import UsersConfig
from django.contrib.auth.views import LoginView, LogoutView

from users.views import RegisterView, ProfileView, VerifyEmailView, CustomPasswordResetView

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(template_name='users/register.html'), name='register'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('verify_email/<str:uid>/<str:token>/', VerifyEmailView.as_view(), name='verify_email'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
]
