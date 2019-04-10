"""HostelManagementPortal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from . import views

app_name='student'

urlpatterns = [
    url(r'^$', views.Home, name='homepage'),
    url(r'^hostel/(?P<pk>[0-9]+)/$', views.Hostel_View, name='hostel_view'),
    url(r'^hostel/login/$', views.HostelLoginView, name='hostellogin'),
    url(r'^hostel/addnotification/$', views.AddNotification, name='addnotification'),
    url(r'^hostel/removenotification/(?P<pk>[0-9]+)/$', views.DeleteNotification, name='removenotification'),
    url(r'^hostel/updateinfo/$', views.UpdateHostel, name='updatehostel'),
    url(r'^logout/$', views.LogoutView, name='logoutview'),
    url(r'^register/resend_validation/$', views.ResendMail, name='resendmail'),
    url(r'^student/profile/$', views.StudentProfile, name='studentprofile'),
    url(r'^student/login/$', views.StudentLogin, name='studentlogin'),
    url(r'^student/changepassword/$', views.ChangePassword, name='changepass'),
    url(r'^student/forgot-password/$', views.ForgotPassword, name='forgot-password'),
    url(r'^student/register/$', views.StudentRegister, name='studentregister'),
    url(r'^student/checkmail/$', views.CheckMailView),
    url(r'^student/addgrievance/$', views.AddGrievance, name='addgrievance'),
    url(r'^student/allotroom/$', views.AllotRoom, name='allotroom'),
    url(r'^student/grievances/$', views.ViewStudentGrievances, name='viewstudentgrievances'),
    url(r'^hostel/grievances/$', views.ViewHostelGrievances, name='viewhostelgrievances'),
    url(r'^hostel/grievance/(?P<pk>[0-9]+)/$', views.ViewGrievanceDetail, name='viewgrievancedetail'),
    url(r'^lostandfound/$', views.ViewLostFound, name='viewlostfound'),
    url(r'^addlostfound/$', views.AddLostFound, name='addlostfound'),
    url(r'^lostfound/(?P<pk>[0-9]+)/$', views.ViewLostFoundDetail, name='viewlostfound'),
]
