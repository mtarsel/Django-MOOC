from django.shortcuts import render_to_response, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.conf import settings
from django.core.servers.basehttp import FileWrapper
from registration.backends.simple.views import RegistrationView
from django.views.generic.edit import UpdateView
from django.core.context_processors import csrf
from django.forms.models import inlineformset_factory

from instructor_portal.forms import SubmissionForm, InstructorProfileForm, NewCourseForm, NewAssignmentForm
import os
import mimetypes

from student_portal.views import get_assignment, get_assignments, get_course, get_lectures
from student_portal.models import *

class InstructorProfileEditView(UpdateView):
    model = Instructor
    form_class = InstructorProfileForm
    template_name = "instructor_portal/edit_profile.html"

    def get_object(self, queryset=None):
        return Instructor.objects.get_or_create(user=self.request.user)[0]

    def get_success_url(self):
	return "/instructor/" #TODO change this to send a user to a nice updated profile page

def instructor_about(request):
    return render(request, 'about.html')

def create_course(request):
    form = NewCourseForm()
    if request.method == 'POST':
	form = NewCourseForm(request.POST or None)
	if form.is_valid():
	    new_course = form.save(commit=False)
	    new_course.instructor = request.user.instructor
	    new_course.save()
	    #new_course = form.save()
	    return render_to_response('instructor_portal/dashboard.html')
    return render_to_response(
        'instructor_portal/new-course.html',
        { 'form': form},
        context_instance=RequestContext(request)
    )
'''
def new_assignment(request, course_id):
    course = Course.objects.get(pk=course_id)
#    form = NewAssignmentForm()
    NewAssignmentForm = inlineformset_factory(Course, Assignment)
#    assInlineFormSet = AssignmentInlineFormSet()
    if request.method == 'POST':
	form = NewAssignmentForm(request.POST, instance = course or None)
	if form.is_valid():
#	    new_ass = form.save(commit=False)
#	    new_ass.course = Course.objects.all().get(id=int(course_id))
#	    assInlineFormSet = AssignmentInlineFormSet(request.POST)
	    new_ass.save()
	    #assInlineFormSet = AssignmentInlineFormSet(request.POST)
	    
#	    if assInlineFormSet.is_valid():
#		assInlineFormSet.save()
#		return render_to_response('instructor_portal/dashboard.html')
    else:
	form = NewAssignmentForm(instance = course) 
    return render_to_response(
        'instructor_portal/new-assignment.html',
        { 'form': form},
        context_instance=RequestContext(request)
    )
'''

def new_assignment(request, course_id):
    course = Course.objects.get(pk=course_id)
    #NewAssignmentForm = inlineformset_factory(Course, Assignment)
    formset= NewAssignmentForm()
    if request.method == "POST":
        formset = NewAssignmentForm(request.POST or None)
        if formset.is_valid():
	    new_ass = formset.save(commit=False)
            new_ass.course = course
            formset.save()
            # Do something. Should generally end with a redirect. For example:
	    return render_to_response('instructor_portal/dashboard.html')
            #return HttpResponseRedirect(author.get_absolute_url())
#    else:
#        formset = NewAssignmentForm(instance=course)

    return render_to_response(
        'instructor_portal/new-assignment.html',
        { 'form': formset},
        context_instance=RequestContext(request)
    )

def lecture(request):
    my_video = 'http://www.youtube.com/watch?v=0d0uu7MW__U'
    context = {'my_video': my_video}
    return render_to_response('instructor_portal/dashboard.html', context)

def get_instructor_from_user(user):
    ls = [instructor for instructor in Instructor.objects.all() if instructor.user == user]
    if ls:
        return ls[0]
    else:
        instructor = Instructor(user=user)
        instructor.save()
        return instructor

def get_separated_course_list(instructor, course_list):
    taught_courses = instructor.course_set.all()#TODO error after login 
    not_taught_courses = []
    for course in course_list:
        if not course.id in map(lambda course: course.id, taught_courses):
            not_taught_courses.append(course)
    return taught_courses, not_taught_courses

@login_required(login_url='/accounts/login/')
def dashboard(request):
    """
    If users are authenticated, direct them to the main page. Otherwise, take
    them to the login page.
    """
    taught_courses,not_taught_courses = get_separated_course_list(get_instructor_from_user(request.user), Course.objects.all())
    context = {'user': request.user,
               'taught_courses':taught_courses}
    return render_to_response('instructor_portal/dashboard.html', context)

def display_courses(request):
    course_list = Course.objects.all()
    taught_courses,not_taught_courses = get_separated_course_list(get_instructor_from_user(request.user), course_list)
    print(taught_courses)
    teacher = True
    context = {'taught_courses': taught_courses,
               'course_list':course_list,
               'teacher':teacher}
    return render(request, 'courses.html', context)

def course_dashboard(request, course_id):
    course = get_course(int(course_id))
    assignments = get_assignments(course)
    course_materials = CourseMaterial.objects.all().filter(course=course)
    context = {'assignments' : assignments,
               'course' : course,
               'course_materials' : course_materials}
    return render(request, 'instructor_portal/course_dashboard.html', context)

def assignment_dashboard(request, course_id, assignment_id):
    course = Course.objects.all().get(id=int(course_id))
    assignments = Assignment.objects.all().filter(course=course)
    assignment = Assignment.objects.all().get(id=int(assignment_id))
    subs = Submission.objects.all().filter(assignment=assignment)
    context = {'submissions' : subs,
               'assignment' : assignment,
               'assignments' : assignments,
               'course' : course}
    context.update(csrf(request))
    if request.method == 'POST':
        print "in post"
        p = request.POST
        sub = Submission.objects.all().get(id=int(p['submission_id']))
        if p['newgrade']:
            sub.grade = float(p['newgrade'])
        sub.remarks = p['newremarks']
        sub.save()
        return render(request, 'instructor_portal/assignment_dashboard.html',context)
    return render(request, 'instructor_portal/assignment_dashboard.html', context)

@login_required(login_url='/accounts/login/') 
def download_submission(request, course_id, assignment_id, submission_id):
    sub = Submission.objects.all().get(id=int(submission_id))
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

def display_course_info(request, course_department, course_id):
    course = get_course(int(course_id))
    lecture_list = get_lectures(course)
    assignment_list = get_assignments(course)
    print assignment_list
    if request.user.is_authenticated():
        instructor = Instructor.objects.all().get(id=request.user.instructor.id)
        taught_courses, not_taught_courses = get_separated_course_list(instructor, Course.objects.all())
        is_taught = course in taught_courses
        
    is_enrolled = False
    return render(request, 'course_info.html', { 'course' : course,
                                                 'is_enrolled': is_enrolled,
                                                 'lecture_list' : lecture_list,
                                                 'assignment_list': assignment_list,
                                                 'is_student' : False})

def delete_course_material(request, course_id, course_mat_id):
    cm = CourseMaterial.objects.all().get(id=int(course_mat_id))
    os.remove(cm.file.name)
    cm.delete()
    return HttpResponseRedirect('/instructor/' + course_id + '/dashboard')

def download_course_material(request, course_id, course_mat_id):
    cm = CourseMaterial.objects.all().get(id=int(course_mat_id))
    dirlist = cm.file.name.split(os.sep)
    print dirlist
    while dirlist[0] != 'media':
        dirlist.pop(0)
    type, _ = mimetypes.guess_type(dirlist[-1])
    f = open(cm.file.name, "r")
    response = HttpResponse(FileWrapper(f), content_type=type)
    response['Content-Disposition'] = 'attachment; filename=' + dirlist[-1]
    return response

def handle_uploaded_course_material(file, course_department, course_id, cm_description, user):
    if file:
        cm = CourseMaterial(course = get_course(int(course_id)),
                            description = cm_description)
        cm.save()
                            
        directory = settings.MEDIA_ROOT+ '/' + course_department + '/' + unicode(course_id) +  '/course_material/'
        if not os.path.exists(directory):
            os.makedirs(directory)
        _, fileExtension = os.path.splitext(file.name)
        filename = course_department + '_' + unicode(course_id) + '_' + unicode(cm.id)  + fileExtension
        print filename
        destination = open(directory+filename, 'wb+')
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()
        cm.file.name = directory+filename
        cm.save()
        
def upload_course_material(request, course_id):
    if request.method == 'POST':
        a = request.POST #the post dict
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            course = get_course(int(course_id))
            handle_uploaded_course_material(request.FILES['file'], course.department, course.id, a['description'], request.user)
            return HttpResponseRedirect('/instructor/' + course_id + '/dashboard')

    else:
        form = SubmissionForm()
    
    context = {'form' : form}
    context.update(csrf(request))
    return render_to_response('upload.html', context)
