from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('', views.logout, name='logout'),
    path('index/', views.index, name='index'),
    path('patientrecord/', views.patientrecord, name='patientrecord'),
    path('followupnew/', views.followupnew, name='followupnew'),
    path('enrollmentdetail/', views.enrollmentdetail, name='enrollmentdetail'),
#    path('followupdetail/', views.followupdetail, name='followupdetail'),
    path('enroll/', views.enrollAdd, name='EnrollAdd'),
    path('enrollPatient/', views.enrollPatient, name='EnrollPatient'),
    path('followPatient/', views.followPatient, name='FollowPatient'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
