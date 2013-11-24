from django.shortcuts import render_to_response, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext

from registration.backends.simple.views import RegistrationView

from django.views.generic.edit import UpdateView

from instructor_portal.forms import SubmissionForm, InstructorProfileForm
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

def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Submission(docfile = request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('mooc.instructor_portal.views.list'))
    else:
        form = SubmissionForm() # A empty, unbound form

    # Load documents for the list page
    documents = Submission.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'instructor_portal/list.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    )

@login_required(login_url='/accounts/login/')
def dashboard(request):
    """
    If users are authenticated, direct them to the main page. Otherwise, take
    them to the login page.
    """
    taught_courses = get_separated_course_list(get_instructor_from_user(request.user), Course.objects.all())
    context = {'user': request.user, 'courses':taught_courses}
    #return render_to_response('instructor_portal/dashboard.html', {'user': request.user})
    return render_to_response('instructor_portal/dashboard.html', context)

def display_courses(request):
    course_list = Course.objects.all()
    taught_courses,not_taught_courses = get_separated_course_list(get_instructor_from_user(request.user), course_list)
    print(taught_courses)
    teacher = True
    context = {'taught_courses': taught_courses, 'course_list':course_list, 'teacher':teacher}
    return render(request, 'courses.html', context)

def course_dashboard(request, course_id):
    context={current_course: course_id}
    return render(request, 'instructor_portal/course_dashboard.html', context)
