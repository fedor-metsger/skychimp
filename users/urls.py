
from django.urls import path

from users.views import LoginView, LogoutView, UserRegisterView, UserUpdateView, UserPasswordView, UserActivationView

app_name = 'user'

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('<int:pk>/activation/', UserActivationView.as_view(), name='activation'),
    path('<int:pk>/update/', UserUpdateView.as_view(), name='update'),
    path('<int:pk>/password/', UserPasswordView.as_view(), name='password')
]