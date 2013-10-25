from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from spine.models import Course, Submission
from spine.forms import DocumentForm
from django.contrib.auth import logout

from django.template import RequestContext
from django.core.urlresolvers import reverse

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

#def login(request):
#    return render(request, 'login.html')

#def register(request):
#    return render(request, 'register.html')

def courses(request):
    course_list = Course.objects.all()
    context = {'course_list': course_list}
    return render(request, 'courses.html', context)

def logout_view( request ):
    logout( request )
    return render(request, 'index.html')

def uploads(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Submission(file = request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('spine.views.uploads'))
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Submission.objects.all()
    context = {'documents': documents}
    return render(request, 'upload_submission.html', context)
