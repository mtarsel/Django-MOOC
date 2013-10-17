from django.shortcuts import render


def home(request):
    return render(request, '/instructor/home.html')

def courses(request):
    return render(request, '/instructor/courses.html')

