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
    department = models.CharField(max_length=4)
    description = models.CharField(max_length=512)
#	files = models.FileField(upload_to=get_upload_dir)

    def __unicode__(self):
        return unicode(self.name)

class Student(models.Model):
    user = models.ForeignKey(User)

    course = models.ManyToManyField(Course)

    def __unicode__(self):
        return unicode(self.user)

class Assignment(models.Model):
    course = models.ForeignKey(Course)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=512)
    points_possible = models.IntegerField(default=100)
    

    def __unicode__(self):
        return (self.course.name + " - " + self.name)

class Submission(models.Model):
    date = models.DateTimeField(editable=False, auto_now_add=True)
    course = models.ForeignKey(Course)
    assignment = models.ForeignKey(Assignment)
    submitter = models.ForeignKey(Student)
    #file = ProtectedFileField(upload_to=get_grade_path, max_length=250)

    def get_grade_path(self, filename):
        savename = str(self.assignment.name) + os.path.splitext(filename)[1]
        return os.path.join('uploads/submitted_files/',
                            self.course.department,
                            self.course.name,
                            self.submitter.username,
                            savename)

    def __unicode__(self):
        return (self.assignment.__unicode__() + " - " + submitter.User.username)

class Grade(models.Model):
    grade = models.FloatField()
	#student = models.ForeignKey(Student, primary_key=True)
    student = models.ForeignKey(Student)
	#course = models.ForeignKey(Course, primary_key=True)
    course = models.ForeignKey(Course)

    def __unicode__(self):
        return unicode(self.student.user.last_name) + ', ' + unicode(self.student.user.first_name) + " enrolled in " + unicode(self.course)
