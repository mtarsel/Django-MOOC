from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render, render_to_response

from student_portal.models import Course

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def courses(request):
    course_list = Course.objects.all()
    context = {'course_list': course_list}
    return render(request, 'courses.html', context)

