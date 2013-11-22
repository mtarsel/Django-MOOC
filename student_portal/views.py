from django.shortcuts import render_to_response, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.core.context_processors import csrf
from django.conf import settings
from django.core.servers.basehttp import FileWrapper

from registration.backends.simple.views import RegistrationView
import os
import mimetypes
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView

from student_portal.forms import SubmissionForm, StudentProfileForm
from student_portal.models import Submission, Course, Student, Lecture
from student_portal.models import Assignment, Homework, Quiz, Exam, Project
#from mooc.views import get_course

def get_assignments(course):
    assignment_list = Assignment.objects.all()
    assignments = []
    for assignment in assignment_list:
        if(assignment.course == course):
            assignments.append(assignment)
    return assignments

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
                                                 'assignment_list': assignment_list})


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
    return render(request, 'lecture.html', context)


class StudentProfileEditView(UpdateView):
    model = Student
    form_class = StudentProfileForm
    template_name = "student_portal/edit_profile.html"

    def get_object(self, queryset=None):
        return Student.objects.get_or_create(user=self.request.user)[0]

    def get_success_url(self):
	return "/student/" #TODO change this to send a user to a nice updated profile page

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

def get_submissions(student, course):
    submissions = Submission.objects.all()
    student_submissions = []
    for submission in submissions:
        if submission.submitter == student and submission.course == course:
            student_submissions.append(submission)
    print (student_submissions)
    return student_submissions

def get_homeworks(student, course):
    homeworks = Homework.objects.all()
    student_homeworks = []
    for homework in homeworks:
        if homework.submitter == student and homework.course == course:
            student_homeworks.append(homework)
    print (student_homeworks)
    return student_homeworks

def get_quizzes(student, course):
    quizzes = Quiz.objects.all()
    student_quizzes = []
    for quiz in quizzes:
        if quiz.submitter == student and quiz.course == course:
            student_quizzes.append(quiz)
    print (student_quizzes)
    return student_quizzes

def get_exams(student, course):
    exams = Exam.objects.all()
    student_exams = []
    for exam in exams:
        if exam.submitter == student and exam.course == course:
            student_exams.append(exam)
    print (student_exams)
    return student_exams

def get_projects(student, course):
    projects = Project.objects.all()
    student_projects = []
    for project in projects:
        if project.submitter == student and project.course == course:
            student_projects.append(project)
    print (student_projects)
    return student_projects

def get_grades(submissions):
    total = 0
    grade = 0
    weight = 0
    if len(submissions) > 0:
        weight = submissions[0].weight

    for submission in submissions:
        total = total + submission.assignment.points_possible * weight
        if not submission.grade == None:
            grade = grade + submission.grade * weight

    total_and_grade = []
    total_and_grade.append(total)
    total_and_grade.append(grade)
    return total_and_grade

def display_grades(request, course_department, course_id):
    student = request.user.student
    course = get_course(int(course_id))
    homeworks = get_homeworks(student, course)
    quizzes = get_quizzes(student, course)
    exams = get_exams(student, course)
    projects = get_projects(student, course)
    hwgrades = get_grades(homeworks)
    hwtotal = hwgrades[0]
    hwgrade = hwgrades[1]
    quizgrades = get_grades(quizzes)
    quiztotal = quizgrades[0]
    quizgrade = quizgrades[1]
    examgrades = get_grades(exams)
    examtotal = examgrades[0]
    examgrade = examgrades[1]
    projectgrades = get_grades(projects)
    projecttotal = projectgrades[0]
    projectgrade = projectgrades[1]
    grade = hwgrade + quizgrade + examgrade + projectgrade
    total = hwtotal + quiztotal + examtotal + projecttotal

    context = {'homeworks': homeworks,
               'quizzes': quizzes,
               'exams': exams,
               'projects': projects,
               'course': course,
               'total': total,
               'grade': grade,
               'hwtotal': hwtotal, 'hwgrade': hwgrade,
               'quiztotal': quiztotal, 'quizgrade': quizgrade,
               'examtotal': examtotal, 'examgrade': examgrade,
               'projecttotal': projecttotal, 'projectgrade': projectgrade}
    return render(request, 'student_portal/grades.html', context)
