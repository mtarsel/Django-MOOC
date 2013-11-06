from django.shortcuts import render_to_response, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext

from registration.backends.simple.views import RegistrationView

from django.views.generic.edit import UpdateView

from instructor_portal.forms import SubmissionForm, InstructorProfileForm
from student_portal.models import Submission, Course, Instructor
'''
class InstructorProfileEditView(UpdateView):
    model = Instructor
    form_class = InstructorProfileForm
    template_name = "instructor_portal/edit_profile.html"

    def get_object(self, queryset=None):
        return Instructor.objects.get_or_create(user=self.request.user)[0]

    def get_success_url(self):
	return "/instructor/" #TODO change this to send a user to a nice updated profile page
'''

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
    enrolled_courses = instructor.course.all()
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
    enrolled_courses, _ = get_separated_course_list(get_instructor_from_user(request.user), Course.objects.all())
    context = {'user': request.user,
               'courses':enrolled_courses}
    #return render_to_response('instructor_portal/dashboard.html', {'user': request.user})
    return render_to_response('instructor_portal/dashboard.html', context)

class MyRegistrationView(RegistrationView):
    def get_success_url(self, request, user):
        return "/instructor/"

def enroll_courses(request):
    course_list = Course.objects.all()
    if request.method == 'POST':
        if request.user.is_authenticated():
            courseid = int(request.POST['course'])
            enroll = str(request.POST['enroll']) == "True"
            current_instructor = get_instructor_from_user(request.user)
            
            if enroll:
                current_instructor.course.add(courseid)
            else:
                current_instructor.course.remove(courseid)

            current_instructor.save()
            print current_instructor.course.all()
            enrolled_courses, not_enrolled_courses = get_separated_course_list(current_instructor, course_list)
            context = {'not_enrolled_courses': not_enrolled_courses,
                       'enrolled_courses': enrolled_courses,
                       'course_list': course_list}
            return render(request, 'courses.html', context)

        else:
            return redirect('/accounts/login')

    else:
        if request.user.is_authenticated():
            current_instructor = get_instructor_from_user(request.user)
            enrolled_courses, not_enrolled_courses = get_separated_course_list(current_instructor, course_list)

        else:
            enrolled_courses = []
            not_enrolled_courses = course_list

        context = {'not_enrolled_courses': not_enrolled_courses,
                'enrolled_courses': enrolled_courses,
                'course_list': course_list}
        return render(request, 'courses.html', context)
