from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render, render_to_response, redirect

from student_portal.models import Course, Student, Lecture
from student_portal.views import get_separated_course_list, get_student_from_user, enroll_courses

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def select_login(request):
    return render(request, 'login.html')

