from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns=[
    path('admin',admin.site.urls),
    path('', HomePage, name='HomePage'),
    path('LoginPage', LoginPage, name='LoginPage'),
    path('PasswordPage', PasswordPage, name='PasswordPage'),
    path('register', RegisterPage, name='RegisterPage'),
    path('DashboardPage', DashboardPage, name='DashboardPage'),
    path('EditProfile', EditProfile, name='EditProfile'),
    path('Complogin', Complogin, name='Complogin'),
    path('CompPass', CompPass, name='CompPass'),
    path('CompReg', CompReg, name='CompReg'),
    path('CompDash', CompDash, name='CompDash'),
    path('PostJob', PostJob, name='PostJob'),
    path('joblist', Joblist, name='Joblist'),
    path('jobdetails/<int:job_id>', JobDetails, name='JobDetails'),
    path('applyjob/<int:job_id>', ApplyJob, name='ApplyJob'),
    path('SearchJob', SearchJob, name='SearchJob'),
    path('PostedJobs', PostedJobs, name='PostedJobs'),
    path('MyJobs', MyJobs, name='MyJobs'),
    path('ViewProfile', ViewProfile, name='ViewProfile'),
    path('DeleteProfile', DeleteProfile, name='DeleteProfile'),
    path('DeleteAppliedJob/<int:application_id>', DeleteAppliedJob, name='DeleteAppliedJob'),
    path('logout', logout, name='logout'),
    path('UpdateJob/<int:job_id>', UpdateJob, name='UpdateJob'),
    path('DeleteJob/<int:job_id>', DeleteJob, name='DeleteJob'),
    path('Applicants', Applicants, name='Applicants'),
    path('UpdateStatus/<int:app_id>', UpdateStatus, name='UpdateStatus'),
    path('DeleteApplication/<int:app_id>', DeleteApplication, name='DeleteApplication'),
    path('Complogout', Complogout, name='Complogout'),

]