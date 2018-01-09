from django.shortcuts import render
from django.http import HttpResponse

from .models import Studyidentity
from .models import Slicccriteria
from .models import Medicalcondition
from .models import Acrcriteria

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
    return render(request, 'enrollment-detail.html')

def enrollAdd(request):
    return render(request, 'enrollment-add.html')

def enrollPatient(request):
    if request.method == "POST":
        #All data feilds
  #      EnrollStudyidentity = Studyidentity(dateofdiagnosis = request.POST.get('dateofdiagnosis', ''),
  #                              dateofenrollment = request.POST.get('dateofenrollment', ''),
  #                              gender = request.POST.get('gender', ''),
  #                              dateofbirth = request.POST.get('dateofbirth', ''),
  #                              religion = request.POST.get('religion', ''),
  ##                              education = request.POST.get('education', ''),
  #                              maritalstatus = request.POST.get('maritalstatus', ''),
  #                              region = request.POST.get('region', ''),
   #                             occupation = request.POST.get('occupation', ''),
   #                             income = request.POST.get('income', ''))
        #print(EnrollStudyidentity)
        #EnrollStudyidentity.save()
        #StudyNumber = EnrollStudyidentity.studynumber
        EnrollSlicccriteria = Slicccriteria(slicc1 = request.POST.get('slicc1', ''),
                                            slicc2 = request.POST.get('slicc2', ''),
                                            slicc3 = request.POST.get('slicc3', ''),
                                            slicc4 = request.POST.get('slicc4', ''),
                                            slicc5 = request.POST.get('slicc5', ''),
                                            slicc6 = request.POST.get('slicc6', ''),
                                            slicc7 = request.POST.get('slicc7', ''),
                                            slicc8 = request.POST.get('slicc8', ''),
                                            slicc9 = request.POST.get('slicc9', ''),
                                            slicc10 = request.POST.get('slicc10', ''),
                                            slicc11 = request.POST.get('slicc11', ''),
                                            slicc12 = request.POST.get('slicc12', ''),
                                            slicc13 = request.POST.get('slicc13', ''),
                                            slicc14 = request.POST.get('slicc14', ''),
                                            slicc15 = request.POST.get('slicc15', ''),
                                            slicc16 = request.POST.get('slicc16', ''),
                                            slicc17 = request.POST.get('slicc17', ''))
        #EnrollAcrcriteria = Acrcriteria()
        #EnrollMedicalcondition = Medicalcondition()
    return render(request, 'enrollment-detail.html',{'EnrollSlicccriteria': EnrollSlicccriteria.slicc1})

#def followPatient(request):
 #   if request.method == "POST":
        #All data feilds
  #  return render(request, 'SLE/followup-detail')