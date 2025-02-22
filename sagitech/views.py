from django.shortcuts import render

def LandingPage(request):
    return render(request, 'sagitech/index.html')

def LoginPage(request):
    return render(request, 'sagitech/login.html')

def SignupPage(request):
    return render(request, 'sagitech/signup.html')

