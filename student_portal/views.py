from django.shortcuts import render_to_response, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.template import RequestContext
from django.core.context_processors import csrf
from django.conf import settings
from django.core.servers.basehttp import FileWrapper
from registration.backends.simple.views import RegistrationView
from django.views.static import serve
import matplotlib.pyplot as plt
import numpy as np
import os
import mimetypes

from django.views.generic.edit import UpdateView

from student_portal.forms import SubmissionForm, StudentProfileForm

from student_portal.models import Submission, Course, Student, Lecture, Assignment, Homework, Quiz, Exam, Project, CourseMaterial

def student_about(request):
    return render(request, 'about.html')

class StudentProfileEditView(UpdateView):
    model = Student
    form_class = StudentProfileForm
    template_name = "student_portal/edit_profile.html"

    def get_object(self, queryset=None):
        return Student.objects.get_or_create(user=self.request.user)[0]

    def get_success_url(self):
        return "/student/"

def get_assignments(course):
    assignment_list = Assignment.objects.all()
    assignments = []
    for assignment in assignment_list:
        if(assignment.course == course):
            assignments.append(assignment)
    return assignments

def get_course(course_id):
    course_list = Course.objects.all().order_by('name')
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
    assignment_list = get_assignments(course)
    print assignment_list
    if request.user.is_authenticated():
        student = get_student_from_user(request.user)
        enrolled_ls, not_enrolled_ls = get_separated_course_list(student, Course.objects.all())
        is_enrolled = course in enrolled_ls

    else:
        is_enrolled = False
        
    print "display_course_info: got "
    print is_enrolled
    print course.description
    print course.id
    return render(request, 'course_info.html', { 'course' : course,
                                                 'is_enrolled': is_enrolled,
                                                 'lecture_list' : lecture_list,
                                                 'assignment_list': assignment_list,
                                                 'is_student' : True})


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
    course = get_course(int(course_id))
    lecture = get_lecture(int(lecture_id))
    lecture_list = get_lectures(lecture.course)
    my_video = lecture.video
    print(lecture.video)
    context = {'my_video': my_video, 'lecture_list': lecture_list, 'course':course}
    return render(request, 'lecture.html', context)


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

@login_required(login_url='/accounts/login/') 
def dashboard(request):
    enrolled_courses = get_separated_course_list(get_student_from_user(request.user), Course.objects.all())
    context = {'user': request.user,
	   'courses':enrolled_courses}
    """
    If users are authenticated, direct them to the main page. Otherwise, take
    them to the login page.
    """
    enrolled_courses, _ = get_separated_course_list(get_student_from_user(request.user), Course.objects.all().order_by('name'))
    context = {'user': request.user,
               'courses':enrolled_courses.order_by('name')}
    #return render_to_response('student_portal/dashboard.html', {'user': request.user})
    return render_to_response('student_portal/dashboard.html', context)

class MyRegistrationView(RegistrationView):
    def get_success_url(self, request, user):
        return "/student/"

def enroll_courses(request):
    course_list = Course.objects.all().order_by('name')
    if request.method == 'POST':
        if request.user.is_authenticated():
            current_student = get_student_from_user(request.user)
            if request.POST['course'] != "":
                courseid = int(request.POST['course'])
                enroll = str(request.POST['enroll']) == "True"
            
                if enroll:
                    current_student.course.add(courseid)
                else:
                    current_student.course.remove(courseid)

                    current_student.save()
                    print current_student.course.all()
                enrolled_courses, not_enrolled_courses = get_separated_course_list(current_student, course_list)
                context = {'not_enrolled_courses': not_enrolled_courses,
                           'enrolled_courses': enrolled_courses.order_by('name'),
                           #'course_list': course_list.order_by(request.POST['sort'])} this doesn't work in the case of enrolling from the course_info page
                           'course_list': course_list}
                return render(request, 'courses.html', context)
            else:
                enrolled_courses, not_enrolled_courses = get_separated_course_list(current_student, course_list)

                context = {'not_enrolled_courses': not_enrolled_courses,
                           'enrolled_courses': enrolled_courses.order_by('name'),
                           'course_list': course_list.order_by(request.POST['sort'])}
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

@login_required(login_url='/accounts/login/') 
def display_assignments(request, course_department, course_id):
    course = get_course(int(course_id))
    assignments = get_assignments(course)
    print course.id
    context = {'assignments': assignments, 'course': course}
    return render(request, 'student_portal/all_assignments.html', context)

def get_assignment(assignments, assignment_id):
    for a in assignments:
        if a.id == assignment_id:
            return a

def get_submission(user, assignment_id):
    for sub in Submission.objects.all():
        if (sub.assignment.id == assignment_id) and (sub.submitter == user.student):
            return sub
    return None

@login_required(login_url='/accounts/login/') 
def display_assignment(request, course_department, course_id, assignment_id):
    course = get_course(int(course_id))
    print course.id
    assignments = get_assignments(course)
    assignment = get_assignment(assignments, int(assignment_id))
    print assignment.id
    sub = get_submission(request.user, int(assignment_id))
    print sub
    context = {'assignment': assignment,
               'assignments': assignments,
               'course': course,
               'submission': sub}
    return render(request, 'student_portal/assignments.html', context)

def handle_uploaded_file(file, course_department, course_id, assignment_id, user):
    if file:
        directory = settings.MEDIA_ROOT+ '/' + course_department+ '/' + course_id + '/' + assignment_id + '/'
        if not os.path.exists(directory):
            os.makedirs(directory)
        _, fileExtension = os.path.splitext(file.name)
        filename = user.username + fileExtension
        destination = open(directory+filename, 'wb+')
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()
        old = get_submission(user, int(assignment_id))
        if old != None:
            old.delete()
        course = get_course(int(course_id))
        assign = get_assignment(get_assignments(course), int(assignment_id))
        if assign.submission_type == 'Quiz':
            sub = Quiz()
        elif assign.submission_type == 'Exam':
            sub = Exam()
        elif assign.submission_type == 'Homework':
            sub = Homework()
        else:
            sub = Project()
        sub.course = course
        sub.assignment = assign
        sub.submitter = user.student
        sub.docfile.name = directory+filename
        sub.save()

@login_required(login_url='/accounts/login/') 
def upload_assignment(request, course_department, course_id, assignment_id):
    assignments = get_assignments(get_course(int(course_id)))
    assignment = get_assignment(assignments, int(assignment_id))
    print assignment.id 
    if request.method == 'POST':
        a=request.POST #the post dict
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'], course_department, course_id, assignment_id, request.user)
            return HttpResponseRedirect('/student/' + course_department + '/' + course_id + '/assignments/' + assignment_id + '/')

    else:
        form = SubmissionForm()
    
    context = {'form' : form}
    context.update(csrf(request))
    return render_to_response('upload.html', context)

@login_required(login_url='/accounts/login/') 
def download_assignment(request, course_department, course_id, assignment_id):
    sub = get_submission(request.user, int(assignment_id))
    print sub.id
    dirlist = sub.docfile.name.split(os.sep)
    while dirlist[0] != 'media':
        dirlist.pop(0)
    print dirlist
    print dirlist[-1]
    type, _ = mimetypes.guess_type(dirlist[-1])
    print type
    f = open(sub.docfile.name, "r")
    response = HttpResponse(FileWrapper(f), content_type=type)
    response['Content-Disposition'] = 'attachment; filename=' + dirlist[-1]
    return response

def get_graded_material(student, course, model):
    student_model = []
    for x in model.objects.all():
        if x.submitter == student and x.course == course:
            student_model.append(x)
    return student_model

def get_grades(submissions):
    total = 0
    grade = 0
    weight = 0
    if submissions:
        weight = submissions[0].weight

    for submission in submissions:
        total = total + submission.assignment.points_possible * weight
        if not submission.grade == None:
            grade = grade + submission.grade * weight

    return total, grade

def get_total_grade(course, student): #not pythonic lyfe
    return sum([item for sublist in
                    ( map(get_grades, # that feel when no functional compose
                         map(lambda x: get_graded_material(student, course, x),
                             [Homework, Quiz, Exam, Project])))
                  for item in sublist][1::2])

def update_histogram(course):
    total_grade = sum(map(lambda x: eval(x.submission_type).weight*x.points_possible , course.assignment_set.all())) #it's safe but I feel bad anyway
    all_grades = map(lambda x: get_total_grade(course, x)/total_grade, course.student_set.all())
    student_and_grade = zip(course.student_set.all(), all_grades)
    ranked_students = sorted( filter(lambda x: x[1] != 0, student_and_grade), key=lambda x: x[1])[::-1]
    ranked_grades = np.array(filter(lambda x: x != 0, all_grades))
    plt.clf()
    if ranked_students:
        n, bins, patches = plt.hist( ranked_grades , bins=20, color='b')
    else:
        return -1
    plt.axvline(ranked_grades.mean(), color='r', linestyle='dashed', linewidth=2, label='mean')
    print np.median(ranked_grades)
    plt.axvline(np.median(ranked_grades), color='g', linestyle='dashed', linewidth=2, label='median')
    plt.legend()
    plt.xlim([0, 1])
    plt.xlabel('Total Grade')
    plt.ylabel('Students')
    plt.yticks( range(1, n.max()+3) )
    fig = plt.gcf()
    fig.set_size_inches(10,4)
    fn = settings.MEDIA_ROOT + '/' + course.department + '/' + str(course.id) + '/distribution.png'
    plt.savefig(fn, bbox_inches=0, transparent=True)
    fn = fn.split('/')
    while fn[0] != 'media': fn.pop(0)
    fn_ = ''
    for d in fn: fn_ += '/' + d
    return fn_

def update_rank_and_histogram(course, student):
    all_grades = map(lambda x: get_total_grade(course, x), course.student_set.all())
    student_and_grade = zip(course.student_set.all(), all_grades)
    ranked_students = sorted( filter(lambda x: x[1] != 0, student_and_grade), key=lambda x: x[1])[::-1]
    amt_ranked = len(ranked_students)
    try: # get a student's rank
        rank = [y[0] for y in ranked_students ].index(student) + 1
    except ValueError:
        rank = 0
    fn = update_histogram(course)
    return rank, amt_ranked, fn

def display_grades(request, course_department, course_id):
    student = request.user.student
    course = get_course(int(course_id))
    homeworks, quizzes, exams, projects = map(lambda x: get_graded_material(student, course, x), [Homework, Quiz, Exam, Project])
    (hwtotal, hwgrade), (quiztotal, quizgrade), (examtotal, examgrade), (projecttotal, projectgrade) =  map(get_grades, [homeworks, quizzes, exams, projects])
    grade = hwgrade + quizgrade + examgrade + projectgrade
    total = hwtotal + quiztotal + examtotal + projecttotal
    rank, amt_ranked, hist_fn = update_rank_and_histogram(course, student)
    context = {'homeworks': homeworks,
               'quizzes': quizzes,
               'exams': exams,
               'projects': projects,
               'course': course,
               'total': total,
               'grade': grade,
               'hwtotal': hwtotal,           'hwgrade': hwgrade,
               'quiztotal': quiztotal,       'quizgrade': quizgrade,
               'examtotal': examtotal,       'examgrade': examgrade,
               'projecttotal': projecttotal, 'projectgrade': projectgrade,
               'rank' : rank, 'amt_ranked' : amt_ranked, 'hist_img' : hist_fn}
    return render(request, 'student_portal/grades.html', context)

def display_course_materials(request, course_dept, course_id):
    c = get_course(int(course_id))
    courses = list(request.user.student.course.all())
    cms = CourseMaterial.objects.all().filter(course=c)
    lecture_list = get_lectures(c)
    assignment_list = get_assignments(c)
    context = {'course' : c,
               'courses' : courses,
               'lecture_list' : lecture_list,
               'assignment_list' : assignment_list,
               'is_enrolled' : True,
               'course_materials' : cms}
    return render(request, 'student_portal/course_materials.html', context)

def download_course_materials(request, course_dept, course_id, coursemat_id):
    c = get_course(int(course_id))
    cm = CourseMaterial.objects.all().get(id=int(coursemat_id))
    dirlist = cm.file.name.split(os.sep)
    while dirlist[0] != 'media':
        dirlist.pop(0)
    type, _ = mimetypes.guess_type(dirlist[-1])
    f = open(cm.file.name, "r")
    response = HttpResponse(FileWrapper(f), content_type=type)
    response['Content-Disposition'] = 'attachment; filename=' + dirlist[-1]
    return response

def display_distribution(request, course_dept, course_id, document_root):
    update_histogram(get_course(int(course_id)))
    return serve(request, course_dept + '/' + course_id + '/distribution.png', document_root)
