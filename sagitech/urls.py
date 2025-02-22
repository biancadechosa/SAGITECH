from django.urls import path
from .views import LandingPage, LoginPage, SignupPage 

urlpatterns = [
    path('', LandingPage, name='index'),
    path('login/', LoginPage, name='login'),
    path('signup/', SignupPage, name='signup'),
]
