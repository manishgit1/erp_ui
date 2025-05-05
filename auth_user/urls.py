from django.urls import path
from .views import LoginView, RegisterView, Logout

urlpatterns = [
      path('user/login', LoginView.as_view(), name='user-login-create'),
      path('user/register', RegisterView.as_view(), name='user-register'),
      path('user/register/create', RegisterView.as_view(), name='user-register-create'),

      path('', LoginView.as_view(), name='user-login'),
      path('user/logout', Logout.as_view(), name='user-logout'),


]