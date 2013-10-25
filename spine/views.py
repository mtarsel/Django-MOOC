from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render, render_to_response
from spine.models import Course
from django.contrib.auth import logout

from spine.models import Document
from spine.forms import DocumentForm

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

def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('spine.views.list'))
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'list.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    )
