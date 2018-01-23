from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('', views.logout, name='logout'),
    path('index/', views.index, name='index'),
    path('patientrecord/<str:studynum>/', views.patientrecord, name='patientrecord'),
    path('patientrecord/', views.patientrecord, name='patientrecord'),
    path('followupnew/<str:studynum>/', views.followupnew, name='followupnew'),
    path('followupnew/', views.followupnew, name='followupnew'),
    path('enroll/', views.enrollAdd, name='EnrollAdd'),
    path('enrollPatient/<str:studynum>/', views.enrollPatient, name='EnrollPatient'),
    path('enrollPatient/', views.enrollPatient, name='EnrollPatient'),
    path('followPatient/<str:visitid>/', views.followPatient, name='FollowPatient'),
    path('followPatient/', views.followPatient, name='FollowPatient'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
