from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from spine.models import Course
from django.contrib.auth import logout

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

#def login(request):
#    return render(request, 'login.html')

#def register(request):
#    return render(request, 'register.html')

def courses(request):
    course_list = Course.objects.all()
    context = {'course_list': course_list}
    return render(request, 'courses.html', context)

def logout_view( request ):
    logout( request )
