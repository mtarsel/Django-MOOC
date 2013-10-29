from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render, render_to_response

from student_portal.models import Course, Student

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')
