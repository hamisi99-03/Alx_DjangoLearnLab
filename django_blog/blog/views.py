
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
# simple views for login and registration pages
def login_view(request):
    return render(request, 'blog/login.html')

 #Registration view
def register_view(request):
    if request.method == 'POST':
        form =  CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto-login
            messages.success(request, 'Registration successful. Welcome!')
            return redirect('profile') 
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form =  CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

# Profile view
@login_required
def profile_view(request):
    if request.method == "POST":
        request.user.email = request.POST.get("email")
        request.user.save()
        return redirect("profile")
    return render(request, "blog/profile.html", {"user": request.user})


