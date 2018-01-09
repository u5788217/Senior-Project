from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('', views.logout, name='logout'),
    path('index/', views.index, name='index'),
    path('patientrecord/', views.patientrecord, name='patientrecord'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
