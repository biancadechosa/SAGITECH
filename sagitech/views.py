from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from sagitech.models import UserProfile
from django.contrib.auth import logout
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import ensure_csrf_cookie

def LandingPage(request):
    return render(request, 'sagitech/index.html')

@ensure_csrf_cookie
def LoginPage(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Check if it's an AJAX request
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        if not email or not password:
            if is_ajax:
                return JsonResponse({'success': False, 'message': 'Email and password are required'}, status=400)
            else:
                # Handle non-AJAX request (fallback)
                messages.error(request, 'Email and password are required')
                return render(request, 'sagitech/login.html')
        
        # Authenticate user (adjust according to your authentication method)
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            if is_ajax:
                return JsonResponse({
                    'success': True, 
                    'message': 'Login successful',
                    'redirect_url': '/dashboard/'  # Change to your redirect URL
                })
            else:
                return redirect('dashboard')  # Fallback for non-AJAX
        else:
            if is_ajax:
                return JsonResponse({'success': False, 'message': 'Invalid email or password'}, status=401)
            else:
                messages.error(request, 'Invalid email or password')
                return render(request, 'sagitech/dashboard.html')
    
    # GET request - just render the login page
    return render(request, 'sagitech/login.html')

def SignupPage(request):
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Form validation
        if not fullname or not email or not password or not confirm_password:
            messages.error(request, 'All fields are required')
            return render(request, 'sagitech/signup.html')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'sagitech/signup.html')
        
        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long')
            return render(request, 'sagitech/signup.html')
        
        # Check if user already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return render(request, 'sagitech/signup.html')
        
        # Create the user
        try:
            # Using email as username for simplicity
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password
            )
            
            # Create user profile
            UserProfile.objects.create(
                user=user,
                full_name=fullname
            )
            
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
    
    return render(request, 'sagitech/signup.html')

@login_required
def DashboardPage(request):
    return render(request, 'sagitech/dashboard.html')

def LogoutView(request):
    logout(request)
    return redirect('login')