from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render, render_to_response

from student_portal.models import Course, Student

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def get_student_from_user(user):
    return [student for student in Student.objects.all() if student.user == user][0]

def get_separated_course_list(student, course_list):
    enrolled_courses = student.course.all()
    not_enrolled_courses = []
    for course in course_list:
        if not course.id in map(lambda course: course.id, enrolled_courses):
            not_enrolled_courses.append(course)
    return enrolled_courses, not_enrolled_courses

def courses(request):
    course_list = Course.objects.all()
    if request.method == 'POST':
        if request.user.is_authenticated():
            courseid = int(request.POST['course'])
            enroll = str(request.POST['enroll']) == "True"
            current_student = get_student_from_user(request.user)
            
            if enroll:
                current_student.course.add(courseid)
            else:
                current_student.course.remove(courseid)

            current_student.save()
            print current_student.course.all()
            enrolled_courses, not_enrolled_courses = get_separated_course_list(current_student, course_list)
            context = {'not_enrolled_courses': not_enrolled_courses,
                       'enrolled_courses': enrolled_courses,
                       'course_list': course_list}
            return render(request, 'courses.html', context)

        else:
            return render(request, 'courses.html')

    else:
        if request.user.is_authenticated():
            current_student = get_student_from_user(request.user)
        
            #enrolled_courses = current_student.course.all()
            #not_enrolled_courses = [for course in course_list if not map(lambda course: course.id,enrolled_courses).contains(course.id)]
            #not_enrolled_courses = []
            #for course in course_list:
            #    if not course.id in map(lambda course: course.id, enrolled_courses):
            #        not_enrolled_courses.append(course)

            enrolled_courses, not_enrolled_courses = get_separated_course_list(current_student, course_list)

        else:
            enrolled_courses = []
            not_enrolled_courses = course_list

        context = {'not_enrolled_courses': not_enrolled_courses,
                'enrolled_courses': enrolled_courses,
                'course_list': course_list}
        return render(request, 'courses.html', context)
