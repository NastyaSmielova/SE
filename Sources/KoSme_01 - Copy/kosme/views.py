from django.http import HttpResponseRedirect
from django.views import generic
from kosme.forms import SignUpForm, UserForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .models import *
from rest_framework.utils import json
from django.contrib import messages
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
import os.path
from django.http import HttpResponse
from django.utils.safestring import mark_safe
# Create your views here.
import socket
import re

import urllib.request
import requests
# from poster.encode import multipart_encode
# from poster.streaminghttp import register_openers

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate

import pdfkit


@login_required(login_url='kosme:mainPage')
@csrf_exempt
def lectureIDEdit(request,pk_lect):
        if request.method == "GET":
            lecture = Lecture.objects.filter(id=pk_lect)[0]
         #   text = urllib.request.urlopen('http://127.0.0.1:8800/newOne.txt').read()#lecture.link).read()# open(lecture.link)
          #  text = myfile.read()
          #  myfile.close()
       #     contents = urllib.request.urlopen("http://127.0.0.1:8800/q15.txt").read()


            # HOST = 'http://127.0.0.1'
            # PORT = 8800
            # ADDR = (HOST, PORT)
            #
            # client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # client.connect(ADDR)
            # client.write_message('\0' * 8000, True)
            # client.write_message('nklnlknlknlkn')
            #
            # client.write_message('\0' * 8000, True)
            #
            # client.close()

            return render_to_response('kosme/lectureEdit.html', {'lecture': lecture, 'text': ""})
        if request.method == 'POST':
            # dataToSave = request.POST.get("HTMLtoPDF", "")
            # save_path = 'C:/users/pc/Desktop/KoSmeShool'
            #
            # lecture = Lecture.objects.filter(id = pk_lect)[0]
            # fullName = lecture.name + ".txt"
            # completeName = os.path.join(save_path, fullName)
            # lecture.save()
            # file1 = open(completeName, "w")
            # toFile = dataToSave
            # file1.write(toFile)
            # file1.close()


            return redirect('kosme:courses')



@login_required(login_url='kosme:mainPage')
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
        fullName   = name_of_file + ".txt"
        completeName = os.path.join(save_path, fullName)
        lecture.link =('http://127.0.0.1:8800/'+fullName)
        lecture.save()
        # file1 = open(completeName, "w")
        # toFile = dataToSave
        # file1.write(toFile)
        # file1.close()
      #  register_openers()

        # url = 'http://127.0.0.1:8800/'
        # files = {'file': open('additional.txt','r')}
        # r = requests.put(url, data={'file': open('additional.txt','r')})

        return redirect('kosme:mainPage')

@login_required(login_url='kosme:mainPage')
def lectureID(request,pk_course,pk_lect):
    lecture = Lecture.objects.filter(id=pk_lect)[0]
   # text = urllib.request.urlopen('http://127.0.0.1:8800/newOne.txt').read()#    text = myfile.read()
  #  myfile.close()
    return render_to_response('kosme/lectureShow.html', {'lecture': lecture, 'text': ""})


@login_required(login_url='kosme:mainPage')
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
            print("reached")
    return render(request, 'kosme/quizCreate.html')

def show_quiz(request, pk_quiz):
    quiz = Quiz.objects.get(id=pk_quiz)
    mainJSON = quiz.data
    return render(request, 'kosme/quizShow.html', {'mainJSON': mainJSON})

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
