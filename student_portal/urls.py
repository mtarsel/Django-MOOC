from django.conf.urls.defaults import *
from student_portal.views import *
from django.contrib.auth.decorators import login_required as auth


urlpatterns = patterns('student_portal.views',

    # Main web portal entrance.
    (r'^$', dashboard),
    
    #List uploaded files
    url(r'^list/$', 'list', name='list'),

    #edit student profile 
    url(r'^edit_profile/$', auth(StudentProfileEditView.as_view()), name="edit_profile"),

# django registration simple, no email registration
    url(r'^accounts/', include('registration.backends.simple.urls')),

)
