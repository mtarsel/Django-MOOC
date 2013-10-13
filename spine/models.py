from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

#USER:
#username
#password
#email
#first name
#last name

class Instructor(models.Model):
	user = models.ForeignKey(User)

	def __unicode__(self):
	    return unicode(self.user)

class Course(models.Model):
	name = models.CharField(max_length=512)
	instructor = models.ForeignKey(Instructor)
	files = models.FileField(upload_to=get-upload-directory)

	def get-upload-dir(instance, filename):
	    user_id = instance.user.id
	    upload_dir = "%s/%d/%d/%s" % (settings.MEDIA_ROOT, course_id, user_id, filename)
	    print "Upload directory set to: %s" % upload_dir
	    return

	def __unicode__(self):
	    return unicode(self.name)

class Student(models.Model):
	user = models.ForeignKey(User)
	course = models.ManyToManyField(Course)

	def __unicode__(self):
	    return unicode(self.user)

class Grade(models.Model):
	grade = models.FloatField()
	#student = models.ForeignKey(Student, primary_key=True)
	student = models.ForeignKey(Student)
	#course = models.ForeignKey(Course, primary_key=True)
	course = models.ForeignKey(Course)

	def __unicode__(self):
	    return unicode(self.student.user.last_name) + ', ' + unicode(self.student.user.first_name) + " enrolled in " + unicode(self.course)
