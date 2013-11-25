from django.conf.urls import *
from instructor_portal.views import *
from django.contrib.auth.decorators import login_required as auth


urlpatterns = patterns('instructor_portal.views',

    # Main web portal entrance.
    (r'^$', dashboard),

    url(r'^schedule/$', include('schedule.urls')),

    #about page
    url(r'^about/$', instructor_about, name='instructor_about'),    

    url(r'^courses/$', 'display_courses', name='display_courses'),#show all courses available    

    #List uploaded files
    url(r'^list/$', 'list', name='list'),

    #edit instructor profile 
    url(r'^edit_profile/$', auth(InstructorProfileEditView.as_view()), name="edit_profile"),

# create course page
    url(r'^new-course/', create_course, name='create_course'),

# create a new assignment page
    url(r'^new-assignment/', new_assignment, name='new_assignment'),
# django registration simple, no email registration
#    url(r'^accounts/', include('registration.backends.simple.urls')),
    # course_info for instructors
#    url(r'^([A-Z|a-z]{2,4})/(\d+)/$', display_course_info, name='display_course_info'),

    #instructor course dashboards
    url(r'^(\d+)/dashboard/$', 'course_dashboard', name='course_dashboard'),

    url(r'^(\d+)/assignments/(\d+)/$', 'assignment_dashboard', name='assignment_dashboard'),
    url(r'^(\d+)/assignments/(\d+)/(\d+)/download/$', 'download_submission', name=download_submission),
)
