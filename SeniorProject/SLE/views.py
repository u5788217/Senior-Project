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
        EnrollMedicalcondition = Medicalcondition(studynumber = EnrollStudyidentity,
    mc1_1 = check
    mc1_2 = 'True' if request.POST.get('mc1_2', '')== '1' else 'False',
    mc1_3 = 'True' if request.POST.get('mc1_3', '')== '1' else 'False',
    mc1_4 = 'True' if request.POST.get('mc1_4', '')== '1' else 'False',
    mc1_5 = 'True' if request.POST.get('mc1_5', '')== '1' else 'False',
    mc1_6 = 'True' if request.POST.get('mc1_6', '')== '1' else 'False',
    mc1_7 = 'True' if request.POST.get('mc1_7', '')== '1' else 'False',
    mc1_8 = 'True' if request.POST.get('mc1_8', '')== '1' else 'False',
    mc1_9 = 'True' if request.POST.get('mc1_9', '')== '1' else 'False',
    mc1_10 = 'True' if request.POST.get('mc1_10', '')== '1' else 'False',
    mc1_11 = 'True' if request.POST.get('mc1_11', '')== '1' else 'False',
    mc2_1 = check
    mc2_2 = 'True' if request.POST.get('mc2_2', '')== '1' else 'False',
    mc2_3 = 'True' if request.POST.get('mc2_3', '')== '1' else 'False',
    mc2_4 = 'True' if request.POST.get('mc2_4', '')== '1' else 'False',
    mc2_5 = 'True' if request.POST.get('mc2_5', '')== '1' else 'False',
    mc2_6 = 'True' if request.POST.get('mc2_6', '')== '1' else 'False',
    mc3_1 = check
    mc3_2 = 'True' if request.POST.get('mc3_2', '')== '1' else 'False',
    mc3_3 = 'True' if request.POST.get('mc3_3', '')== '1' else 'False',
    mc3_4 = 'True' if request.POST.get('mc3_4', '')== '1' else 'False',
    mc3_5 = 'True' if request.POST.get('mc3_5', '')== '1' else 'False',
    mc4_1 = check
    mc4_2 = 'True' if request.POST.get('mc4_2', '')== '1' else 'False',
    mc4_3 = 'True' if request.POST.get('mc4_3', '')== '1' else 'False',
    mc4_4 = 'True' if request.POST.get('mc4_4', '')== '1' else 'False',
    mc4_5 = 'True' if request.POST.get('mc4_5', '')== '1' else 'False',
    mc4_6 = 'True' if request.POST.get('mc4_6', '')== '1' else 'False',
    mc4_7 = 'True' if request.POST.get('mc4_7', '')== '1' else 'False',
    mc4_8 = 'True' if request.POST.get('mc4_8', '')== '1' else 'False',
    mc4_9 = ArrayField(models.CharField(max_length=20), blank=True)  # This field type is a guess. --> now it is array.
    mc5_1 = check
    mc5_2 = check
    mc5_2_1 = models.CharField(max_length=200, blank=True, null=True)
    mc5_2_2 = models.DateField(blank=True, null=True)
    mc5_2_3 = models.DateField(blank=True, null=True)
    mc5_3 = check
    mc5_3_1 = models.CharField(max_length=200, blank=True, null=True)
    mc5_3_2 = models.DateField(blank=True, null=True)
    mc5_3_3 = models.DateField(blank=True, null=True)
    mc5_4 = check
    mc5_4_1 = models.DateField(blank=True, null=True)
    mc5_4_2 = models.DateField(blank=True, null=True)
    mc5_5 = check
    mc5_5_1 = models.DateField(blank=True, null=True)
    mc5_5_2 = models.DateField(blank=True, null=True)
                                                 )
        EnrollMedicalcondition.save()
    return render(request, 'enrollment-detail.html',{'EnrollSlicccriteria': EnrollSlicccriteria.slicc1})

#def followPatient(request):
 #   if request.method == "POST":
        #All data feilds
  #  return render(request, 'SLE/followup-detail')