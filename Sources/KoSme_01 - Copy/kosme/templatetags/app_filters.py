from django import template
from kosme.models import *

register = template.Library()

@register.filter
def student_result(things, user):
    student = Student.objects.get(user=user)
    return things.get(student=student).points

@register.filter
def result_exists(things, user):
    student = Student.objects.get(user=user)
    return things.filter(student=student).exists()
