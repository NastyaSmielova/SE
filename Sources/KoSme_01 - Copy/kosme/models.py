from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
   user = models.OneToOneField('auth.User')
   User._meta.get_field('email')._unique = True
   is_blocked = models.BooleanField(default=True)
   is_teacher = models.BooleanField(default=False)
   def __str__(self):
       return "%s %s %s" % (self.user, self.is_blocked, self.is_teacher)


class SchoolClass(models.Model):
   name = models.CharField(max_length=30, unique=True)
   class Meta:
        verbose_name_plural = "School classes"
   def __str__(self):
       return "%s " % (self.name)


class Student(models.Model):
    user = models.OneToOneField('auth.User')
    User._meta.get_field('email')._unique = True
    schoolClass = models.ForeignKey(SchoolClass, null=True)
    def __str__(self):
        return "%s %s %s " % (self.user, self.user.first_name, self.user.last_name)


class Teacher(models.Model):
   user = models.OneToOneField('auth.User')
   User._meta.get_field('email')._unique = True

   def __str__(self):
       return "%s %s %s " % (self.user, self.user.first_name, self.user.last_name)


class Course(models.Model):
       name = models.CharField(max_length=30, unique=True)
       author = models.ForeignKey(Teacher,null=True)
       def __str__(self):
           return self.name

class Quiz(models.Model):
    name = models.CharField(max_length=30)
    data = models.TextField(max_length=4000)
    def __str__(self):
        return "%s " % (self.name)

class Lecture(models.Model):
       name = models.CharField(max_length=30, unique=True)
       course = models.ForeignKey(Course,null=True)
       link =  models.CharField(max_length = 250,null=True)
       def __str__(self):
           return self.name


# Create your models here.
