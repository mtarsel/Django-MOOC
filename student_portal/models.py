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
    user = models.OneToOneField(User)

    def __unicode__(self):
        return unicode(self.user)

class Course(models.Model):
    name = models.CharField(max_length=512)
    instructor = models.ForeignKey(Instructor)
    department = models.CharField(max_length=4)
    description = models.CharField(max_length=512)

    def __unicode__(self):
        return unicode(self.name)

class Student(models.Model):
    user = models.OneToOneField(User, unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    username = models.CharField(max_length=30)
    course = models.ManyToManyField(Course, blank=True, null=True)

    def __unicode__(self):
        return unicode(self.user)

class Assignment(models.Model):
    date = models.DateTimeField(editable=False, auto_now_add=True)
    course = models.ForeignKey(Course)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=512)
    points_possible = models.IntegerField(default=100)
    
    def __unicode__(self):
        return (self.course.name + " - " + self.name)

class Submission(models.Model):
    date = models.DateTimeField(editable=False, auto_now_add=True)
    course = models.ForeignKey(Course) 
    grade = models.FloatField(null = True, blank = True)
    assignment = models.ForeignKey(Assignment)
    submitter = models.ForeignKey(Student)
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')

    def get_grade_path(self, filename):
        savename = str(self.assignment.name) + os.path.splitext(filename)[1]
        return os.path.join('uploads/submitted_files/',
                            self.course.department,
                            self.course.name,
                            self.submitter.username,
                            savename)

    def __unicode__(self):
        return (self.assignment.__unicode__() + " - " + self.submitter.user.username)
