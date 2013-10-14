from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
def student_view(request):
    return render(request,'student.html')

def instructor_view(request):
    return render(request,'instructor.html')

def login_fields(request):
    return render(request, 'login.html')

def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            if user.groups == Instructor:
                return redirect('/instructor/')
                #return render(request, 'mooc/templates/student.html'
                # Redirect to a success page.
            if user.groups == Student:
                return redirect('/student/')
                #return render(request, 'mooc/templates/instructor.html'
        else:
            return redirect('/login/')
            # Return a 'disabled account' error message
    else:
        return redirect('/login/')
        # Return an 'invalid login' error message.

def logout_view(request):
    logout(request)
