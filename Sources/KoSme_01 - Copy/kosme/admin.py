from django.contrib import admin

from django.contrib import admin
from .models import  *
from .forms import *

class StudentAdmin(admin.ModelAdmin):
    list_display=['user', 'first_name', 'last_name', 'email']
    def first_name(self, obj):
        return obj.user.first_name
    def last_name(self,obj):
        return obj.user.last_name
    def email(self, obj):
        return obj.user.email

class StudentAdminInline(admin.TabularInline):
    model = Student

class ClassAdmin(admin.ModelAdmin):
    inlines = (StudentAdminInline, )

# Register your models here.
admin.site.register(SchoolClass,ClassAdmin)
admin.site.register(Student,StudentAdmin)
admin.site.register(Teacher)
admin.site.register(Course)
admin.site.register(Lecture)