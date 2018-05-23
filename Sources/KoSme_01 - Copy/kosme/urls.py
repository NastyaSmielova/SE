from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib import admin
from . import views

app_name = 'kosme'

urlpatterns = [
    url(r'^admin/',admin.site.urls),
    url(r'^mainPage/',views.mainPage, name='mainPage'),
   # url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^courses/$', views.courses, name='courses'),
    url(r'^course/(?P<pk_course>\d+)$', views.courseID, name='courseID'),
    #url(r'^course/(?P<pk_course>\d+)/lectures/$', views.lectures, name='lectures'),
    url(r'^course/(?P<pk_course>\d+)/lecture/(?P<pk_lect>\d+)$', views.lectureID, name='lectureID'),
    url(r'^course/(?P<pk_course>\d+)/lecture/create$', views.lectureCreate, name='lectureCreate'),
    url(r'^lecture/(?P<pk_lect>\d+)/edit$', views.lectureIDEdit, name='lectureIDEdit'),
  #  url(r'^lecture/$', views.lecture, name='lecture'),
 #   url(r'^showLecture/$', views.showlecture, name='showLecture'),


    url(r'^quiz/$', views.quiz, name='quiz'),
    url(r'^logout/$', views.log_out, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^user/profile/$', views.profile, name="profile"),
    url(r'^signin/$', views.signin, name="signin"),
    url(r'^user/$', views.user_index, name="userIndex"),
    url(r'^user/class$', views.user_class, name="userClass"),
    url(r'^user/quiz_all/$', views.allQuizes, name="allQuizes"),
    url(r'^user/(?P<pk_quiz>\d+)/show$', views.show_quiz, name="showQuiz")


]