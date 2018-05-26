from django.http import HttpResponseRedirect
from django.views import generic
from rest_framework.utils import json
from django.contrib import messages
from kosme.forms import SignUpForm, UserForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .models import *
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
import os.path
import re
from django.http import HttpResponse
from django.utils.safestring import mark_safe
# Create your views here.



from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate

import pdfkit


@csrf_exempt
def lectureIDEdit(request,pk_lect):
    if request.method == "GET":
        lecture = Lecture.objects.filter(id=pk_lect)[0]
        myfile = open(lecture.link)
        text = myfile.read()
        myfile.close()
        return render_to_response('kosme/lectureEdit.html', {'lecture': lecture, 'text': text})
    if request.method == 'POST':
        dataToSave = request.POST.get("HTMLtoPDF", "")

        lecture = Lecture.objects.filter(id = pk_lect)[0]
        file1 = open(lecture.link, "w")
        toFile = dataToSave
        file1.write(toFile)
        file1.close()

        all_courses = Course.objects.all()
        return render_to_response('kosme/allCourses.html', {'all_courses': all_courses})



@csrf_exempt
def lectureCreate(request,pk_course):
    if request.method == "GET":

        return render_to_response('kosme/lectureCreate.html')

    if request.method == 'POST':
        dataToSave = request.POST.get("HTMLtoPDF", "")
        fileName = request.POST.get("fileName", "")
        save_path = 'C:/users/pc/Desktop/KoSmeShool'

        name_of_file = fileName
        lecture = Lecture()
        lecture.name = fileName
        lecture.course_id = pk_course

        completeName = os.path.join(save_path, name_of_file + ".txt")
        lecture.link =(completeName)
        lecture.save()
        file1 = open(completeName, "w")
        toFile = dataToSave
        file1.write(toFile)
        file1.close()

        all_lectures = Lecture.objects.filter(course_id=pk_course)
        return render_to_response('kosme/allLectures.html', {'all_lectures': all_lectures, 'course_id': pk_course})


def lectureID(request,pk_course,pk_lect):
    lecture = Lecture.objects.filter(id=pk_lect)[0]
    myfile = open(lecture.link)
    text = myfile.read()
    myfile.close()
    return render_to_response('kosme/lectureShow.html', {'lecture': lecture, 'text': text})

class myText():
    text = ""

def showlecture(request):
    if request.method == "GET":
        lecture = Lecture.objects.filter(id = 10)[0]
        myfile = open(lecture.link)
        text = myfile.read()
        myclass = myText()
        myclass.text = text
        myfile.close()
      #  return HttpResponse(text)
        return render_to_response('kosme/lectureShow.html', {'lecture': lecture, 'text':text})

def courseID(request,pk_course):
    all_lectures = Lecture.objects.filter(course_id = pk_course)
    return render_to_response('kosme/allLectures.html', {'all_lectures': all_lectures,'course_id': pk_course })


@login_required(login_url='kosme:mainPage')
def courses(request):
    all_courses = Course.objects.all()
    return render_to_response('kosme/allCourses.html', {'all_courses': all_courses})

#___________________________________________________________________

def signup(request):
    if request.user.is_authenticated():
        return redirect('kosme:userIndex')
    else:
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = User.objects._create_user(username, request.POST['email'], raw_password,
                                                 first_name=request.POST['first_name'],
                                                 last_name=request.POST['last_name'])
                profile = Profile(user=user)
                profile.save()
                return redirect('kosme:signin')
        else:
            form = SignUpForm()
        return render(request, 'kosme/signup.html', {'form': form})

@login_required(login_url='kosme:mainPage')
def profile(request):
    return render(request, 'kosme/profile.html')

@login_required(login_url='kosme:mainPage')
def user_index(request):
    return render(request, 'kosme/userIndex.html')

@login_required(login_url='kosme:mainPage')
def log_out(request):
    logout(request)
    return redirect('kosme:mainPage')

@login_required(login_url='kosme:mainPage')
def user_class(request):
    students = None
    cname = None
    if Student.objects.filter(user=request.user).exists():
        mclass = Student.objects.get(user=request.user).schoolClass
        students = Student.objects.filter(schoolClass=mclass)
        cname = mclass.name
    return render(request, 'kosme/userClass.html', context={'students': students, 'cname': cname})

@login_required(login_url='kosme:mainPage')
def quiz(request):
    if not request.user.profile.is_teacher:
        return redirect('kosme:mainPage')
    else:
        if request.method == 'POST':
            mdata = request.POST["Json"]
            name = request.POST["quiz_name"]
            jdata =  ''.join(mdata.split())
            quiz_elem = Quiz(name=name, data= jdata)
            quiz_elem.save()
            messages.success(request,'Quiz saved')
    return render(request, 'kosme/quizCreate.html')

def delete_quiz(request, pk_quiz):
    Quiz.objects.get(id = pk_quiz).delete()
    return redirect('kosme:allQuizes')

def show_quiz(request, pk_quiz):
    if request.method == 'POST':
        result = request.POST["Json"]
        print(result)
        r = json.loads(result)
    quiz = Quiz.objects.get(id=pk_quiz)
    mainJSON = quiz.data
    qname = quiz.name
    return render(request, 'kosme/quizShow.html', {'mainJSON': mainJSON, 'qname': qname})

def edit_quiz(request, pk_quiz):
    if not request.user.profile.is_teacher:
        return redirect('kosme:mainPage')
    else:
        if request.method == 'POST':
            mdata = request.POST["Json"]
            quiz_elem = Quiz.objects.get(id=pk_quiz)
            quiz_elem.name = request.POST["quiz_name"]
            quiz_elem.data = ''.join(mdata.split())
            quiz_elem.save()
            messages.success(request,'Quiz saved')
    quiz = Quiz.objects.get(id=pk_quiz)
    mainJSON = quiz.data
    qname = quiz.name
    return render(request, 'kosme/quizEdit.html', {'mainJSON': mainJSON, 'qname': qname})

def signin(request):
    if request.user.is_authenticated():
            return redirect('kosme:userIndex')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            raw_password = request.POST['password']
            if User.objects.filter(username=username).exists():
                user = User.objects.get(username=username)
                if not user.profile.is_blocked:
                        user = authenticate(username=username, password=raw_password)
                        login(request, user)
                        return redirect('kosme:userIndex')
                else:
                    messages.warning(request, "Wait for approval")
                    return redirect('kosme:mainPage')
            else:
                return redirect('kosme:signin')

        else:
            form = UserForm()
            return render(request, 'kosme/login.html', {'form': form})

def allQuizes(request):
    all_quizes = Quiz.objects.all()
    print(all_quizes)
    return render(request, 'kosme/allQuizes.html', {'all_quizes': all_quizes})

def mainPage(request):
    if request.user is not None:
        if request.user.is_authenticated():
                return redirect('kosme:userIndex')
    return render_to_response('kosme/mainPage.html')
