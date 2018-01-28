from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required

from django.utils.timezone import datetime

#Models for enrollment
from .models import Studyidentity, Slicccriteria, Acrcriteria, Medicalcondition, Previousorganinvolvement, Previouscomplication, Familyhistory
from .models import Labtype, Medicationtype, Previoustype
from .models import Visiting, Clinicalpresentation, Damageindex, Diseaseactivitysledai, Laboratoryinventoryinvestigation, Lnlab, Medication

from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ObjectDoesNotExist

def ListToArray(List):
    Array = []
    for item in List :
        Array.append(item)
    return Array

def ValidateVisiting(studynum, date):
    visit = None
    try:
        visit = Visiting.objects.get(studynumber = studynum, visitdate = date)
        return False
    except ObjectDoesNotExist:
        visit = None
        return True
    
def haslnlab(lab):
    ln = None
    try:
        ln = Lnlab.objects.get(lnlabid = lab.lnlabid) 
        return True
    except ObjectDoesNotExist:
        ln = None
        return False
        
def CheckboxToInt(string):
    if string == 'on' or string == 'Pos': string = 1
    else : 
        if string == 'off' or string == 'Neg' or string == '': string = 0
    return int(string)

def ToFloat(string):
    if string == 'on': string = 1
    else : 
        if string == 'off' or string == '': string = 0
    return float(string)

def CheckboxToBool(string):
    if string == '1' or string == 'on': string = 'True'
    else : string = 'False'
    return string

def DateToNone(date):
    if date == '': date = None
    return date

def login(request):
    if request.user.is_authenticated is True:
        return render(request, 'index.html',{'patients': Studyidentity.objects.all()})
    else :
        return render(request, 'login.html')

def index(request):
    if request.method == "POST": 
        user_auth = request.POST.get('username',)
        user = authenticate(request, username = user_auth, password = request.POST.get('password',))
        if user is not None:
            auth_login(request, user)
            return render(request, 'index.html',{'patients': Studyidentity.objects.all()})
        else:
            return render(request, 'login.html')
    else:
        if request.user.is_authenticated:
            return render(request, 'index.html',{'patients': Studyidentity.objects.all()})
        else:
            return render(request, 'login.html')

def logout(request):
    #clear session
    auth_logout(request)
    return render(request, 'login.html')

@login_required(login_url='login')
def patientrecord(request, studynum):
    return render(request, 'patient-records.html',{'visit_list': Visiting.objects.filter(studynumber = studynum), 'patient':Studyidentity.objects.get(studynumber = studynum)})

@login_required(login_url='login')
def followupnew(request, studynum):
    return render(request, 'followup-add.html',{'patient':Studyidentity.objects.get(studynumber = studynum)})

@login_required(login_url='login')
def enrollAdd(request):
    return render(request, 'enrollment-add.html',)

@login_required(login_url='login')
def enrollPatient(request):
    if request.method == "POST":
        #All data feilds
        #create studynumber+1
        now = str(datetime.now().year+543)
        current_year = now[-2:]+"0000"
        max_id_list = Studyidentity.objects.all().filter(studynumber__gte = current_year)
        max_year = None
        try:
            max_year = int(max_id_list.latest('studynumber').studynumber)+1
        except ObjectDoesNotExist:
            max_year = current_year
   
        stnum = max_year
        EnrollStudyidentity = Studyidentity(studynumber = stnum,
                                dateofdiagnosis =  DateToNone(request.POST.get('dateofdiagnosis', '')),
                                dateofenrollment = DateToNone(request.POST.get('dateofenrollment', '')),
                                gender = request.POST.get('gender', ''),
                                dateofbirth = DateToNone(request.POST.get('dateofbirth', '')),
                                religion = request.POST.get('religion', ''),
                                education = request.POST.get('education', ''),
                                maritalstatus = request.POST.get('maritalstatus', ''),
                                region = request.POST.get('region', ''),
                                occupation = request.POST.get('occupation', ''),
                                income = request.POST.get('income', ''))
        EnrollStudyidentity.save()
        
        EnrollSlicccriteria = Slicccriteria(studynumber = EnrollStudyidentity,
                                            slicc1 = CheckboxToBool(request.POST.get('slicc1', '')),
                                            slicc2 = CheckboxToBool(request.POST.get('slicc2', '')),
                                            slicc3 = CheckboxToBool(request.POST.get('slicc3', '')),
                                            slicc4 = CheckboxToBool(request.POST.get('slicc4', '')),
                                            slicc5 = CheckboxToBool(request.POST.get('slicc5', '')),
                                            slicc6 = CheckboxToBool(request.POST.get('slicc6', '')),
                                            slicc7 = CheckboxToBool(request.POST.get('slicc7', '')),
                                            slicc8 = CheckboxToBool(request.POST.get('slicc8', '')),
                                            slicc9 = CheckboxToBool(request.POST.get('slicc9', '')),
                                            slicc10 = CheckboxToBool(request.POST.get('slicc10', '')),
                                            slicc11 = CheckboxToBool(request.POST.get('slicc11', '')),
                                            slicc12 = CheckboxToBool(request.POST.get('slicc12', '')),
                                            slicc13 = CheckboxToBool(request.POST.get('slicc13', '')),
                                            slicc14 = CheckboxToBool(request.POST.get('slicc14', '')),
                                            slicc15 = CheckboxToBool(request.POST.get('slicc15', '')),
                                            slicc16 = CheckboxToBool(request.POST.get('slicc16', '')),
                                            slicc17 = CheckboxToBool(request.POST.get('slicc17', '')))
        EnrollSlicccriteria.save()
        
        EnrollAcrcriteria = Acrcriteria(studynumber = EnrollStudyidentity,
                                        acr1 = CheckboxToBool(request.POST.get('acr1', '')),
                                        acr2 = CheckboxToBool(request.POST.get('acr2', '')),
                                        acr3 = CheckboxToBool(request.POST.get('acr3', '')),
                                        acr4 = CheckboxToBool(request.POST.get('acr4', '')),
                                        acr5 = CheckboxToBool(request.POST.get('acr5', '')),
                                        acr6 = CheckboxToBool(request.POST.get('acr6', '')),
                                        acr7 = CheckboxToBool(request.POST.get('acr7', '')),
                                        acr8 = CheckboxToBool(request.POST.get('acr8', '')),
                                        acr9 = CheckboxToBool(request.POST.get('acr9', '')),
                                        acr10 = CheckboxToBool(request.POST.get('acr10', '')),
                                        acr11 = CheckboxToBool(request.POST.get('acr11', '')))
        EnrollAcrcriteria.save()

 
        EnrollMedicalcondition = Medicalcondition(studynumber = EnrollStudyidentity,
                mc1_1 = 'True' if request.POST.get('mc1_2', '')== '1' or request.POST.get('mc1_3', '')== '1' or request.POST.get('mc1_4', '')== '1' or request.POST.get('mc1_5', '')== '1' or request.POST.get('mc1_6', '')== '1' or request.POST.get('mc1_7', '')== '1' or request.POST.get('mc1_8', '')== '1' or request.POST.get('mc1_9', '')== '1' or request.POST.get('mc1_10', '')== '1' or request.POST.get('mc1_11', '')== '1' else 'False',
                mc1_2 = CheckboxToBool(request.POST.get('mc1_2', '')),
                mc1_3 = CheckboxToBool(request.POST.get('mc1_3', '')),
                mc1_4 = CheckboxToBool(request.POST.get('mc1_4', '')),
                mc1_5 = CheckboxToBool(request.POST.get('mc1_5', '')),
                mc1_6 = CheckboxToBool(request.POST.get('mc1_6', '')),
                mc1_7 = CheckboxToBool(request.POST.get('mc1_7', '')),
                mc1_8 = CheckboxToBool(request.POST.get('mc1_8', '')),
                mc1_9 = CheckboxToBool(request.POST.get('mc1_9', '')),
                mc1_10 = CheckboxToBool(request.POST.get('mc1_10', '')),
                mc1_11 = CheckboxToBool(request.POST.get('mc1_11', '')),
                mc2_1 = 'True' if request.POST.get('mc2_2', '')== '1' or request.POST.get('mc2_3', '')== '1' or request.POST.get('mc2_4', '')== '1' or request.POST.get('mc2_5', '')== '1' or request.POST.get('mc2_6', '')== '1' else 'False',                                         
                mc2_2 = CheckboxToBool(request.POST.get('mc2_2', '')),
                mc2_3 = CheckboxToBool(request.POST.get('mc2_3', '')),
                mc2_4 = CheckboxToBool(request.POST.get('mc2_4', '')),
                mc2_5 = CheckboxToBool(request.POST.get('mc2_5', '')),
                mc2_6 = CheckboxToBool(request.POST.get('mc2_6', '')),
                mc3_1 = 'True' if request.POST.get('mc3_2', '')== '1' or request.POST.get('mc3_3', '')== '1' or request.POST.get('mc3_4', '')== '1' or request.POST.get('mc3_5', '')== '1' else 'False',  
                mc3_2 = CheckboxToBool(request.POST.get('mc3_2', '')),
                mc3_3 = CheckboxToBool(request.POST.get('mc3_3', '')),
                mc3_4 = CheckboxToBool(request.POST.get('mc3_4', '')),
                mc3_5 = CheckboxToBool(request.POST.get('mc3_5', '')),
                mc4_1 = 'True' if request.POST.get('mc4_2', '')== '1' or request.POST.get('mc4_3', '')== '1' or request.POST.get('mc4_4', '')== '1' or request.POST.get('mc4_5', '')== '1' or request.POST.get('mc4_6', '')== '1' or request.POST.get('mc4_7', '')== '1' or request.POST.get('mc4_8', '')== '1' else 'False',
                mc4_2 = CheckboxToBool(request.POST.get('mc4_2', '')),
                mc4_3 = CheckboxToBool(request.POST.get('mc4_3', '')),
                mc4_4 = CheckboxToBool(request.POST.get('mc4_4', '')),
                mc4_5 = CheckboxToBool(request.POST.get('mc4_5', '')),
                mc4_6 = CheckboxToBool(request.POST.get('mc4_6', '')),
                mc4_7 = CheckboxToBool(request.POST.get('mc4_7', '')),
                mc4_8 = CheckboxToBool(request.POST.get('mc4_8', '')),

                mc4_9 = ListToArray(request.POST.getlist('mc4_9[]',)),

                mc5_1 = 'True' if request.POST.get('mc5_2_1', '')!='' or request.POST.get('mc5_2_2', '')!='' or request.POST.get('mc5_2_3', '')!='' or request.POST.get('mc5_3_1', '')!='' or request.POST.get('mc5_3_2', '')!='' or request.POST.get('mc5_3_3', '')!='' or request.POST.get('mc5_4_1', '')!='' or request.POST.get('mc5_4_2', '')!='' or request.POST.get('mc5_5_1', '')!='' or request.POST.get('mc5_5_2', '')!='' else 'False', 
                mc5_2 = 'True' if request.POST.get('mc5_2_1', '')!='' or request.POST.get('mc5_2_2', '')!='' or request.POST.get('mc5_2_3', '')!='' else 'False', 
                mc5_2_1 = request.POST.get('mc5_2_1', ''),
                mc5_2_2 = DateToNone(request.POST.get('mc5_2_2', '')),
                mc5_2_3 = DateToNone(request.POST.get('mc5_2_3', '')),
                mc5_3 = 'True' if request.POST.get('mc5_3_1', '')!='' or request.POST.get('mc5_3_2', '')!='' or request.POST.get('mc5_3_3', '')!='' else 'False', 
                mc5_3_1 = request.POST.get('mc5_3_1', ''),
                mc5_3_2 = DateToNone(request.POST.get('mc5_3_2', '')),
                mc5_3_3 = DateToNone(request.POST.get('mc5_3_3', '')),
                mc5_4 = 'True' if request.POST.get('mc5_4_1', '')!='' or request.POST.get('mc5_4_2', '')!='' else 'False', 
                mc5_4_1 = request.POST.get('mc5_4_1', ''),
                mc5_4_2 = DateToNone(request.POST.get('mc5_4_2', '')),
                mc5_5 = 'True' if request.POST.get('mc5_5_1', '')!='' or request.POST.get('mc5_5_2', '')!='' else 'False', 
                mc5_5_1 = request.POST.get('mc5_5_1', ''),
                mc5_5_2 = DateToNone(request.POST.get('mc5_5_2', '')))
        EnrollMedicalcondition.save()
        
        OrganDate = request.POST.getlist('OrganDate[]',)
        OrganOrgan = request.POST.getlist('Organ[]',)
        OrganTreat = request.POST.getlist('OrganTreat[]',)
        OrganResult = request.POST.getlist('OrganResult[]',)
        for i in range(0, len(OrganDate)):
            EnrollOrgan = Previousorganinvolvement(studynumber = EnrollStudyidentity, detail = Previoustype(date = DateToNone(OrganDate[i]), organ = OrganOrgan[i], treatment = OrganTreat[i], result = OrganResult[i]))
            EnrollOrgan.save()
        
        CompDate = request.POST.getlist('CompDate[]',)
        CompOrgan = request.POST.getlist('CompOrgan[]',)
        CompTreat = request.POST.getlist('CompTreat[]',)
        CompRemiss = request.POST.getlist('CompRemiss[]',)
        for i in range(0, len(OrganDate)):
            EnrollComp = Previouscomplication(studynumber = EnrollStudyidentity, detail = Previoustype(date = DateToNone(CompDate[i]), organ = CompOrgan[i], treatment = CompTreat[i], result = CompRemiss[i]))
            EnrollComp.save()
            
        EnrollFam = Familyhistory(studynumber = EnrollStudyidentity,
            familyhistoryofautoimmunedisease = request.POST.get('FamAuto',), 
            systemicautoimmune = CheckboxToBool(request.POST.get('systemicautoimmune',)), 
            sle = ListToArray(request.POST.getlist('sle[]',)),
            ra = ListToArray(request.POST.getlist('ra[]',)),
            dermatomyositis = ListToArray(request.POST.getlist('dermatomyositis[]',)),
            systemicsclerosis = ListToArray(request.POST.getlist('systemicsclerosis[]',)),
            sjogrensyndrome = ListToArray(request.POST.getlist('sjogrensyndrome[]',)),
            tissuespecificautoimmune = CheckboxToBool(request.POST.get('tissuespecificautoimmune',)), 
            dmtypeone = ListToArray(request.POST.getlist('dmtypeone[]',)),
            hashimotosthyroiditis = ListToArray(request.POST.getlist('hashimotosthyroiditis[]',)),
            multiplesclerosis = ListToArray(request.POST.getlist('multiplesclerosis[]',)),
            myastheniagravis = ListToArray(request.POST.getlist('myastheniagravis[]',)),
            tissuespecificother = ListToArray(request.POST.getlist('tissuespecificother[]',)),
            renaldiseasefamilyhistory = request.POST.get('FamRenal',),
            nephroticsyndrome_glomerulardisease = ListToArray(request.POST.getlist('nephroticsyndrome_glomerulardisease[]',)),
            stone = ListToArray(request.POST.getlist('stone[]',)),
            esrd = ListToArray(request.POST.getlist('esrd[]',)),
            renalother = ListToArray(request.POST.getlist('renalother[]',)))
        EnrollFam.save()
    
        return render(request, 'enrollment-detail.html',
                {'patient':Studyidentity.objects.get(studynumber = stnum),
                   'acrcriteria':Acrcriteria.objects.get(studynumber = stnum),
                   'slicccriteria':Slicccriteria.objects.get(studynumber = stnum),
                    'familyhistory':Familyhistory.objects.get(studynumber = stnum),
                    'medicalcondition':Medicalcondition.objects.get(studynumber = stnum),
                    'previousorganinvolvement':Previousorganinvolvement.objects.filter(studynumber = stnum),
                    'previouscomplication':Previouscomplication.objects.filter(studynumber = stnum)})

    
    

@login_required(login_url='login')
def enrollDetail(request, studynum):
    return render(request, 'enrollment-detail.html',
                  {'patient':Studyidentity.objects.get(studynumber = studynum),
                   'acrcriteria':Acrcriteria.objects.get(studynumber = studynum),
                   'slicccriteria':Slicccriteria.objects.get(studynumber = studynum),
                    'familyhistory':Familyhistory.objects.get(studynumber = studynum),
                    'medicalcondition':Medicalcondition.objects.get(studynumber = studynum),
                    'previousorganinvolvement':Previousorganinvolvement.objects.filter(studynumber = studynum),
                    'previouscomplication':Previouscomplication.objects.filter(studynumber = studynum)})


@login_required(login_url='login')
def followPatient(request):
    if request.method == "POST":
        TempstudyNumber = request.POST.get('studynum', '')
        if ValidateVisiting(TempstudyNumber, request.POST.get('visitdate', '')) == True :
            Followvisiting = Visiting(studynumber = Studyidentity.objects.get(studynumber = TempstudyNumber),
                                visitdate =  request.POST.get('visitdate', ''),
                                bp = request.POST.get('bp', ''),
                                height = ToFloat(request.POST.get('height', '')),
                                weight = ToFloat(request.POST.get('weight', '')))
            Followvisiting.save()

            Followclinic = Clinicalpresentation(visitingid = Followvisiting,
                                studynumber = Studyidentity.objects.get(studynumber = TempstudyNumber),
                                visitdate =  request.POST.get('visitdate', ''),
                                cp_1 = CheckboxToBool(request.POST.get('cp_1', '')),
                                cp_2 = CheckboxToBool(request.POST.get('cp_2', '')),
                                cp_3 = CheckboxToBool(request.POST.get('cp_3', '')),
                                cp_4 = CheckboxToBool(request.POST.get('cp_4', '')),
                                cp_5 = CheckboxToBool(request.POST.get('cp_5', '')),
                                cp_6 = request.POST.get('cp_6', ''),
                                cp_7 = CheckboxToBool(request.POST.get('cp_7', '')),
                                cp_8 = CheckboxToBool(request.POST.get('cp_8', '')),
                                cp_9 = CheckboxToBool(request.POST.get('cp_9', '')),
                                cp_10 = CheckboxToBool(request.POST.get('cp_10', '')),
                                cp_11 = CheckboxToBool(request.POST.get('cp_11', '')),
                                cp_12 = CheckboxToBool(request.POST.get('cp_12', '')),
                                cp_13 = CheckboxToBool(request.POST.get('cp_13', '')),
                                cp_14 = CheckboxToBool(request.POST.get('cp_14', '')),
                                cp_15 = CheckboxToBool(request.POST.get('cp_15', '')),
                                cp_16 = CheckboxToBool(request.POST.get('cp_16', '')),
                                cp_17 = CheckboxToBool(request.POST.get('cp_17', '')),
                                cp_18 = CheckboxToBool(request.POST.get('cp_18', '')),
                                cp_19 = CheckboxToBool(request.POST.get('cp_19', '')),
                                cp_20 = CheckboxToBool(request.POST.get('cp_20', '')),
                                cp_21 = CheckboxToBool(request.POST.get('cp_21', '')),
                                cp_22 = CheckboxToBool(request.POST.get('cp_22', '')),
                                cp_23 = CheckboxToBool(request.POST.get('cp_23', '')),
                                cp_24 = CheckboxToBool(request.POST.get('cp_24', '')),
                                cp_25 = CheckboxToBool(request.POST.get('cp_25', '')),
                                cp_26 = CheckboxToBool(request.POST.get('cp_26', '')),
                                cp_27 = CheckboxToBool(request.POST.get('cp_27', '')),
                                cp_28 = CheckboxToBool(request.POST.get('cp_28', '')),
                                cp_29 = CheckboxToBool(request.POST.get('cp_29', '')))
            Followclinic.save()

            Totaldamage = CheckboxToInt(request.POST.get('di_1', '')) + CheckboxToInt(request.POST.get('di_2', '')) + CheckboxToInt(request.POST.get('di_3', '')) + CheckboxToInt(request.POST.get('di_4', '')) + CheckboxToInt(request.POST.get('di_6', '')) + CheckboxToInt(request.POST.get('di_7', '')) + CheckboxToInt(request.POST.get('di_8', '')) + CheckboxToInt(request.POST.get('di_9', '')) + CheckboxToInt(request.POST.get('di_10', '')) + CheckboxToInt(request.POST.get('di_11', '')) + CheckboxToInt(request.POST.get('di_13', '')) + CheckboxToInt(request.POST.get('di_14', '')) + CheckboxToInt(request.POST.get('di_15', '')) + CheckboxToInt(request.POST.get('di_16', '')) + CheckboxToInt(request.POST.get('di_17', '')) + CheckboxToInt(request.POST.get('di_19', '')) + CheckboxToInt(request.POST.get('di_20', '')) + CheckboxToInt(request.POST.get('di_21', '')) + CheckboxToInt(request.POST.get('di_22', '')) + CheckboxToInt(request.POST.get('di_23', '')) + CheckboxToInt(request.POST.get('di_24', '')) + CheckboxToInt(request.POST.get('di_26', '')) + CheckboxToInt(request.POST.get('di_27', '')) + CheckboxToInt(request.POST.get('di_28', '')) + CheckboxToInt(request.POST.get('di_29', '')) + CheckboxToInt(request.POST.get('di_30', '')) + CheckboxToInt(request.POST.get('di_31', '')) + CheckboxToInt(request.POST.get('di_32', '')) + CheckboxToInt(request.POST.get('di_34', '')) + CheckboxToInt(request.POST.get('di_35', '')) + CheckboxToInt(request.POST.get('di_36', '')) + CheckboxToInt(request.POST.get('di_37', '')) + CheckboxToInt(request.POST.get('di_38', '')) + CheckboxToInt(request.POST.get('di_39', '')) + CheckboxToInt(request.POST.get('di_40', ''))

            Followdamage = Damageindex(visitingid = Followvisiting,
                            studynumber = Studyidentity.objects.get(studynumber = TempstudyNumber),
                            visitdate =  request.POST.get('visitdate', ''),
                            di_1 = CheckboxToBool(request.POST.get('di_1', '')),
                            di_2 = CheckboxToBool(request.POST.get('di_2', '')),
                            di_3 = CheckboxToBool(request.POST.get('di_3', '')),
                            di_4 = CheckboxToBool(request.POST.get('di_4', '')),
                            di_5 = CheckboxToInt(request.POST.get('di_5', '')),
                            di_6 = CheckboxToBool(request.POST.get('di_6', '')),
                            di_7 = CheckboxToBool(request.POST.get('di_7', '')),
                            di_8 = CheckboxToBool(request.POST.get('di_8', '')),
                            di_9 = CheckboxToBool(request.POST.get('di_9', '')),
                            di_10 = CheckboxToBool(request.POST.get('di_10', '')),
                            di_11 = CheckboxToBool(request.POST.get('di_11', '')),
                            di_12 = CheckboxToInt(request.POST.get('di_12', '')),
                            di_13 = CheckboxToBool(request.POST.get('di_13', '')),
                            di_14 = CheckboxToBool(request.POST.get('di_14', '')),
                            di_15 = CheckboxToBool(request.POST.get('di_15', '')),
                            di_16 = CheckboxToBool(request.POST.get('di_16', '')),
                            di_17 = CheckboxToBool(request.POST.get('di_17', '')),
                            di_18 = CheckboxToInt(request.POST.get('di_18', '')),
                            di_19 = CheckboxToBool(request.POST.get('di_19', '')),
                            di_20 = CheckboxToBool(request.POST.get('di_20', '')),
                            di_21 = CheckboxToBool(request.POST.get('di_21', '')),
                            di_22 = CheckboxToBool(request.POST.get('di_22', '')),
                            di_23 = CheckboxToBool(request.POST.get('di_23', '')),
                            di_24 = CheckboxToBool(request.POST.get('di_24', '')),
                            di_25 = CheckboxToInt(request.POST.get('di_25', '')),
                            di_26 = CheckboxToBool(request.POST.get('di_26', '')),
                            di_27 = CheckboxToBool(request.POST.get('di_27', '')),
                            di_28 = CheckboxToBool(request.POST.get('di_28', '')),
                            di_29 = CheckboxToBool(request.POST.get('di_29', '')),
                            di_30 = CheckboxToBool(request.POST.get('di_30', '')),
                            di_31 = CheckboxToBool(request.POST.get('di_31', '')),
                            di_32 = CheckboxToBool(request.POST.get('di_32', '')),
                            di_33 = CheckboxToInt(request.POST.get('di_33', '')),
                            di_34 = CheckboxToBool(request.POST.get('di_34', '')),
                            di_35 = CheckboxToBool(request.POST.get('di_35', '')),
                            di_36 = CheckboxToBool(request.POST.get('di_36', '')),
                            di_37 = CheckboxToBool(request.POST.get('di_37', '')),
                            di_38 = CheckboxToBool(request.POST.get('di_38', '')),
                            di_39 = CheckboxToBool(request.POST.get('di_39', '')),
                            di_40 = CheckboxToBool(request.POST.get('di_40', '')),
                            di_41 = CheckboxToInt(request.POST.get('di_41', '')),
                            di_total = Totaldamage)
            Followdamage.save()

            totalSLEDAI = (CheckboxToInt(request.POST.get('seizure', '')) + CheckboxToInt(request.POST.get('psychosis', '')) + CheckboxToInt(request.POST.get('organicbrainsyndrome', '')) + CheckboxToInt(request.POST.get('visualdisturbance', '')) + CheckboxToInt(request.POST.get('cranialnerve', '')) + CheckboxToInt(request.POST.get('lupusheadache', '')) + CheckboxToInt(request.POST.get('cva', '')) + CheckboxToInt(request.POST.get('vasculitis', '')))*8 + (CheckboxToInt(request.POST.get('arthritis', '')) + CheckboxToInt(request.POST.get('myositis', '')) + CheckboxToInt(request.POST.get('casts', '')) + CheckboxToInt(request.POST.get('hematuria', '')) + CheckboxToInt(request.POST.get('proteinuria', '')) + CheckboxToInt(request.POST.get('pyuria', '')))*4 + (CheckboxToInt(request.POST.get('lowcomplement', '')) + CheckboxToInt(request.POST.get('increaseddnabinding', '')) + CheckboxToInt(request.POST.get('rash', '')) + CheckboxToInt(request.POST.get('alopecia', '')) + CheckboxToInt(request.POST.get('mucousmembrane', '')) + CheckboxToInt(request.POST.get('pleurisy', '')) + CheckboxToInt(request.POST.get('pericarditis', '')))*2 + CheckboxToInt(request.POST.get('thrombocytopenia', '')) + CheckboxToInt(request.POST.get('leukopenia', '')) + CheckboxToInt(request.POST.get('fever', '')) 

            FollowSLEDAI = Diseaseactivitysledai(visitingid = Followvisiting,
                        studynumber = Studyidentity.objects.get(studynumber = TempstudyNumber),
                        visitdate =  request.POST.get('visitdate', ''),
                        physiciansglobalassessment = CheckboxToInt(request.POST.get('physiciansglobalassessment', '')),
                        seizure = CheckboxToBool(request.POST.get('seizure', '')),
                        psychosis = CheckboxToBool(request.POST.get('psychosis', '')),
                        organicbrainsyndrome = CheckboxToBool(request.POST.get('organicbrainsyndrome', '')),
                        visualdisturbance = CheckboxToBool(request.POST.get('visualdisturbance', '')),
                        cranialnerve = CheckboxToBool(request.POST.get('cranialnerve', '')),
                        cranialnervedetail = CheckboxToInt(request.POST.get('cranialnervedetail', '')),
                        lupusheadache = CheckboxToBool(request.POST.get('lupusheadache', '')),
                        cva = CheckboxToBool(request.POST.get('cva', '')),
                        vasculitis = CheckboxToBool(request.POST.get('vasculitis', '')),
                        arthritis = CheckboxToBool(request.POST.get('arthritis', '')),
                        arthritisjointamount = CheckboxToInt(request.POST.get('arthritisjointamount', '')),
                        myositis = CheckboxToBool(request.POST.get('myositis', '')),
                        casts = CheckboxToBool(request.POST.get('casts', '')),
                        hematuria = CheckboxToBool(request.POST.get('hematuria', '')),
                        proteinuria = CheckboxToBool(request.POST.get('proteinuria', '')),
                        pyuria = CheckboxToBool(request.POST.get('pyuria', '')),
                        lowcomplement = CheckboxToBool(request.POST.get('lowcomplement', '')),
                        increaseddnabinding = CheckboxToBool(request.POST.get('increaseddnabinding', '')),
                        rash = CheckboxToBool(request.POST.get('rash', '')),
                        alopecia = CheckboxToBool(request.POST.get('alopecia', '')),
                        mucousmembrane = CheckboxToBool(request.POST.get('mucousmembrane', '')),
                        pleurisy = CheckboxToBool(request.POST.get('pleurisy', '')),
                        pericarditis = CheckboxToBool(request.POST.get('pericarditis', '')),
                        thrombocytopenia = CheckboxToBool(request.POST.get('thrombocytopenia', '')),
                        leukopenia = CheckboxToBool(request.POST.get('leukopenia', '')),
                        fever = CheckboxToBool(request.POST.get('fever', '')),
                        sledai_total = totalSLEDAI)
            FollowSLEDAI.save()


            if CheckboxToInt(request.POST.get('LN', '')) > 0:
                FollowLn = Lnlab(renalbiopsyclass = CheckboxToBool(request.POST.get('renalbiopsyclass', '')),
                renalbiopsydate = DateToNone(request.POST.get('renalbiopsydate', '')),
                activityindex = ToFloat(request.POST.get('activityindex', '')),
                chronicityindex = ToFloat(request.POST.get('chronicityindex', '')),
                ln_1 = ToFloat(request.POST.get('ln_1', '')),
                ln_2 = ToFloat(request.POST.get('ln_2', '')),
                ln_3 = request.POST.get('ln_3', ''),
                ln_4 = request.POST.get('ln_4', ''),
                ln_5 = ToFloat(request.POST.get('ln_5', '')))
                FollowLn.save()
            else : FollowLn = None

            Followlab = Laboratoryinventoryinvestigation(visitingid = Followvisiting,
                            studynumber = Studyidentity.objects.get(studynumber = TempstudyNumber),
                            lnlabid = FollowLn,
                            visitdate =  request.POST.get('visitdate', ''),
                            hb = ToFloat(request.POST.get('hb', '')),
                            wbc = ToFloat(request.POST.get('wbc', '')),
                            n = ToFloat(request.POST.get('n', '')),
                            l = ToFloat(request.POST.get('l', '')),
                            platelets = ToFloat(request.POST.get('platelets', '')),
                            esr = ToFloat(request.POST.get('esr', '')),
                            wbc_hpf = ToFloat(request.POST.get('wbc_hpf', '')),
                            rbc_hpf = ToFloat(request.POST.get('rbc_hpf', '')),
                            wbccasts = ToFloat(request.POST.get('wbccasts', '')),
                            rbccasts = ToFloat(request.POST.get('rbccasts', '')),
                            granularcasts = ToFloat(request.POST.get('granularcasts', '')),
                            glucose = ToFloat(request.POST.get('glucose', '')),
                            protein = ToFloat(request.POST.get('protein', '')),
                            tp_spoturineprotein = ToFloat(request.POST.get('tp_spoturineprotein', '')),
                            cre_spoturinecreatinine = ToFloat(request.POST.get('cre_spoturinecreatinine', '')),
                            tfhr_urineprotein = ToFloat(request.POST.get('tfhr_urineprotein', '')),
                            tfhr_urinecreatinine = ToFloat(request.POST.get('tfhr_urinecreatinine ', '')),
                            upci = ToFloat(request.POST.get('upci ', '')),
                            fbs = ToFloat(request.POST.get('fbs', '')),
                            hba1c = ToFloat(request.POST.get('hba1c', '')),
                            bun = ToFloat(request.POST.get('bun', '')),
                            cr =ToFloat(request.POST.get('cr', '')),
                            alp = ToFloat(request.POST.get('alp', '')),
                            ast = ToFloat(request.POST.get('ast', '')),
                            alt =ToFloat(request.POST.get('alt', '')),
                            ggt = ToFloat(request.POST.get('ggt', '')),
                            ldh = ToFloat(request.POST.get('ldh', '')),
                            albumin = ToFloat(request.POST.get('albumin', '')),
                            tdbilirubin = [ToFloat(request.POST.get('tdbilirubin1','')),ToFloat(request.POST.get('tdbilirubin2', ''))],
                            crp = ToFloat(request.POST.get('crp', '')),
                            choles = ToFloat(request.POST.get('choles', '')),
                            tg = ToFloat(request.POST.get('tg', '')),
                            ldl = ToFloat(request.POST.get('ldl', '')),
                            hdl = ToFloat(request.POST.get('hdl', '')),
                            inr = ToFloat(request.POST.get('inr', '')),
                            anatiter = CheckboxToBool(request.POST.get('anatiter', '')),
                            homogeneous1 = ToFloat(request.POST.get('homogeneous1', '')),
                            peripheral1 =ToFloat(request.POST.get('peripheral1', '')),
                            speckled1 = ToFloat(request.POST.get('speckled1', '')),
                            nucleolar1 = ToFloat(request.POST.get('nucleolar1', '')),
                            anti_dsdna = ToFloat(request.POST.get('anti_dsdna', '')),
                            antism = CheckboxToBool(request.POST.get('antism', '')),
                            antirnp = CheckboxToBool(request.POST.get('antirnp', '')),
                            antiro = CheckboxToBool(request.POST.get('antiro', '')),
                            antila = CheckboxToBool(request.POST.get('antila', '')),
                            aca = ToFloat(request.POST.get('aca', '')),
                            lupusanticoagulant = CheckboxToBool(request.POST.get('lupusanticoagulant', '')),
                            b2gpi = ToFloat(request.POST.get('b2gpi', '')),
                            c3 = ToFloat(request.POST.get('c3', '')),
                            c4 = ToFloat(request.POST.get('c4', '')),
                            ch50 = ToFloat(request.POST.get('ch50', '')),
                            hbsag = CheckboxToBool(request.POST.get('hbsag', '')),
                            antihbs = CheckboxToBool(request.POST.get('antihbs', '')),
                            antihbc = CheckboxToBool(request.POST.get('antihbc', '')),
                            antihcv = CheckboxToBool(request.POST.get('antihcv', '')),
                            antihiv = CheckboxToBool(request.POST.get('antihiv', '')),
                            anticic = ToFloat(request.POST.get('anticic', '')),
                            il6 = ToFloat(request.POST.get('il6', '')),
                            mpa = ToFloat(request.POST.get('mpa', '')),
                            fk507 = ToFloat(request.POST.get('fk507', '')),
                            cyclosporin = ToFloat(request.POST.get('cyclosporin', '')),
                            cytokine = CheckboxToBool(request.POST.get('cytokine', '')),
                            l1l4spinebmd_tscore = [ToFloat(request.POST.get('l1l4spinebmd_tscore1','')),ToFloat(request.POST.get('l1l4spinebmd_tscore2', ''))],
                            hipbmd_tscore = [ToFloat(request.POST.get('hipbmd_tscore1', '')),ToFloat(request.POST.get('hipbmd_tscore2', ''))],
                            radiusbmd_tscore = [ToFloat(request.POST.get('radiusbmd_tscore1', '')),ToFloat(request.POST.get('radiusbmd_tscore2', ''))],
                            stoolparasite = Labtype(status = request.POST.get('stool1', ''), date = DateToNone(request.POST.get('stool2', ''))),
                            cxr = Labtype(status = request.POST.get('CXR1', ''), date = DateToNone(request.POST.get('CXR2', ''))),
                            ekg = Labtype(status = request.POST.get('EKG1', ''), date = DateToNone(request.POST.get('EKG2', ''))),
                            echo = Labtype(status = request.POST.get('Echo1', ''), date = DateToNone(request.POST.get('Echo2', ''))))
            Followlab.save()

            FollowMed = Medication(visitingid = Followvisiting,
                            studynumber = Studyidentity.objects.get(studynumber = TempstudyNumber),
                            visitdate =  request.POST.get('visitdate',),
                            msle_1_1 = Medicationtype(generic = request.POST.get('gen1',), doseperdate = ToFloat(request.POST.get('dose1',)), startdate = DateToNone(request.POST.get('start1',)), stopdate = DateToNone(request.POST.get('end1',))),
                            msle_1_2 = Medicationtype(generic = request.POST.get('gen2',), doseperdate = ToFloat(request.POST.get('dose2',)), startdate = DateToNone(request.POST.get('start2',)), stopdate = DateToNone(request.POST.get('end2',))),
                            msle_1_3 = Medicationtype(generic = request.POST.get('gen3',), doseperdate = ToFloat(request.POST.get('dose3',)), startdate = DateToNone(request.POST.get('start3',)), stopdate = DateToNone(request.POST.get('end3',))),
                            msle_2_1 = Medicationtype(generic = request.POST.get('gen4',), doseperdate = ToFloat(request.POST.get('dose4',)), startdate = DateToNone(request.POST.get('start4',)), stopdate = DateToNone(request.POST.get('end4',))),
                            msle_2_2 = Medicationtype(generic = request.POST.get('gen5',), doseperdate = ToFloat(request.POST.get('dose5',)), startdate = DateToNone(request.POST.get('start5',)), stopdate = DateToNone(request.POST.get('end5',))),
                            msle_3_1 = Medicationtype(generic = request.POST.get('gen6',), doseperdate = ToFloat(request.POST.get('dose6',)), startdate = DateToNone(request.POST.get('start6',)), stopdate = DateToNone(request.POST.get('end6',))),
                            msle_3_2 = Medicationtype(generic = request.POST.get('gen7',), doseperdate = ToFloat(request.POST.get('dose7',)), startdate = DateToNone(request.POST.get('start7',)), stopdate = DateToNone(request.POST.get('end7',))),
                            msle_3_3 = Medicationtype(generic = request.POST.get('gen8',), doseperdate = ToFloat(request.POST.get('dose8',)), startdate = DateToNone(request.POST.get('start8',)), stopdate = DateToNone(request.POST.get('end8',))),
                            msle_3_4 = Medicationtype(generic = request.POST.get('gen9',), doseperdate = ToFloat(request.POST.get('dose9',)), startdate = DateToNone(request.POST.get('start9',)), stopdate = DateToNone(request.POST.get('end9',))),
                            msle_4_1 = Medicationtype(generic = request.POST.get('gen10',), doseperdate = ToFloat(request.POST.get('dose10',)), startdate = DateToNone(request.POST.get('start10',)), stopdate = DateToNone(request.POST.get('end10',))),
                            msle_4_2 = Medicationtype(generic = request.POST.get('gen11',), doseperdate = ToFloat(request.POST.get('dose11',)), startdate = DateToNone(request.POST.get('start11',)), stopdate = DateToNone(request.POST.get('end11',))),
                            msle_4_3 = Medicationtype(generic = request.POST.get('gen12',), doseperdate = ToFloat(request.POST.get('dose12',)), startdate = DateToNone(request.POST.get('start12',)), stopdate = DateToNone(request.POST.get('end12',))),
                            msle_4_4 = Medicationtype(generic = request.POST.get('gen13',), doseperdate = ToFloat(request.POST.get('dose13',)), startdate = DateToNone(request.POST.get('start13',)), stopdate = DateToNone(request.POST.get('end13',))),
                            msle_4_5 = Medicationtype(generic = request.POST.get('gen14',), doseperdate = ToFloat(request.POST.get('dose14',)), startdate = DateToNone(request.POST.get('start14',)), stopdate = DateToNone(request.POST.get('end14',))),
                            msle_4_6 = Medicationtype(generic = request.POST.get('gen15',), doseperdate = ToFloat(request.POST.get('dose15',)), startdate = DateToNone(request.POST.get('start15',)), stopdate = DateToNone(request.POST.get('end15',))),
                            msle_4_7 = Medicationtype(generic = request.POST.get('gen16',), doseperdate = ToFloat(request.POST.get('dose16',)), startdate = DateToNone(request.POST.get('start16',)), stopdate = DateToNone(request.POST.get('end16',))),
                            msle_4_8 = Medicationtype(generic = request.POST.get('gen17',), doseperdate = ToFloat(request.POST.get('dose17',)), startdate = DateToNone(request.POST.get('start17',)), stopdate = DateToNone(request.POST.get('end17',))),
                            msle_4_9 = Medicationtype(generic = request.POST.get('gen18',), doseperdate = ToFloat(request.POST.get('dose18',)), startdate = DateToNone(request.POST.get('start18',)), stopdate = DateToNone(request.POST.get('end18',))),
                            msle_4_10 = Medicationtype(generic = request.POST.get('gen19',), doseperdate = ToFloat(request.POST.get('dose19',)), startdate = DateToNone(request.POST.get('start19',)), stopdate = DateToNone(request.POST.get('end19',))),
                            msle_4_11 = Medicationtype(generic = request.POST.get('gen20',), doseperdate = ToFloat(request.POST.get('dose20',)), startdate = DateToNone(request.POST.get('start20',)), stopdate = DateToNone(request.POST.get('end20',))),
                            mgt_1_1 = Medicationtype(generic = request.POST.get('gen21',), doseperdate = ToFloat(request.POST.get('dose21',)), startdate = DateToNone(request.POST.get('start21',)), stopdate = DateToNone(request.POST.get('end21',))),
                            mgt_1_2 = Medicationtype(generic = request.POST.get('gen22',), doseperdate = ToFloat(request.POST.get('dose22',)), startdate = DateToNone(request.POST.get('start22',)), stopdate = DateToNone(request.POST.get('end22',))),
                            mgt_1_3 = Medicationtype(generic = request.POST.get('gen23',), doseperdate = ToFloat(request.POST.get('dose23',)), startdate = DateToNone(request.POST.get('start23',)), stopdate = DateToNone(request.POST.get('end23',))),
                            mgt_1_4 = Medicationtype(generic = request.POST.get('gen24',), doseperdate = ToFloat(request.POST.get('dose24',)), startdate = DateToNone(request.POST.get('start24',)), stopdate = DateToNone(request.POST.get('end24',))),
                            mgt_1_5 = Medicationtype(generic = request.POST.get('gen25',), doseperdate = ToFloat(request.POST.get('dose25',)), startdate = DateToNone(request.POST.get('start25',)), stopdate = DateToNone(request.POST.get('end25',))),
                            mgt_2_1 = Medicationtype(generic = request.POST.get('gen26',), doseperdate = ToFloat(request.POST.get('dose26',)), startdate = DateToNone(request.POST.get('start26',)), stopdate = DateToNone(request.POST.get('end26',))),
                            mgt_2_2 = Medicationtype(generic = request.POST.get('gen27',), doseperdate = ToFloat(request.POST.get('dose27',)), startdate = DateToNone(request.POST.get('start27',)), stopdate = DateToNone(request.POST.get('end27',))),
                            mgt_2_3 = Medicationtype(generic = request.POST.get('gen28',), doseperdate = ToFloat(request.POST.get('dose28',)), startdate = DateToNone(request.POST.get('start28',)), stopdate = DateToNone(request.POST.get('end28',))),
                            mgt_2_4 = Medicationtype(generic = request.POST.get('gen29',), doseperdate = ToFloat(request.POST.get('dose29',)), startdate = DateToNone(request.POST.get('start29',)), stopdate = DateToNone(request.POST.get('end29',))),
                            mgt_3_1 = Medicationtype(generic = request.POST.get('gen30',), doseperdate = ToFloat(request.POST.get('dose30',)), startdate = DateToNone(request.POST.get('start30',)), stopdate = DateToNone(request.POST.get('end30',))),
                            mgt_3_2 = Medicationtype(generic = request.POST.get('gen31',), doseperdate = ToFloat(request.POST.get('dose31',)), startdate = DateToNone(request.POST.get('start31',)), stopdate = DateToNone(request.POST.get('end31',))),
                            mgt_3_3 = Medicationtype(generic = request.POST.get('gen32',), doseperdate = ToFloat(request.POST.get('dose32',)), startdate = DateToNone(request.POST.get('start32',)), stopdate = DateToNone(request.POST.get('end32',))),
                            mgt_4_1 = Medicationtype(generic = request.POST.get('gen33',), doseperdate = ToFloat(request.POST.get('dose33',)), startdate = DateToNone(request.POST.get('start33',)), stopdate = DateToNone(request.POST.get('end33',))),
                            mgt_4_2 = Medicationtype(generic = request.POST.get('gen34',), doseperdate = ToFloat(request.POST.get('dose34',)), startdate = DateToNone(request.POST.get('start34',)), stopdate = DateToNone(request.POST.get('end34',))),
                            mgt_4_3 = Medicationtype(generic = request.POST.get('gen35',), doseperdate = ToFloat(request.POST.get('dose35',)), startdate = DateToNone(request.POST.get('start35',)), stopdate = DateToNone(request.POST.get('end35',))),
                            mgt_4_4 = Medicationtype(generic = request.POST.get('gen36',), doseperdate = ToFloat(request.POST.get('dose36',)), startdate = DateToNone(request.POST.get('start36',)), stopdate = DateToNone(request.POST.get('end36',))),
                            mgt_other = CheckboxToBool(request.POST.get('mgt_other',)))
            FollowMed.save()
        
            #test_med_list = Medication.objects.all()
            #All data feilds
            lab = Laboratoryinventoryinvestigation.objects.get(visitingid = Followvisiting.visitingid)
            if haslnlab(lab) is True:
                lnlab = Lnlab.objects.get(lnlabid = lab.lnlabid) 
            else: 
                lnlab = None

            return render(request, 'followup-detail.html',
                          {'visiting':Visiting.objects.get(visitingid = Followvisiting.visitingid),
                          'med':Medication.objects.get(visitingid = Followvisiting.visitingid),
                          'lab':Laboratoryinventoryinvestigation.objects.get(visitingid = Followvisiting.visitingid),
                          'lnlab':lnlab,
                          'sledai':Diseaseactivitysledai.objects.get(visitingid = Followvisiting.visitingid),
                          'damageindex':Damageindex.objects.get(visitingid = Followvisiting.visitingid),
                          'clinicalpresentation':Clinicalpresentation.objects.get(visitingid = Followvisiting.visitingid)})
        else:
            return render(request, 'login.html')


@login_required(login_url='login')
def followDetail(request, visitid):
    lab = Laboratoryinventoryinvestigation.objects.get(visitingid = visitid)
    if haslnlab(lab) is True:
        lnlab = Lnlab.objects.get(lnlabid = lab.lnlabid) 
    else: 
        lnlab = None
    return render(request, 'followup-detail.html',
                      {'visiting':Visiting.objects.get(visitingid = visitid),
                      'med':Medication.objects.get(visitingid = visitid),
                      'lab':Laboratoryinventoryinvestigation.objects.get(visitingid = visitid),
                      'lnlab':lnlab,
                      'sledai':Diseaseactivitysledai.objects.get(visitingid = visitid),
                      'damageindex':Damageindex.objects.get(visitingid = visitid),
                      'clinicalpresentation':Clinicalpresentation.objects.get(visitingid = visitid)})


@login_required(login_url='login')
def followEditPost(request):
    if request.method == "POST":
        temp_visitid = request.POST.get('visitid',)
        old_visiting = Visiting.objects.get(visitingid = temp_visitid)
        old_visiting.visitdate =  request.POST.get('visitdate',)
        old_visiting.bp = request.POST.get('bp',)
        old_visiting.height = ToFloat(request.POST.get('height',))
        old_visiting.weight = ToFloat(request.POST.get('weight',))
        old_visiting.save()

        old_clinic = Clinicalpresentation.objects.get(visitingid = temp_visitid)
        old_clinic.visitdate =  request.POST.get('visitdate', '')
        old_clinic.cp_1 = CheckboxToBool(request.POST.get('cp_1', ''))
        old_clinic.cp_2 = CheckboxToBool(request.POST.get('cp_2', ''))
        old_clinic.cp_3 = CheckboxToBool(request.POST.get('cp_3', ''))
        old_clinic.cp_4 = CheckboxToBool(request.POST.get('cp_4', ''))
        old_clinic.cp_5 = CheckboxToBool(request.POST.get('cp_5', ''))
        old_clinic.cp_6 = request.POST.get('cp_6', '')
        old_clinic.cp_7 = CheckboxToBool(request.POST.get('cp_7', ''))
        old_clinic.cp_8 = CheckboxToBool(request.POST.get('cp_8', ''))
        old_clinic.cp_9 = CheckboxToBool(request.POST.get('cp_9', ''))
        old_clinic.cp_10 = CheckboxToBool(request.POST.get('cp_10', ''))
        old_clinic.cp_11 = CheckboxToBool(request.POST.get('cp_11', ''))
        old_clinic.cp_12 = CheckboxToBool(request.POST.get('cp_12', ''))
        old_clinic.cp_13 = CheckboxToBool(request.POST.get('cp_13', ''))
        old_clinic.cp_14 = CheckboxToBool(request.POST.get('cp_14', ''))
        old_clinic.cp_15 = CheckboxToBool(request.POST.get('cp_15', ''))
        old_clinic.cp_16 = CheckboxToBool(request.POST.get('cp_16', ''))
        old_clinic.cp_17 = CheckboxToBool(request.POST.get('cp_17', ''))
        old_clinic.cp_18 = CheckboxToBool(request.POST.get('cp_18', ''))
        old_clinic.cp_19 = CheckboxToBool(request.POST.get('cp_19', ''))
        old_clinic.cp_20 = CheckboxToBool(request.POST.get('cp_20', ''))
        old_clinic.cp_21 = CheckboxToBool(request.POST.get('cp_21', ''))
        old_clinic.cp_22 = CheckboxToBool(request.POST.get('cp_22', ''))
        old_clinic.cp_23 = CheckboxToBool(request.POST.get('cp_23', ''))
        old_clinic.cp_24 = CheckboxToBool(request.POST.get('cp_24', ''))
        old_clinic.cp_25 = CheckboxToBool(request.POST.get('cp_25', ''))
        old_clinic.cp_26 = CheckboxToBool(request.POST.get('cp_26', ''))
        old_clinic.cp_27 = CheckboxToBool(request.POST.get('cp_27', ''))
        old_clinic.cp_28 = CheckboxToBool(request.POST.get('cp_28', ''))
        old_clinic.cp_29 = CheckboxToBool(request.POST.get('cp_29', ''))
        old_clinic.save()

        Totaldamage = CheckboxToInt(request.POST.get('di_1', '')) + CheckboxToInt(request.POST.get('di_2', '')) + CheckboxToInt(request.POST.get('di_3', '')) + CheckboxToInt(request.POST.get('di_4', '')) + CheckboxToInt(request.POST.get('di_6', '')) + CheckboxToInt(request.POST.get('di_7', '')) + CheckboxToInt(request.POST.get('di_8', '')) + CheckboxToInt(request.POST.get('di_9', '')) + CheckboxToInt(request.POST.get('di_10', '')) + CheckboxToInt(request.POST.get('di_11', '')) + CheckboxToInt(request.POST.get('di_13', '')) + CheckboxToInt(request.POST.get('di_14', '')) + CheckboxToInt(request.POST.get('di_15', '')) + CheckboxToInt(request.POST.get('di_16', '')) + CheckboxToInt(request.POST.get('di_17', '')) + CheckboxToInt(request.POST.get('di_19', '')) + CheckboxToInt(request.POST.get('di_20', '')) + CheckboxToInt(request.POST.get('di_21', '')) + CheckboxToInt(request.POST.get('di_22', '')) + CheckboxToInt(request.POST.get('di_23', '')) + CheckboxToInt(request.POST.get('di_24', '')) + CheckboxToInt(request.POST.get('di_26', '')) + CheckboxToInt(request.POST.get('di_27', '')) + CheckboxToInt(request.POST.get('di_28', '')) + CheckboxToInt(request.POST.get('di_29', '')) + CheckboxToInt(request.POST.get('di_30', '')) + CheckboxToInt(request.POST.get('di_31', '')) + CheckboxToInt(request.POST.get('di_32', '')) + CheckboxToInt(request.POST.get('di_34', '')) + CheckboxToInt(request.POST.get('di_35', '')) + CheckboxToInt(request.POST.get('di_36', '')) + CheckboxToInt(request.POST.get('di_37', '')) + CheckboxToInt(request.POST.get('di_38', '')) + CheckboxToInt(request.POST.get('di_39', '')) + CheckboxToInt(request.POST.get('di_40', ''))

        old_damage = Damageindex.objects.get(visitingid = temp_visitid)
        old_damage.visitdate =  request.POST.get('visitdate', '')
        old_damage.di_1 = CheckboxToBool(request.POST.get('di_1', ''))
        old_damage.di_2 = CheckboxToBool(request.POST.get('di_2', ''))
        old_damage.di_3 = CheckboxToBool(request.POST.get('di_3', ''))
        old_damage.di_4 = CheckboxToBool(request.POST.get('di_4', ''))
        old_damage.di_5 = CheckboxToInt(request.POST.get('di_5', ''))
        old_damage.di_6 = CheckboxToBool(request.POST.get('di_6', ''))
        old_damage.di_7 = CheckboxToBool(request.POST.get('di_7', ''))
        old_damage.di_8 = CheckboxToBool(request.POST.get('di_8', ''))
        old_damage.di_9 = CheckboxToBool(request.POST.get('di_9', ''))
        old_damage.di_10 = CheckboxToBool(request.POST.get('di_10', ''))
        old_damage.di_11 = CheckboxToBool(request.POST.get('di_11', ''))
        old_damage.di_12 = CheckboxToInt(request.POST.get('di_12', ''))
        old_damage.di_13 = CheckboxToBool(request.POST.get('di_13', ''))
        old_damage.di_14 = CheckboxToBool(request.POST.get('di_14', ''))
        old_damage.di_15 = CheckboxToBool(request.POST.get('di_15', ''))
        old_damage.di_16 = CheckboxToBool(request.POST.get('di_16', ''))
        old_damage.di_17 = CheckboxToBool(request.POST.get('di_17', ''))
        old_damage.di_18 = CheckboxToInt(request.POST.get('di_18', ''))
        old_damage.di_19 = CheckboxToBool(request.POST.get('di_19', ''))
        old_damage.di_20 = CheckboxToBool(request.POST.get('di_20', ''))
        old_damage.di_21 = CheckboxToBool(request.POST.get('di_21', ''))
        old_damage.di_22 = CheckboxToBool(request.POST.get('di_22', ''))
        old_damage.di_23 = CheckboxToBool(request.POST.get('di_23', ''))
        old_damage.di_24 = CheckboxToBool(request.POST.get('di_24', ''))
        old_damage.di_25 = CheckboxToInt(request.POST.get('di_25', ''))
        old_damage.di_26 = CheckboxToBool(request.POST.get('di_26', ''))
        old_damage.di_27 = CheckboxToBool(request.POST.get('di_27', ''))
        old_damage.di_28 = CheckboxToBool(request.POST.get('di_28', ''))
        old_damage.di_29 = CheckboxToBool(request.POST.get('di_29', ''))
        old_damage.di_30 = CheckboxToBool(request.POST.get('di_30', ''))
        old_damage.di_31 = CheckboxToBool(request.POST.get('di_31', ''))
        old_damage.di_32 = CheckboxToBool(request.POST.get('di_32', ''))
        old_damage.di_33 = CheckboxToInt(request.POST.get('di_33', ''))
        old_damage.di_34 = CheckboxToBool(request.POST.get('di_34', ''))
        old_damage.di_35 = CheckboxToBool(request.POST.get('di_35', ''))
        old_damage.di_36 = CheckboxToBool(request.POST.get('di_36', ''))
        old_damage.di_37 = CheckboxToBool(request.POST.get('di_37', ''))
        old_damage.di_38 = CheckboxToBool(request.POST.get('di_38', ''))
        old_damage.di_39 = CheckboxToBool(request.POST.get('di_39', ''))
        old_damage.di_40 = CheckboxToBool(request.POST.get('di_40', ''))
        old_damage.di_41 = CheckboxToInt(request.POST.get('di_41', ''))
        old_damage.di_total = Totaldamage
        old_damage.save()

        totalSLEDAI = (CheckboxToInt(request.POST.get('seizure', '')) + CheckboxToInt(request.POST.get('psychosis', '')) + CheckboxToInt(request.POST.get('organicbrainsyndrome', '')) + CheckboxToInt(request.POST.get('visualdisturbance', '')) + CheckboxToInt(request.POST.get('cranialnerve', '')) + CheckboxToInt(request.POST.get('lupusheadache', '')) + CheckboxToInt(request.POST.get('cva', '')) + CheckboxToInt(request.POST.get('vasculitis', '')))*8 + (CheckboxToInt(request.POST.get('arthritis', '')) + CheckboxToInt(request.POST.get('myositis', '')) + CheckboxToInt(request.POST.get('casts', '')) + CheckboxToInt(request.POST.get('hematuria', '')) + CheckboxToInt(request.POST.get('proteinuria', '')) + CheckboxToInt(request.POST.get('pyuria', '')))*4 + (CheckboxToInt(request.POST.get('lowcomplement', '')) + CheckboxToInt(request.POST.get('increaseddnabinding', '')) + CheckboxToInt(request.POST.get('rash', '')) + CheckboxToInt(request.POST.get('alopecia', '')) + CheckboxToInt(request.POST.get('mucousmembrane', '')) + CheckboxToInt(request.POST.get('pleurisy', '')) + CheckboxToInt(request.POST.get('pericarditis', '')))*2 + CheckboxToInt(request.POST.get('thrombocytopenia', '')) + CheckboxToInt(request.POST.get('leukopenia', '')) + CheckboxToInt(request.POST.get('fever', '')) 

        old_sledai = Diseaseactivitysledai.objects.get(visitingid = temp_visitid)
        old_sledai.visitdate =  request.POST.get('visitdate', '')
        old_sledai.physiciansglobalassessment = CheckboxToInt(request.POST.get('physiciansglobalassessment', ''))
        old_sledai.seizure = CheckboxToBool(request.POST.get('seizure', ''))
        old_sledai.psychosis = CheckboxToBool(request.POST.get('psychosis', ''))
        old_sledai.organicbrainsyndrome = CheckboxToBool(request.POST.get('organicbrainsyndrome', ''))
        old_sledai.visualdisturbance = CheckboxToBool(request.POST.get('visualdisturbance', ''))
        old_sledai.cranialnerve = CheckboxToBool(request.POST.get('cranialnerve', ''))
        old_sledai.cranialnervedetail = CheckboxToInt(request.POST.get('cranialnervedetail', ''))
        old_sledai.lupusheadache = CheckboxToBool(request.POST.get('lupusheadache', ''))
        old_sledai.cva = CheckboxToBool(request.POST.get('cva', ''))
        old_sledai.vasculitis = CheckboxToBool(request.POST.get('vasculitis', ''))
        old_sledai.arthritis = CheckboxToBool(request.POST.get('arthritis', ''))
        old_sledai.arthritisjointamount = CheckboxToInt(request.POST.get('arthritisjointamount', ''))
        old_sledai.myositis = CheckboxToBool(request.POST.get('myositis', ''))
        old_sledai.casts = CheckboxToBool(request.POST.get('casts', ''))
        old_sledai.hematuria = CheckboxToBool(request.POST.get('hematuria', ''))
        old_sledai.proteinuria = CheckboxToBool(request.POST.get('proteinuria', ''))
        old_sledai.pyuria = CheckboxToBool(request.POST.get('pyuria', ''))
        old_sledai.lowcomplement = CheckboxToBool(request.POST.get('lowcomplement', ''))
        old_sledai.increaseddnabinding = CheckboxToBool(request.POST.get('increaseddnabinding', ''))
        old_sledai.rash = CheckboxToBool(request.POST.get('rash', ''))
        old_sledai.alopecia = CheckboxToBool(request.POST.get('alopecia', ''))
        old_sledai.mucousmembrane = CheckboxToBool(request.POST.get('mucousmembrane', ''))
        old_sledai.pleurisy = CheckboxToBool(request.POST.get('pleurisy', ''))
        old_sledai.pericarditis = CheckboxToBool(request.POST.get('pericarditis', ''))
        old_sledai.thrombocytopenia = CheckboxToBool(request.POST.get('thrombocytopenia', ''))
        old_sledai.leukopenia = CheckboxToBool(request.POST.get('leukopenia', ''))
        old_sledai.fever = CheckboxToBool(request.POST.get('fever', ''))
        old_sledai.sledai_total = totalSLEDAI
        old_sledai.save()

        old_ln = None
        if CheckboxToInt(request.POST.get('LN', '')) > 0:
            if Laboratoryinventoryinvestigation.objects.get(visitingid = temp_visitid).lnlabid is not None:
                old_ln = Lnlab.objects.get(lnlabid = Laboratoryinventoryinvestigation.objects.get(visitingid = temp_visitid).lnlabid)
                old_ln.renalbiopsyclass = CheckboxToBool(request.POST.get('renalbiopsyclass', ''))
                old_ln.renalbiopsydate = DateToNone(request.POST.get('renalbiopsydate', ''))
                old_ln.activityindex = ToFloat(request.POST.get('activityindex', ''))
                old_ln.chronicityindex = ToFloat(request.POST.get('chronicityindex', ''))
                old_ln.ln_1 = ToFloat(request.POST.get('ln_1', ''))
                old_ln.ln_2 = ToFloat(request.POST.get('ln_2', ''))
                old_ln.ln_3 = request.POST.get('ln_3', '')
                old_ln.ln_4 = request.POST.get('ln_4', '')
                old_ln.ln_5 = ToFloat(request.POST.get('ln_5', ''))
                old_ln.save()
            else : 
                old_ln = Lnlab(renalbiopsyclass = CheckboxToBool(request.POST.get('renalbiopsyclass', '')),
                renalbiopsydate = DateToNone(request.POST.get('renalbiopsydate', '')),
                activityindex = ToFloat(request.POST.get('activityindex', '')),
                chronicityindex = ToFloat(request.POST.get('chronicityindex', '')),
                ln_1 = ToFloat(request.POST.get('ln_1', '')),
                ln_2 = ToFloat(request.POST.get('ln_2', '')),
                ln_3 = request.POST.get('ln_3', ''),
                ln_4 = request.POST.get('ln_4', ''),
                ln_5 = ToFloat(request.POST.get('ln_5', '')))
                old_ln.save()

        old_lab = Laboratoryinventoryinvestigation.objects.get(visitingid = temp_visitid)
        old_lab.lnlabid = old_ln
        old_lab.visitdate =  request.POST.get('visitdate', '')
        old_lab.hb = ToFloat(request.POST.get('hb', ''))
        old_lab.wbc = ToFloat(request.POST.get('wbc', ''))
        old_lab.n = ToFloat(request.POST.get('n', ''))
        old_lab.l = ToFloat(request.POST.get('l', ''))
        old_lab.platelets = ToFloat(request.POST.get('platelets', ''))
        old_lab.esr = ToFloat(request.POST.get('esr', ''))
        old_lab.wbc_hpf = ToFloat(request.POST.get('wbc_hpf', ''))
        old_lab.rbc_hpf = ToFloat(request.POST.get('rbc_hpf', ''))
        old_lab.wbccasts = ToFloat(request.POST.get('wbccasts', ''))
        old_lab.rbccasts = ToFloat(request.POST.get('rbccasts', ''))
        old_lab.granularcasts = ToFloat(request.POST.get('granularcasts', ''))
        old_lab.glucose = ToFloat(request.POST.get('glucose', ''))
        old_lab.protein = ToFloat(request.POST.get('protein', ''))
        old_lab.tp_spoturineprotein = ToFloat(request.POST.get('tp_spoturineprotein', ''))
        old_lab.cre_spoturinecreatinine = ToFloat(request.POST.get('cre_spoturinecreatinine', ''))
        old_lab.tfhr_urineprotein = ToFloat(request.POST.get('tfhr_urineprotein', ''))
        old_lab.tfhr_urinecreatinine = ToFloat(request.POST.get('tfhr_urinecreatinine ', ''))
        old_lab.upci = ToFloat(request.POST.get('upci ', ''))
        old_lab.fbs = ToFloat(request.POST.get('fbs', ''))
        old_lab.hba1c = ToFloat(request.POST.get('hba1c', ''))
        old_lab.bun = ToFloat(request.POST.get('bun', ''))
        old_lab.cr =ToFloat(request.POST.get('cr', ''))
        old_lab.alp = ToFloat(request.POST.get('alp', ''))
        old_lab.ast = ToFloat(request.POST.get('ast', ''))
        old_lab.alt =ToFloat(request.POST.get('alt', ''))
        old_lab.ggt = ToFloat(request.POST.get('ggt', ''))
        old_lab.ldh = ToFloat(request.POST.get('ldh', ''))
        old_lab.albumin = ToFloat(request.POST.get('albumin', ''))
        old_lab.tdbilirubin = [ToFloat(request.POST.get('tdbilirubin1','')),ToFloat(request.POST.get('tdbilirubin2', ''))]
        old_lab.crp = ToFloat(request.POST.get('crp', ''))
        old_lab.choles = ToFloat(request.POST.get('choles', ''))
        old_lab.tg = ToFloat(request.POST.get('tg', ''))
        old_lab.ldl = ToFloat(request.POST.get('ldl', ''))
        old_lab.hdl = ToFloat(request.POST.get('hdl', ''))
        old_lab.inr = ToFloat(request.POST.get('inr', ''))
        old_lab.anatiter = CheckboxToBool(request.POST.get('anatiter', ''))
        old_lab.homogeneous1 = ToFloat(request.POST.get('homogeneous1', ''))
        old_lab.peripheral1 =ToFloat(request.POST.get('peripheral1', ''))
        old_lab.speckled1 = ToFloat(request.POST.get('speckled1', ''))
        old_lab.nucleolar1 = ToFloat(request.POST.get('nucleolar1', ''))
        old_lab.anti_dsdna = ToFloat(request.POST.get('anti_dsdna', ''))
        old_lab.antism = CheckboxToBool(request.POST.get('antism', ''))
        old_lab.antirnp = CheckboxToBool(request.POST.get('antirnp', ''))
        old_lab.antiro = CheckboxToBool(request.POST.get('antiro', ''))
        old_lab.antila = CheckboxToBool(request.POST.get('antila', ''))
        old_lab.aca = ToFloat(request.POST.get('aca', ''))
        old_lab.lupusanticoagulant = CheckboxToBool(request.POST.get('lupusanticoagulant', ''))
        old_lab.b2gpi = ToFloat(request.POST.get('b2gpi', ''))
        old_lab.c3 = ToFloat(request.POST.get('c3', ''))
        old_lab.c4 = ToFloat(request.POST.get('c4', ''))
        old_lab.ch50 = ToFloat(request.POST.get('ch50', ''))
        old_lab.hbsag = CheckboxToBool(request.POST.get('hbsag', ''))
        old_lab.antihbs = CheckboxToBool(request.POST.get('antihbs', ''))
        old_lab.antihbc = CheckboxToBool(request.POST.get('antihbc', ''))
        old_lab.antihcv = CheckboxToBool(request.POST.get('antihcv', ''))
        old_lab.antihiv = CheckboxToBool(request.POST.get('antihiv', ''))
        old_lab.anticic = ToFloat(request.POST.get('anticic', ''))
        old_lab.il6 = ToFloat(request.POST.get('il6', ''))
        old_lab.mpa = ToFloat(request.POST.get('mpa', ''))
        old_lab.fk507 = ToFloat(request.POST.get('fk507', ''))
        old_lab.cyclosporin = ToFloat(request.POST.get('cyclosporin', ''))
        old_lab.cytokine = CheckboxToBool(request.POST.get('cytokine', ''))
        old_lab.l1l4spinebmd_tscore = [ToFloat(request.POST.get('l1l4spinebmd_tscore1',)),ToFloat(request.POST.get('l1l4spinebmd_tscore2',))]
        old_lab.hipbmd_tscore = [ToFloat(request.POST.get('hipbmd_tscore1',)),ToFloat(request.POST.get('hipbmd_tscore2',))]
        old_lab.radiusbmd_tscore = [ToFloat(request.POST.get('radiusbmd_tscore1',)),ToFloat(request.POST.get('radiusbmd_tscore2',))]
        old_lab.stoolparasite = Labtype(status = request.POST.get('stool1',), date = DateToNone(request.POST.get('stool2',)))
        old_lab.cxr = Labtype(status = request.POST.get('CXR1',), date = DateToNone(request.POST.get('CXR2',)))
        old_lab.ekg = Labtype(status = request.POST.get('EKG1',), date = DateToNone(request.POST.get('EKG2',)))
        old_lab.echo = Labtype(status = request.POST.get('Echo1',), date = DateToNone(request.POST.get('Echo2',)))
        old_lab.save()
        
        old_med = Medication.objects.get(visitingid = temp_visitid)
        old_med.visitdate =  request.POST.get('visitdate',)
        old_med.msle_1_1 = Medicationtype(generic = request.POST.get('gen1',), doseperdate = ToFloat(request.POST.get('dose1',)), startdate = DateToNone(request.POST.get('start1',)), stopdate = DateToNone(request.POST.get('end1',)))
        old_med.msle_1_2 = Medicationtype(generic = request.POST.get('gen2',), doseperdate = ToFloat(request.POST.get('dose2',)), startdate = DateToNone(request.POST.get('start2',)), stopdate = DateToNone(request.POST.get('end2',)))
        old_med.msle_1_3 = Medicationtype(generic = request.POST.get('gen3',), doseperdate = ToFloat(request.POST.get('dose3',)), startdate = DateToNone(request.POST.get('start3',)), stopdate = DateToNone(request.POST.get('end3',)))
        old_med.msle_2_1 = Medicationtype(generic = request.POST.get('gen4',), doseperdate = ToFloat(request.POST.get('dose4',)), startdate = DateToNone(request.POST.get('start4',)), stopdate = DateToNone(request.POST.get('end4',)))
        old_med.msle_2_2 = Medicationtype(generic = request.POST.get('gen5',), doseperdate = ToFloat(request.POST.get('dose5',)), startdate = DateToNone(request.POST.get('start5',)), stopdate = DateToNone(request.POST.get('end5',)))
        old_med.msle_3_1 = Medicationtype(generic = request.POST.get('gen6',), doseperdate = ToFloat(request.POST.get('dose6',)), startdate = DateToNone(request.POST.get('start6',)), stopdate = DateToNone(request.POST.get('end6',)))
        old_med.msle_3_2 = Medicationtype(generic = request.POST.get('gen7',), doseperdate = ToFloat(request.POST.get('dose7',)), startdate = DateToNone(request.POST.get('start7',)), stopdate = DateToNone(request.POST.get('end7',)))
        old_med.msle_3_3 = Medicationtype(generic = request.POST.get('gen8',), doseperdate = ToFloat(request.POST.get('dose8',)), startdate = DateToNone(request.POST.get('start8',)), stopdate = DateToNone(request.POST.get('end8',))),
        old_med.msle_3_4 = Medicationtype(generic = request.POST.get('gen9',), doseperdate = ToFloat(request.POST.get('dose9',)), startdate = DateToNone(request.POST.get('start9',)), stopdate = DateToNone(request.POST.get('end9',)))
        old_med.msle_4_1 = Medicationtype(generic = request.POST.get('gen10',), doseperdate = ToFloat(request.POST.get('dose10',)), startdate = DateToNone(request.POST.get('start10',)), stopdate = DateToNone(request.POST.get('end10',)))
        old_med.msle_4_2 = Medicationtype(generic = request.POST.get('gen11',), doseperdate = ToFloat(request.POST.get('dose11',)), startdate = DateToNone(request.POST.get('start11',)), stopdate = DateToNone(request.POST.get('end11',)))
        old_med.msle_4_3 = Medicationtype(generic = request.POST.get('gen12',), doseperdate = ToFloat(request.POST.get('dose12',)), startdate = DateToNone(request.POST.get('start12',)), stopdate = DateToNone(request.POST.get('end12',)))
        old_med.msle_4_4 = Medicationtype(generic = request.POST.get('gen13',), doseperdate = ToFloat(request.POST.get('dose13',)), startdate = DateToNone(request.POST.get('start13',)), stopdate = DateToNone(request.POST.get('end13',)))
        old_med.msle_4_5 = Medicationtype(generic = request.POST.get('gen14',), doseperdate = ToFloat(request.POST.get('dose14',)), startdate = DateToNone(request.POST.get('start14',)), stopdate = DateToNone(request.POST.get('end14',)))
        old_med.msle_4_6 = Medicationtype(generic = request.POST.get('gen15',), doseperdate = ToFloat(request.POST.get('dose15',)), startdate = DateToNone(request.POST.get('start15',)), stopdate = DateToNone(request.POST.get('end15',)))
        old_med.msle_4_7 = Medicationtype(generic = request.POST.get('gen16',), doseperdate = ToFloat(request.POST.get('dose16',)), startdate = DateToNone(request.POST.get('start16',)), stopdate = DateToNone(request.POST.get('end16',)))
        old_med.msle_4_8 = Medicationtype(generic = request.POST.get('gen17',), doseperdate = ToFloat(request.POST.get('dose17',)), startdate = DateToNone(request.POST.get('start17',)), stopdate = DateToNone(request.POST.get('end17',)))
        old_med.msle_4_9 = Medicationtype(generic = request.POST.get('gen18',), doseperdate = ToFloat(request.POST.get('dose18',)), startdate = DateToNone(request.POST.get('start18',)), stopdate = DateToNone(request.POST.get('end18',)))
        old_med.msle_4_10 = Medicationtype(generic = request.POST.get('gen19',), doseperdate = ToFloat(request.POST.get('dose19',)), startdate = DateToNone(request.POST.get('start19',)), stopdate = DateToNone(request.POST.get('end19',)))
        old_med.msle_4_11 = Medicationtype(generic = request.POST.get('gen20',), doseperdate = ToFloat(request.POST.get('dose20',)), startdate = DateToNone(request.POST.get('start20',)), stopdate = DateToNone(request.POST.get('end20',)))
        old_med.mgt_1_1 = Medicationtype(generic = request.POST.get('gen21',), doseperdate = ToFloat(request.POST.get('dose21',)), startdate = DateToNone(request.POST.get('start21',)), stopdate = DateToNone(request.POST.get('end21',)))
        old_med.mgt_1_2 = Medicationtype(generic = request.POST.get('gen22',), doseperdate = ToFloat(request.POST.get('dose22',)), startdate = DateToNone(request.POST.get('start22',)), stopdate = DateToNone(request.POST.get('end22',)))
        old_med.mgt_1_3 = Medicationtype(generic = request.POST.get('gen23',), doseperdate = ToFloat(request.POST.get('dose23',)), startdate = DateToNone(request.POST.get('start23',)), stopdate = DateToNone(request.POST.get('end23',)))
        old_med.mgt_1_4 = Medicationtype(generic = request.POST.get('gen24',), doseperdate = ToFloat(request.POST.get('dose24',)), startdate = DateToNone(request.POST.get('start24',)), stopdate = DateToNone(request.POST.get('end24',)))
        old_med.mgt_1_5 = Medicationtype(generic = request.POST.get('gen25',), doseperdate = ToFloat(request.POST.get('dose25',)), startdate = DateToNone(request.POST.get('start25',)), stopdate = DateToNone(request.POST.get('end25',)))
        old_med.mgt_2_1 = Medicationtype(generic = request.POST.get('gen26',), doseperdate = ToFloat(request.POST.get('dose26',)), startdate = DateToNone(request.POST.get('start26',)), stopdate = DateToNone(request.POST.get('end26',)))
        old_med.mgt_2_2 = Medicationtype(generic = request.POST.get('gen27',), doseperdate = ToFloat(request.POST.get('dose27',)), startdate = DateToNone(request.POST.get('start27',)), stopdate = DateToNone(request.POST.get('end27',)))
        old_med.mgt_2_3 = Medicationtype(generic = request.POST.get('gen28',), doseperdate = ToFloat(request.POST.get('dose28',)), startdate = DateToNone(request.POST.get('start28',)), stopdate = DateToNone(request.POST.get('end28',)))
        old_med.mgt_2_4 = Medicationtype(generic = request.POST.get('gen29',), doseperdate = ToFloat(request.POST.get('dose29',)), startdate = DateToNone(request.POST.get('start29',)), stopdate = DateToNone(request.POST.get('end29',)))
        old_med.mgt_3_1 = Medicationtype(generic = request.POST.get('gen30',), doseperdate = ToFloat(request.POST.get('dose30',)), startdate = DateToNone(request.POST.get('start30',)), stopdate = DateToNone(request.POST.get('end30',)))
        old_med.mgt_3_2 = Medicationtype(generic = request.POST.get('gen31',), doseperdate = ToFloat(request.POST.get('dose31',)), startdate = DateToNone(request.POST.get('start31',)), stopdate = DateToNone(request.POST.get('end31',)))
        old_med.mgt_3_3 = Medicationtype(generic = request.POST.get('gen32',), doseperdate = ToFloat(request.POST.get('dose32',)), startdate = DateToNone(request.POST.get('start32',)), stopdate = DateToNone(request.POST.get('end32',)))
        old_med.mgt_4_1 = Medicationtype(generic = request.POST.get('gen33',), doseperdate = ToFloat(request.POST.get('dose33',)), startdate = DateToNone(request.POST.get('start33',)), stopdate = DateToNone(request.POST.get('end33',)))
        old_med.mgt_4_2 = Medicationtype(generic = request.POST.get('gen34',), doseperdate = ToFloat(request.POST.get('dose34',)), startdate = DateToNone(request.POST.get('start34',)), stopdate = DateToNone(request.POST.get('end34',)))
        old_med.mgt_4_3 = Medicationtype(generic = request.POST.get('gen35',), doseperdate = ToFloat(request.POST.get('dose35',)), startdate = DateToNone(request.POST.get('start35',)), stopdate = DateToNone(request.POST.get('end35',)))
        old_med.mgt_4_4 = Medicationtype(generic = request.POST.get('gen36',), doseperdate = ToFloat(request.POST.get('dose36',)), startdate = DateToNone(request.POST.get('start36',)), stopdate = DateToNone(request.POST.get('end36',)))
        old_med.mgt_other = CheckboxToBool(request.POST.get('mgt_other',))
        old_med.save()
        
        return render(request, 'followup-detail.html',
                          {'visiting':old_visiting,
                          'med':old_med,
                          'lab':old_lab,
                          'lnlab':old_ln,
                          'sledai':old_sledai,
                          'damageindex':old_damage,
                          'clinicalpresentation':old_clinic})
    

@login_required(login_url='login')
def followEdit(request, visitid):
    lab = Laboratoryinventoryinvestigation.objects.get(visitingid = visitid)
    if haslnlab(lab) is True:
        lnlab = Lnlab.objects.get(lnlabid = lab.lnlabid) 
    else: 
        lnlab = None
    return render(request, 'followup-edit.html',
                      {'visiting':Visiting.objects.get(visitingid = visitid),
                      'med':Medication.objects.get(visitingid = visitid),
                      'lab':lab,
                      'lnlab':lnlab,
                      'sledai':Diseaseactivitysledai.objects.get(visitingid = visitid),
                      'damageindex':Damageindex.objects.get(visitingid = visitid),
                      'clinicalpresentation':Clinicalpresentation.objects.get(visitingid = visitid)})




@login_required(login_url='login')
def enrollEdit(request, studynum):
    return render(request, 'enrollment-edit.html',
                  {'patient':Studyidentity.objects.get(studynumber = studynum),
                   'acrcriteria':Acrcriteria.objects.get(studynumber = studynum),
                   'slicccriteria':Slicccriteria.objects.get(studynumber = studynum),
                    'familyhistory':Familyhistory.objects.get(studynumber = studynum),
                    'medicalcondition':Medicalcondition.objects.get(studynumber = studynum),
                    'previousorganinvolvement':Previousorganinvolvement.objects.filter(studynumber = studynum),
                    'previouscomplication':Previouscomplication.objects.filter(studynumber = studynum)})


@login_required(login_url='login')
def enrollEditPost(request):
    if request.method == "POST":
        stnum = request.POST.get('studynum',)
        old_studyidentity = Studyidentity.objects.get(studynumber = stnum)
        old_studyidentity.dateofdiagnosis =  DateToNone(request.POST.get('dateofdiagnosis', ''))
        old_studyidentity.dateofenrollment = DateToNone(request.POST.get('dateofenrollment', ''))
        old_studyidentity.gender = request.POST.get('gender', '')
        old_studyidentity.dateofbirth = DateToNone(request.POST.get('dateofbirth', ''))
        old_studyidentity.religion = DateToNone(request.POST.get('religion', ''))
        old_studyidentity.education = DateToNone(request.POST.get('education', ''))
        old_studyidentity.maritalstatus = DateToNone(request.POST.get('maritalstatus', ''))
        old_studyidentity.region = DateToNone(request.POST.get('region', ''))
        old_studyidentity.occupation = DateToNone(request.POST.get('occupation', ''))
        old_studyidentity.income = DateToNone(request.POST.get('income', ''))
        old_studyidentity.save()
        
        old_slicc = Slicccriteria.objects.get(studynumber = stnum)
        old_slicc.slicc1 = CheckboxToBool(request.POST.get('slicc1', ''))
        old_slicc.slicc2 = CheckboxToBool(request.POST.get('slicc2', ''))
        old_slicc.slicc3 = CheckboxToBool(request.POST.get('slicc3', ''))
        old_slicc.slicc4 = CheckboxToBool(request.POST.get('slicc4', ''))
        old_slicc.slicc5 = CheckboxToBool(request.POST.get('slicc5', ''))
        old_slicc.slicc6 = CheckboxToBool(request.POST.get('slicc6', ''))
        old_slicc.slicc7 = CheckboxToBool(request.POST.get('slicc7', ''))
        old_slicc.slicc8 = CheckboxToBool(request.POST.get('slicc8', ''))
        old_slicc.slicc9 = CheckboxToBool(request.POST.get('slicc9', ''))
        old_slicc.slicc10 = CheckboxToBool(request.POST.get('slicc10', ''))
        old_slicc.slicc11 = CheckboxToBool(request.POST.get('slicc11', ''))
        old_slicc.slicc12 = CheckboxToBool(request.POST.get('slicc12', ''))
        old_slicc.slicc13 = CheckboxToBool(request.POST.get('slicc13', ''))
        old_slicc.slicc14 = CheckboxToBool(request.POST.get('slicc14', ''))
        old_slicc.slicc15 = CheckboxToBool(request.POST.get('slicc15', ''))
        old_slicc.slicc16 = CheckboxToBool(request.POST.get('slicc16', ''))
        old_slicc.slicc17 = CheckboxToBool(request.POST.get('slicc17', ''))
        old_slicc.save()
        
        old_arcc = Acrcriteria.objects.get(studynumber = stnum)
        old_arcc.acr1 = CheckboxToBool(request.POST.get('acr1', ''))
        old_arcc.acr2 = CheckboxToBool(request.POST.get('acr2', ''))
        old_arcc.acr3 = CheckboxToBool(request.POST.get('acr3', ''))
        old_arcc.acr4 = CheckboxToBool(request.POST.get('acr4', ''))
        old_arcc.acr5 = CheckboxToBool(request.POST.get('acr5', ''))
        old_arcc.acr6 = CheckboxToBool(request.POST.get('acr6', ''))
        old_arcc.acr7 = CheckboxToBool(request.POST.get('acr7', ''))
        old_arcc.acr8 = CheckboxToBool(request.POST.get('acr8', ''))
        old_arcc.acr9 = CheckboxToBool(request.POST.get('acr9', ''))
        old_arcc.acr10 = CheckboxToBool(request.POST.get('acr10', ''))
        old_arcc.acr11 = CheckboxToBool(request.POST.get('acr11', ''))
        old_arcc.save()

        old_condition = Medicalcondition.objects.get(studynumber = stnum)
        old_condition.mc1_1 = 'True' if request.POST.get('mc1_2', '')== '1' or request.POST.get('mc1_3', '')== '1' or request.POST.get('mc1_4', '')== '1' or request.POST.get('mc1_5', '')== '1' or request.POST.get('mc1_6', '')== '1' or request.POST.get('mc1_7', '')== '1' or request.POST.get('mc1_8', '')== '1' or request.POST.get('mc1_9', '')== '1' or request.POST.get('mc1_10', '')== '1' or request.POST.get('mc1_11', '')== '1' else 'False'
        old_condition.mc1_2 = CheckboxToBool(request.POST.get('mc1_2', ''))
        old_condition.mc1_3 = CheckboxToBool(request.POST.get('mc1_3', ''))
        old_condition.mc1_4 = CheckboxToBool(request.POST.get('mc1_4', ''))
        old_condition.mc1_5 = CheckboxToBool(request.POST.get('mc1_5', ''))
        old_condition.mc1_6 = CheckboxToBool(request.POST.get('mc1_6', ''))
        old_condition.mc1_7 = CheckboxToBool(request.POST.get('mc1_7', ''))
        old_condition.mc1_8 = CheckboxToBool(request.POST.get('mc1_8', ''))
        old_condition.mc1_9 = CheckboxToBool(request.POST.get('mc1_9', ''))
        old_condition.mc1_10 = CheckboxToBool(request.POST.get('mc1_10', ''))
        old_condition.mc1_11 = CheckboxToBool(request.POST.get('mc1_11', ''))
        old_condition.mc2_1 = 'True' if request.POST.get('mc2_2', '')== '1' or request.POST.get('mc2_3', '')== '1' or request.POST.get('mc2_4', '')== '1' or request.POST.get('mc2_5', '')== '1' or request.POST.get('mc2_6', '')== '1' else 'False'                                         
        old_condition.mc2_2 = CheckboxToBool(request.POST.get('mc2_2', ''))
        old_condition.mc2_3 = CheckboxToBool(request.POST.get('mc2_3', ''))
        old_condition.mc2_4 = CheckboxToBool(request.POST.get('mc2_4', ''))
        old_condition.mc2_5 = CheckboxToBool(request.POST.get('mc2_5', ''))
        old_condition.mc2_6 = CheckboxToBool(request.POST.get('mc2_6', ''))
        old_condition.mc3_1 = 'True' if request.POST.get('mc3_2', '')== '1' or request.POST.get('mc3_3', '')== '1' or request.POST.get('mc3_4', '')== '1' or request.POST.get('mc3_5', '')== '1' else 'False'  
        old_condition.mc3_2 = CheckboxToBool(request.POST.get('mc3_2', ''))
        old_condition.mc3_3 = CheckboxToBool(request.POST.get('mc3_3', ''))
        old_condition.mc3_4 = CheckboxToBool(request.POST.get('mc3_4', ''))
        old_condition.mc3_5 = CheckboxToBool(request.POST.get('mc3_5', ''))
        old_condition.mc4_1 = 'True' if request.POST.get('mc4_2', '')== '1' or request.POST.get('mc4_3', '')== '1' or request.POST.get('mc4_4', '')== '1' or request.POST.get('mc4_5', '')== '1' or request.POST.get('mc4_6', '')== '1' or request.POST.get('mc4_7', '')== '1' or request.POST.get('mc4_8', '')== '1' else 'False'
        old_condition.mc4_2 = CheckboxToBool(request.POST.get('mc4_2', ''))
        old_condition.mc4_3 = CheckboxToBool(request.POST.get('mc4_3', ''))
        old_condition.mc4_4 = CheckboxToBool(request.POST.get('mc4_4', ''))
        old_condition.mc4_5 = CheckboxToBool(request.POST.get('mc4_5', ''))
        old_condition.mc4_6 = CheckboxToBool(request.POST.get('mc4_6', ''))
        old_condition.mc4_7 = CheckboxToBool(request.POST.get('mc4_7', ''))
        old_condition.mc4_8 = CheckboxToBool(request.POST.get('mc4_8', ''))
        old_condition.mc4_9 = ListToArray(request.POST.getlist('mc4_9[]',))
        old_condition.mc5_1 = 'True' if request.POST.get('mc5_2_1', '')!='' or request.POST.get('mc5_2_2', '')!='' or request.POST.get('mc5_2_3', '')!='' or request.POST.get('mc5_3_1', '')!='' or request.POST.get('mc5_3_2', '')!='' or request.POST.get('mc5_3_3', '')!='' or request.POST.get('mc5_4_1', '')!='' or request.POST.get('mc5_4_2', '')!='' or request.POST.get('mc5_5_1', '')!='' or request.POST.get('mc5_5_2', '')!='' else 'False' 
        old_condition.mc5_2 = 'True' if request.POST.get('mc5_2_1', '')!='' or request.POST.get('mc5_2_2', '')!='' or request.POST.get('mc5_2_3', '')!='' else 'False' 
        old_condition.mc5_2_1 = request.POST.get('mc5_2_1', '')
        old_condition.mc5_2_2 = DateToNone(request.POST.get('mc5_2_2', ''))
        old_condition.mc5_2_3 = DateToNone(request.POST.get('mc5_2_3', ''))
        old_condition.mc5_3 = 'True' if request.POST.get('mc5_3_1', '')!='' or request.POST.get('mc5_3_2', '')!='' or request.POST.get('mc5_3_3', '')!='' else 'False' 
        old_condition.mc5_3_1 = request.POST.get('mc5_3_1', '')
        old_condition.mc5_3_2 = DateToNone(request.POST.get('mc5_3_2', ''))
        old_condition.mc5_3_3 = DateToNone(request.POST.get('mc5_3_3', ''))
        old_condition.mc5_4 = 'True' if request.POST.get('mc5_4_1', '')!='' or request.POST.get('mc5_4_2', '')!='' else 'False' 
        old_condition.mc5_4_1 = request.POST.get('mc5_4_1', '')
        old_condition.mc5_4_2 = DateToNone(request.POST.get('mc5_4_2', ''))
        old_condition.mc5_5 = 'True' if request.POST.get('mc5_5_1', '')!='' or request.POST.get('mc5_5_2', '')!='' else 'False' 
        old_condition.mc5_5_1 = request.POST.get('mc5_5_1', '')
        old_condition.mc5_5_2 = DateToNone(request.POST.get('mc5_5_2', ''))
        old_condition.save()
        
        Previousorganinvolvement.objects.filter(studynumber = stnum).delete()
        Previouscomplication.objects.filter(studynumber = stnum).delete()

        OrganDate = request.POST.getlist('OrganDate[]',)
        OrganOrgan = request.POST.getlist('Organ[]',)
        OrganTreat = request.POST.getlist('OrganTreat[]',)
        OrganResult = request.POST.getlist('OrganResult[]',)
        for i in range(0, len(OrganDate)):
            EnrollOrgan = Previousorganinvolvement(studynumber = old_studyidentity, detail = Previoustype(date = DateToNone(OrganDate[i]), organ = OrganOrgan[i], treatment = OrganTreat[i], result = OrganResult[i]))
            EnrollOrgan.save()
        
        CompDate = request.POST.getlist('CompDate[]',)
        CompOrgan = request.POST.getlist('CompOrgan[]',)
        CompTreat = request.POST.getlist('CompTreat[]',)
        CompRemiss = request.POST.getlist('CompRemiss[]',)
        for i in range(0, len(OrganDate)):
            EnrollComp = Previouscomplication(studynumber = old_studyidentity, detail = Previoustype(date = DateToNone(CompDate[i]), organ = CompOrgan[i], treatment = CompTreat[i], result = CompRemiss[i]))
            EnrollComp.save()
            
        old_fam = Familyhistory.objects.get(studynumber = stnum)
        old_fam.familyhistoryofautoimmunedisease = request.POST.get('FamAuto',) 
        old_fam.systemicautoimmune = CheckboxToBool(request.POST.get('systemicautoimmune',)) 
        old_fam.sle = ListToArray(request.POST.getlist('sle[]',))
        old_fam.ra = ListToArray(request.POST.getlist('ra[]',))
        old_fam.dermatomyositis = ListToArray(request.POST.getlist('dermatomyositis[]',))
        old_fam.systemicsclerosis = ListToArray(request.POST.getlist('systemicsclerosis[]',))
        old_fam.sjogrensyndrome = ListToArray(request.POST.getlist('sjogrensyndrome[]',))
        old_fam.tissuespecificautoimmune = CheckboxToBool(request.POST.get('tissuespecificautoimmune',)) 
        old_fam.dmtypeone = ListToArray(request.POST.getlist('dmtypeone[]',))
        old_fam.hashimotosthyroiditis = ListToArray(request.POST.getlist('hashimotosthyroiditis[]',))
        old_fam.multiplesclerosis = ListToArray(request.POST.getlist('multiplesclerosis[]',))
        old_fam.myastheniagravis = ListToArray(request.POST.getlist('myastheniagravis[]',))
        old_fam.tissuespecificother = ListToArray(request.POST.getlist('tissuespecificother[]',))
        old_fam.renaldiseasefamilyhistory = request.POST.get('FamRenal',)
        old_fam.nephroticsyndrome_glomerulardisease = ListToArray(request.POST.getlist('nephroticsyndrome_glomerulardisease[]',))
        old_fam.stone = ListToArray(request.POST.getlist('stone[]',))
        old_fam.esrd = ListToArray(request.POST.getlist('esrd[]',))
        old_fam.renalother = ListToArray(request.POST.getlist('renalother[]',))
        old_fam.save()
    
        return render(request, 'enrollment-detail.html',
                {'patient':Studyidentity.objects.get(studynumber = stnum),
                   'acrcriteria':Acrcriteria.objects.get(studynumber = stnum),
                   'slicccriteria':Slicccriteria.objects.get(studynumber = stnum),
                    'familyhistory':Familyhistory.objects.get(studynumber = stnum),
                    'medicalcondition':Medicalcondition.objects.get(studynumber = stnum),
                    'previousorganinvolvement':Previousorganinvolvement.objects.filter(studynumber = stnum),
                    'previouscomplication':Previouscomplication.objects.filter(studynumber = stnum)})