from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render, render_to_response, redirect
from django.core.urlresolvers import resolve
from django.views.defaults import server_error

from student_portal.models import Course, Student, Lecture
from student_portal.views import get_separated_course_list, get_student_from_user, enroll_courses

def redirect_to_app(request, student_ret, instructor_ret, default_ret):
    prev_url = request.META['HTTP_REFERER']
    print prev_url.split('/')
    if 'student' in prev_url.split('/'):
        print "in student block"
        return student_ret
    elif 'instructor' in prev_url.split('/'):
        print "in instructor block"
        return instructor_ret
    else:
        return default_ret

def index(request):
    return render(request, 'index.html')

def edit_profile(request):
    return redirect_to_app(request,
                           HttpResponseRedirect('/student/edit_profile'),
                           HttpResponseRedirect('/instructor/edit_profile'),
                           render(request, 'index.html'))

def about(request):
    if request.user.is_authenticated:
        return redirect_to_app(request,
                               HttpResponseRedirect('/student/about'),
                               HttpResponseRedirect('/instructor/about'),
                               render(request, 'about.html'))
    else:
        print request.get_full_path()
        return render(request, 'about.html')
#        return HttpResponseRedirect('about.html')
                
def select_login(request):
    return render(request, 'login.html')

def redirect_to_correct_dash(request):
    return redirect_to_app(request,
                           HttpResponseRedirect('/student'),
                           HttpResponseRedirect('/instructor'),
                           HttpResponseRedirect('/'))

def schedule(request):
    return redirect_to_app(request,
                           HttpResponseRedirect('/student/schedule'),
                           HttpResponseRedirect('/instructor/schedule'),
                           render(request, 'index.html'))
