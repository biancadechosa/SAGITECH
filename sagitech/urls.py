from django.urls import path
from .views import LandingPage, LoginPage, SignupPage, DashboardPage, LogoutView 

urlpatterns = [
    path('', LandingPage, name='index'),
    path('login/', LoginPage, name='login'),
    path('signup/', SignupPage, name='signup'), 
    path('dashboard/', DashboardPage, name='dashboard'),  
    path('logout/', LogoutView, name='logout'),
]
