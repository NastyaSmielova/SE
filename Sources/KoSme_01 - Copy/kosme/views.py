from kosme.forms import SignUpForm, UserForm
from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt

import requests

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from collections import defaultdict


def getTeacher(request):
    return Teacher.objects.get(user_id=request.user.profile.user_id)

def isAuthor(teacher,course):
    return course.author_id == teacher.id

SERVERHOST = "http://127.0.0.1:8800"

def saveToServer(type,id,dataToSave):
    link = createLink(type=type,id=id)
    r = requests.put(url=link, data=dataToSave)


def createLink(type,id):
    return SERVERHOST +'/'+ type + str(id)

def getData(link):
    return requests.get(url=link).text

@login_required(login_url='kosme:mainPage')
@csrf_exempt
def lectureIDEdit(request,pk_course,pk_lect):
    course = Course.objects.filter(id=pk_course)
    if not course:
        return render(request,'kosme/404Page.html', {'error_message': "Такого предмету не існує"})
    course = course[0]
    teacher = getTeacher(request)
    if not isAuthor(teacher,course):
        return render(request,'kosme/404Page.html', {'error_message': "Це не ваш предмет"})
    if request.user.profile.is_teacher:
        if request.method == "GET":

                lectures = Lecture.objects.filter(id=pk_lect)
                if not lectures:
                    return render(request,'kosme/404Page.html', {'error_message': "Такої лекції не існує."})
                lecture = lectures[0]
                return render(request,'kosme/lectureEdit.html', {'lecture': lecture})

        if request.method == 'POST':
            return redirect('kosme:courses')

    else:
        return redirect('kosme:mainPage')



@login_required(login_url='kosme:mainPage')
@csrf_exempt
def lectureCreate(request,pk_course):
    course = Course.objects.filter(id=pk_course)
    if not course:
        return render(request,'kosme/404Page.html', {'error_message': "Такого предмету не існує"})
    course = course[0]
    teacher = getTeacher(request)
    if not isAuthor(teacher,course):
        return render(request,'kosme/404Page.html', {'error_message': "Це не ваш предмет"})
    if request.user.profile.is_teacher:
        if request.method == "GET":
            return render(request,'kosme/lectureCreate.html')

        if request.method == 'POST':
            dataToSave = request.POST.get("HTMLtoPDF", "").encode("utf-8")
            fileName = request.POST.get("fileName", "")
            lecture = Lecture()
            lecture.name = fileName
            lecture.course_id = pk_course
            lecture.save()
            lecture.link = createLink('lecture',lecture.id)
            lecture.save()
            saveToServer('lecture',lecture.id,dataToSave)
            return redirect('kosme:mainPage')
    else:  return redirect('kosme:mainPage')

@login_required(login_url='kosme:mainPage')
def lectureID(request,pk_course,pk_lect):
    lecture = Lecture.objects.filter(id=pk_lect)
    if not lecture:
        return render(request,'kosme/404Page.html', {'error_message': "Такої лекції не існує"})
    lecture = lecture[0]
    return render(request,'kosme/lectureShow.html', {'lecture': lecture})

@login_required(login_url='kosme:mainPage')
def lectureIDDelete(request,pk_course, pk_lect):
    course = Course.objects.filter(id=pk_course)
    if not course:
        return render(request,'kosme/404Page.html', {'error_message': "Такого предмету не існує"})
    Lecture.objects.filter(id=pk_lect)[0].delete()
    return redirect("kosme:courseID",pk_course)



@login_required(login_url='kosme:mainPage')
def courseID(request,pk_course):
    course = Course.objects.filter(id=pk_course)
    if not course:
        return render(request,'kosme/404Page.html', {'error_message': "Такого предмету не існує"})
    course = course[0]
    if request.user.profile.is_teacher:
        teacher = getTeacher(request)
        if not course.author_id == teacher.id:
            return render(request,'kosme/404Page.html', {'error_message': "Це не ваш предмет"})
        all_lectures = Lecture.objects.filter(course_id = pk_course)
        all_quizes = Quiz.objects.filter(course_id=pk_course)
    else:
        all_lectures = Lecture.objects.filter(course_id=pk_course)
        all_quizes = Quiz.objects.filter(course_id=pk_course)
    return render(request,'kosme/allLectures.html', {"all_quizes": all_quizes,'all_lectures': all_lectures,'course_id': pk_course , 'user':request.user})


@login_required(login_url='kosme:mainPage')
def courses(request):
    if request.user.profile.is_blocked:
        return redirect("kosme:mainPage")
    else:
        if request.user.profile.is_teacher:
            teacher = Teacher.objects.get(user_id = request.user.profile.user_id)
            all_courses = Course.objects.filter(author_id= teacher.id)
            return render(request,'kosme/allCourses.html', {'all_courses': all_courses, 'user':request.user})
        else:
            student = Student.objects.filter(user_id=request.user.profile.user_id)[0]
            schoolClass = SchoolClass.objects.filter(id=student.schoolClass.id)[0]
            all_courses = Course.objects.all()
            courses =[]
            for course in all_courses:
                if schoolClass in course.classes.all():
                    courses.append(course)
            return render(request,'kosme/allCourses.html', {'all_courses': courses, 'user': request.user})

@login_required(login_url='kosme:mainPage')
def results(request,pk_qiuz):
    if request.user.profile.is_blocked:
        return redirect("kosme:mainPage")
    else:
        if request.user.profile.is_teacher:
            results = Result.objects.filter(quiz_id=pk_qiuz)
            return render(request,'kosme/results.html', {'all_results': results})
        else:

            return render(request,'kosme/404Page.html', {'error_message': "Ви не викладач"})



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


def signin(request):
    if request.user.is_authenticated():
            return redirect('kosme:userIndex')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            raw_password = request.POST['password']
            if User.objects.filter(username=username).exists():
                user = User.objects.get(username=username)
                if Profile.objects.filter(user=user).exists():
                    if not user.profile.is_blocked:
                            user = authenticate(username=username, password=raw_password)
                            if user is not None:
                                login(request, user)
                                return redirect('kosme:userIndex')
                            else:
                                messages.error(request, "Введено неправильний пароль")
                                return redirect('kosme:signin')
                    else:
                        messages.error(request, "Чекайте підтвердження від адміністратора")
                        return redirect('kosme:signin')
                else:
                    return render_to_response('kosme/404Page.html',
                                              {'error_message': "Виникла помилка аккаунта. Зверніться до адміністратора."})
            else:
                messages.error(request, "Неправильні дані. Користувача з заданим логіном не існує.")
                return redirect('kosme:signin')

        else:
            form = UserForm()
            return render(request, 'kosme/login.html', {'form': form})


def mainPage(request):
    if request.user is not None:
        if request.user.is_authenticated():
                return redirect('kosme:userIndex')
    return render(request,'kosme/mainPage.html')

#______________________________________________________#

@login_required(login_url='kosme:mainPage')
def quiz(request, pk_course):
    if not request.user.profile.is_teacher:
        return redirect('kosme:mainPage')
    else:
        if request.method == 'POST':
            mdata = request.POST["Json"].encode('utf-8')
            name = request.POST["quiz_name"].encode('utf-8')
           # jdata =  ''.join(mdata.split())
            quiz_elem = Quiz(name=name,data="", course=Course.objects.get(id=pk_course))
            quiz_elem.save()

            link = createLink('quiz',id = quiz_elem.id)
            quiz_elem.data = link
            quiz_elem.save()
            saveToServer('quiz',quiz_elem.id,mdata)
            messages.success(request,'Quiz saved')
    return render(request, 'kosme/quizCreate.html')

def delete_quiz(request, pk_quiz):
    quiz = Quiz.objects.get(id = pk_quiz)
    pk_course = quiz.course_id
    quiz.delete()
    return redirect('kosme:courseID', pk_course)

def is_completed_quiz(request, quiz):
    student = Student.objects.get(user_id = request.user)
    return  student.result_set.filter(quiz = quiz).exists()

def is_wrong_student_quiz(request,quiz):
    student = Student.objects.get(user_id=request.user)
    return student.schoolClass.course_set.filter(id=quiz.course_id).exists()


@login_required(login_url='kosme:mainPage')
def show_quiz(request, pk_quiz):
    if request.method == 'POST':
        result = request.POST["result"]
        print(result)
        nstudent = Student.objects.get(user=request.user)
        result = Result(student = nstudent, points=result)
        result.quiz_id = pk_quiz
        result.save()
       # quiz = Quiz.objects.get(id=pk_quiz)
       #  quiz.results = result
       #  quiz.save()
        return redirect('kosme:mainPage')
    else:
        if request.user.profile.is_teacher:
            quiz = Quiz.objects.get(id=pk_quiz)
            mainJSON = getData(quiz.data)
            qname = quiz.name
            return render(request, 'kosme/quizShow.html', {'mainJSON': mainJSON, 'qname': qname})
        else:
            nstudent = Student.objects.get(user=request.user)
            results = Result.objects.filter(student_id=nstudent.id)
            pks=[]
            pks.append(pk_quiz)
            for result in results:
                pks.append(result.quiz_id)
                if str(result.quiz_id) == pk_quiz:
                    return render_to_response('kosme/404Page.html',{'error_message':"Ви вже проходили цей тест"})
            quiz = Quiz.objects.get(id=pk_quiz)
            mainJSON = getData(quiz.data)
            qname = quiz.name
            return render(request, 'kosme/quizShow.html', {'mainJSON': mainJSON, 'qname': qname})


def is_wrong_teacher_quiz(request, quiz):
    teacher = Teacher.objects.get(user_id=request.user.profile.user_id)
    if quiz.course.author.id == teacher.id:
        return False
    else:
        return True


@login_required(login_url='kosme:mainPage')
def user_statistics(request):
    if request.user.profile.is_teacher:
        redirect('kosme:userIndex')
    else:
        school_class = SchoolClass.objects.get(student__user = request.user)
        courses = school_class.course_set.all()
        return render(request, 'kosme/userStatistics.html', {'courses': courses})


@login_required(login_url='kosme:mainPage')
def edit_quiz(request, pk_quiz):
    quiz = Quiz.objects.get(id=pk_quiz)
    if not request.user.profile.is_teacher:
        return redirect('kosme:mainPage')
    else:
        # по моей логике преподаватель не может проходить тесты
        if is_wrong_teacher_quiz(request, quiz):
            return render_to_response('kosme/404Page.html', {'error_message': "Ви не можете редагувати цей тест"})
        elif request.method == 'POST':
            mdata = request.POST["Json"].encode('utf-8')
            quiz = Quiz.objects.get(id=pk_quiz)
            quiz.name = request.POST["quiz_name"].encode('utf-8')
            #??? quiz.data = ''.join(mdata.split())
            saveToServer('quiz',quiz.id,mdata)
            quiz.save()
            messages.success(request,'Тест збережено')
    mainJSON =  getData(quiz.data)
    qname = quiz.name
    return render(request, 'kosme/quizEdit.html', {'mainJSON': mainJSON, 'qname': qname})

def allQuizes(request):
    all_quizes = Quiz.objects.all()
    return render(request, 'kosme/allQuizes.html', {'all_quizes': all_quizes})
