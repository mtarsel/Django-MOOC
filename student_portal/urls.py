from django.conf.urls import *
from student_portal.views import *
from django.contrib.auth.decorators import login_required as auth


urlpatterns = patterns('student_portal.views',

    # Main web portal entrance.
    (r'^$', dashboard),

    #about page
    url(r'^about/$', student_about, name='student_about'),

    url(r'^courses/$', enroll_courses,name="courses"),#show all courses available    

    # List uploaded files
    url(r'^list/$', 'list', name='list'),
    # edit_profile
    url(r'^edit_profile/$', auth(StudentProfileEditView.as_view()), name="edit_profile"), 
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
    #grades?
    url(r'^([A-Z|a-z]{2,4})/(\d+)/grades/$', display_grades, name='display_grades'),
)
