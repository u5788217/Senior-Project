from django.shortcuts import render
from django.http import HttpResponse

def login(request):
    return render(request, 'login.html')

def index(request):
    return render(request, 'index.html')

def logout(request):
    #clear session
    return render(request, 'login.html')

def patientrecord(request):
    return render(request, 'patient-records.html')

def followupnew(request):
    return render(request, 'followup-add.html')

def enrollmentdetail(request):
    return render(request, 'enrollment-add.html')
