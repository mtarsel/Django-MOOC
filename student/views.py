from django.shortcuts import render

#@login_required
def home(request):
    return render(request, 'student/home.html')

#@login_required
def courses(request):
    return render(request, 'student/courses.html')

