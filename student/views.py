from django.shortcuts import render


def home(request):
    return render(request, 'student/home.html')

def courses(request):
    return render(request, 'student/courses.html')

