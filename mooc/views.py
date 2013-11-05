from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render, render_to_response, redirect

from student_portal.models import Course, Student, Lecture
from student_portal.views import get_separated_course_list, get_student_from_user, enroll_courses

def lecture(request):
    lectures = Lecture.objects.all()
    my_video = ''
    for lecture in lectures:
        if (lecture.name == 'Lecture01'):
            my_video = lecture.video
    context = {'my_video': my_video}
    return render_to_response('instructor_portal/lecture.html', context)

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def select_login(request):
    return render(request, 'login.html')

def get_course(course_id):
    course_list = Course.objects.all()
    for course in course_list:
        if (course.id == course_id):
            return course

def display_course_info(request, course_id):
    if request.method == 'POST':
        if not request.user.is_authenticated():
            return redirect('/student')
        enroll_courses(request)

    course = get_course(int(course_id))
    if request.user.is_authenticated():
        student = get_student_from_user(request.user)
        enrolled_ls, not_enrolled_ls = get_separated_course_list(student, Course.objects.all())
        is_enrolled = course in enrolled_ls

    else:
        is_enrolled = False
        
    print "display_course_info: got "
    print course
    print course.id
    return render(request, 'course_info.html', { 'course' : course,
                                                 'is_enrolled': is_enrolled})
