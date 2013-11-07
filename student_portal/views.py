from django.shortcuts import render_to_response, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext

from registration.backends.simple.views import RegistrationView

from django.views.generic.edit import UpdateView

from student_portal.forms import SubmissionForm, StudentProfileForm
from student_portal.models import Submission, Course, Student, Lecture
#from mooc.views import get_course


def get_course(course_id):
    course_list = Course.objects.all()
    for course in course_list:
        if (course.id == course_id):
            return course

def get_lectures(course):
    lecture_list = Lecture.objects.all()
    class_lectures = []
    for lecture in lecture_list:
        if (lecture.course == course):
            class_lectures.append(lecture)
    return class_lectures

def display_course_info(request, _,  course_id):
    if request.method == 'POST':
        if not request.user.is_authenticated():
            return redirect('/student')
        enroll_courses(request)
    
    course = get_course(int(course_id))
    lecture_list = get_lectures(course)
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
                                                 'is_enrolled': is_enrolled,
                                                 'lecture_list' : lecture_list})


def display_course(request, course_id):
    if request.method == 'POST':
        if not request.user.is_authenticated():
            return redirect('/student')
        enroll_courses(request)

    course = get_course(int(course_id))
    lecture_list = get_lectures(course)
    if request.user.is_authenticated():
        student = get_student_from_user(request.user)
        enrolled_ls, not_enrolled_ls = get_separated_course_list(student, Course.objects.all())
        is_enrolled = course in enrolled_ls

    else:
        is_enrolled = False
        
    print "display_course_info: got "
    print course
    print course.id
    print lecture_list
    return render(request, 'lecture.html', { 'course' : course,
                                                 'lecture_list': lecture_list})

def get_lecture(lecture_id):
    lecture_list = Lecture.objects.all()
    for lecture in lecture_list:
        if(lecture.id == lecture_id):
            return lecture

@login_required(login_url='/accounts/login/')
def display_lecture(request,dept_id, course_id, lecture_id ):
    print("This is the dept. ID " + dept_id)
    print("This is the course " + course_id)
    print("This is the lecture_id " + lecture_id)
    lecture = get_lecture(int(lecture_id))
    lecture_list = get_lectures(lecture.course)
    my_video = lecture.video
    print(lecture.video)
    context = {'my_video': my_video, 'lecture_list': lecture_list}
    return render_to_response('lecture.html', context)


'''
class StudentProfileEditView(UpdateView):
    model = Student
    form_class = StudentProfileForm
    template_name = "student_portal/edit_profile.html"

    def get_object(self, queryset=None):
        return Student.objects.get_or_create(user=self.request.user)[0]

    def get_success_url(self):
	return "/student/" #TODO change this to send a user to a nice updated profile page
'''

def get_student_from_user(user):
    """
    takes the user from request.user and finds the student, or makes them into one
    """
    ls = [student for student in Student.objects.all() if student.user == user]
    if ls:
        return ls[0]
    else:
        student = Student(user=user)
        student.save()
        return student

def get_separated_course_list(student, course_list):
    """
    takes a student and a course_list, returns a list of courses that the student is enrolled in, and a list of the courses the student is not enrolled in
    """
    enrolled_courses = student.course.all()
    not_enrolled_courses = []
    for course in course_list:
        if not course.id in map(lambda course: course.id, enrolled_courses):
            not_enrolled_courses.append(course)
    return enrolled_courses, not_enrolled_courses

def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Submission(docfile = request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('mooc.student_portal.views.list'))
    else:
        form = SubmissionForm() # A empty, unbound form

    # Load documents for the list page
    documents = Submission.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'student_portal/list.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    )


@login_required(login_url='/accounts/login/')
def dashboard(request):
    """
    If users are authenticated, direct them to the main page. Otherwise, take
    them to the login page.
    """
    enrolled_courses, _ = get_separated_course_list(get_student_from_user(request.user), Course.objects.all())
    context = {'user': request.user,
               'courses':enrolled_courses}
    #return render_to_response('student_portal/dashboard.html', {'user': request.user})
    return render_to_response('student_portal/dashboard.html', context)

class MyRegistrationView(RegistrationView):
    def get_success_url(self, request, user):
        return "/student/"

def enroll_courses(request):
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
            return redirect('/student')

    else:
        if request.user.is_authenticated():
            current_student = get_student_from_user(request.user)
            enrolled_courses, not_enrolled_courses = get_separated_course_list(current_student, course_list)

        else:
            enrolled_courses = []
            not_enrolled_courses = course_list

        context = {'not_enrolled_courses': not_enrolled_courses,
                'enrolled_courses': enrolled_courses,
                'course_list': course_list}
        return render(request, 'courses.html', context)
