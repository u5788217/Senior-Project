from django.shortcuts import render
from django.http import HttpResponse

#Models for enrollment
from .models import Studyidentity, Slicccriteria, Acrcriteria, Medicalcondition

def login(request):
    return render(request, 'login.html')

def index(request):
    #if request.method == "POST": return username
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
        #create studynumber+1
        stnum = 2
        EnrollStudyidentity = Studyidentity(studynumber = stnum,
                                dateofdiagnosis = request.POST.get('dateofdiagnosis', ''),
                                dateofenrollment = request.POST.get('dateofenrollment', ''),
                                gender = request.POST.get('gender', ''),
                                dateofbirth = request.POST.get('dateofbirth', ''),
                                religion = request.POST.get('religion', ''),
                                education = request.POST.get('education', ''),
                                maritalstatus = request.POST.get('maritalstatus', ''),
                                region = request.POST.get('region', ''),
                                occupation = request.POST.get('occupation', ''),
                                income = request.POST.get('income', ''))
        EnrollStudyidentity.save()
        
        EnrollSlicccriteria = Slicccriteria(studynumber = EnrollStudyidentity,
                                            slicc1 = 'True' if request.POST.get('slicc1', '') == '1' else 'False',
                                            slicc2 = 'True' if request.POST.get('slicc2', '') == '1' else 'False',
                                            slicc3 = 'True' if request.POST.get('slicc3', '') == '1' else 'False',
                                            slicc4 = 'True' if request.POST.get('slicc4', '') == '1' else 'False',
                                            slicc5 = 'True' if request.POST.get('slicc5', '') == '1' else 'False',
                                            slicc6 = 'True' if request.POST.get('slicc6', '') == '1' else 'False',
                                            slicc7 = 'True' if request.POST.get('slicc7', '') == '1' else 'False',
                                            slicc8 = 'True' if request.POST.get('slicc8', '') == '1' else 'False',
                                            slicc9 = 'True' if request.POST.get('slicc9', '') == '1' else 'False',
                                            slicc10 = 'True' if request.POST.get('slicc10', '') == '1' else 'False',
                                            slicc11 = 'True' if request.POST.get('slicc11', '') == '1' else 'False',
                                            slicc12 = 'True' if request.POST.get('slicc12', '') == '1' else 'False',
                                            slicc13 = 'True' if request.POST.get('slicc13', '') == '1' else 'False',
                                            slicc14 = 'True' if request.POST.get('slicc14', '') == '1' else 'False',
                                            slicc15 = 'True' if request.POST.get('slicc15', '') == '1' else 'False',
                                            slicc16 = 'True' if request.POST.get('slicc16', '') == '1' else 'False',
                                            slicc17 = 'True' if request.POST.get('slicc17', '') == '1' else 'False')
        EnrollSlicccriteria.save()
        EnrollAcrcriteria = Acrcriteria(studynumber = EnrollStudyidentity,
                                        acr1 = 'True' if request.POST.get('acr1', '')== '1' else 'False',
                                        acr2 = 'True' if request.POST.get('acr2', '')== '1' else 'False',
                                        acr3 = 'True' if request.POST.get('acr3', '')== '1' else 'False',
                                        acr4 = 'True' if request.POST.get('acr4', '')== '1' else 'False',
                                        acr5 = 'True' if request.POST.get('acr5', '')== '1' else 'False',
                                        acr6 = 'True' if request.POST.get('acr6', '')== '1' else 'False',
                                        acr7 = 'True' if request.POST.get('acr7', '')== '1' else 'False',
                                        acr8 = 'True' if request.POST.get('acr8', '')== '1' else 'False',
                                        acr9 = 'True' if request.POST.get('acr9', '')== '1' else 'False',
                                        acr10 = 'True' if request.POST.get('acr10', '')== '1' else 'False',
                                        acr11 = 'True' if request.POST.get('acr11', '')== '1' else 'False')
        EnrollAcrcriteria.save()
        #EnrollMedicalcondition = Medicalcondition()
    return render(request, 'enrollment-detail.html',{'EnrollSlicccriteria': EnrollSlicccriteria.slicc1})

#def followPatient(request):
 #   if request.method == "POST":
        #All data feilds
  #  return render(request, 'SLE/followup-detail')