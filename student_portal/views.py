from django.shortcuts import render_to_response, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext

from registration.backends.simple.views import RegistrationView

from student_portal.forms import SubmissionForm
from student_portal.models import Submission

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
<<<<<<< HEAD
    return render_to_response('student_portal/dashboard.html')


class MyRegistrationView(RegistrationView):
    def get_success_url(self, request, user):
        return "/student/"
=======
    return render_to_response('student_portal/dashboard.html', {'user': request.user})
>>>>>>> a2b4d8b2c6de873d322d8f0a0ad189f7e9a9aa2f
