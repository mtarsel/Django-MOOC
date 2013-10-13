from django.contrib.auth import authenticate, login, redirect, logout
from django.shortcuts import render

def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active and user.groups == Instructor:
            login(request, user)
            return render(request, 'mooc/templates/student.html'
            # Redirect to a success page.
        elif user.is_active and user.groups == Student:
            login(request, user)
            return render(request, 'mooc/templates/instructor.html'
        else:
            # Return a 'disabled account' error message
    else:
        # Return an 'invalid login' error message.

def logout_view(request):
    logout(request)
