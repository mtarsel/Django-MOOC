from django.conf.urls.defaults import *
from student_portal.views import *
from django.contrib.auth.decorators import login_required as auth


urlpatterns = patterns('student_portal.views',

    # Main web portal entrance.
    (r'^$', dashboard),
    
    # List uploaded files
    url(r'^list/$', 'list', name='list'),

    #edit student profile 
    url(r'^edit_profile/$', auth(StudentProfileEditView.as_view()), name="edit_profile"),

    # django registration simple, no email registration
    url(r'^accounts/', include('registration.backends.simple.urls')),
    # course info display
    url(r'^([A-Z|a-z]{2,4})/(\d+)/(\d+)/$', display_lecture, name='display_lecture'),
    url(r'^([A-Z|a-z]{2,4})/(\d+)/$', display_course_info, name='display_course_info'),
    #assignments
    url(r'^([A-Z|a-z]{2,4})/(\d+)/assignments/$', display_assignments, name='display_assignments'),
    url(r'^([A-Z|a-z]{2,4})/(\d+)/assignments/(\d+)/$', display_assignment, name='display_assignment'),
    #uploads
    url(r'^([A-Z|a-z]{2,4})/(\d+)/assignments/(\d+)/upload/$', upload_assignment, name='upload_assignment'),
    #downloading
    url(r'^([A-Z|a-z]{2,4})/(\d+)/assignments/(\d+)/download/$', download_assignment, name='download_assignment'),
)
