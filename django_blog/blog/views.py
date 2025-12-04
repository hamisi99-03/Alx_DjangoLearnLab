
from django.shortcuts import render
# simple views for login and registration pages
def login_view(request):
    return render(request, 'blog/login.html')

def register_view(request):
    return render(request, 'blog/register.html')