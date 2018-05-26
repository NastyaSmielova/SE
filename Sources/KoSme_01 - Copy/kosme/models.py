from django.db import models
from django.contrib.auth.models import User

import django.utils.timezone as timezone

class Profile(models.Model):
   user = models.OneToOneField('auth.User')
   User._meta.get_field('email')._unique = True
   is_blocked = models.BooleanField(default=True)
   is_teacher = models.BooleanField(default=False)
   def __str__(self):
       return "%s %s %s" % (self.user, self.is_blocked, self.is_teacher)


class Teacher(models.Model):
   user = models.OneToOneField('auth.User')
   User._meta.get_field('email')._unique = True

   def __str__(self):
       return "%s %s %s " % (self.user, self.user.first_name, self.user.last_name)


class SchoolClass(models.Model):
   name = models.CharField(max_length=30, unique=True)
   class Meta:
        verbose_name_plural = "School classes"
   def __str__(self):
       return "%s " % (self.name)


class Course(models.Model):
       name = models.CharField(max_length=30)
       author = models.ForeignKey(Teacher,null=True)
       classes = models.ManyToManyField(SchoolClass)

       class Meta:
           verbose_name_plural = "Courses"

       def __str__(self):
           return self.name



class Student(models.Model):
    user = models.OneToOneField('auth.User')
    User._meta.get_field('email')._unique = True
    schoolClass = models.ForeignKey(SchoolClass, null=True)
    def __str__(self):
        return "%s %s %s " % (self.user, self.user.first_name, self.user.last_name)



class Result(models.Model):
    student = models.ForeignKey(Student)
    points = models.IntegerField(default=0)

class Quiz(models.Model):
    name = models.CharField(max_length=30)
    data = models.TextField(max_length=4000)
    results = models.ForeignKey(Result,null=True)
    class Meta:
        verbose_name_plural = "Quizes"
    def __str__(self):
        return "%s " % (self.name)

class Lecture(models.Model):
       name = models.CharField(max_length=100)
       course = models.ForeignKey(Course,null=True)
       link =  models.CharField(max_length = 250,null=True)
       date = models.DateField(default=timezone.now())
       def __str__(self):
           return self.name


# Create your models here.
