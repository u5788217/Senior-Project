from django.shortcuts import render
from django.http import HttpResponse

#Models for enrollment
from .models import Studyidentity, Slicccriteria, Acrcriteria, Medicalcondition, Previoustype
from .models import Labtype, Medicationtype, Previoustype
from .models import Visiting, Clinicalpresentation, Damageindex, Diseaseactivitysledai, Laboratoryinventoryinvestigation, Lnlab, Medication

from django.contrib.postgres.fields import ArrayField

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

def my_view_that_updates_pieFact(request):
    if request.method == 'POST':
        if 'pieFact' in request.POST:
            pieFact = request.POST['pieFact']
            # doSomething with pieFact here...
            return HttpResponse('success') # if everything is OK
    # nothing went well
    return HttpRepsonse('FAIL!!!!!')

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
    return render(request, 'enrollment-add.html',{'a': ArrayField(Previoustype)})

def enrollPatient(request):
    if request.method == "POST":
        #All data feilds
        #create studynumber+1
        stnum = 4
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

                mc4_9 = request.POST.get('mc4_9', ''),

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
    
    return render(request, 'enrollment-detail.html',{'EnrollSlicccriteria': EnrollSlicccriteria.slicc1})

def followPatient(request):
    if request.method == "POST":
        TempstudyNumber = 4
        Followvisiting = Visiting(studynumber = Studyidentity.objects.get(studynumber = TempstudyNumber),
                            visitdate =  request.POST.get('visitdate', ''),
                            bp = request.POST.get('bp', ''),
                            height = ToFloat(request.POST.get('height', '')),
                            weight = ToFloat(request.POST.get('weight', '')))
        Followvisiting.save()

        Followclinic = Clinicalpresentation(studynumber = Studyidentity.objects.get(studynumber = TempstudyNumber),
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
        
        Followdamage = Damageindex(studynumber = Studyidentity.objects.get(studynumber = TempstudyNumber),
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
                    
        FollowSLEDAI = Diseaseactivitysledai(studynumber = Studyidentity.objects.get(studynumber = TempstudyNumber),
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
            
        Followlab = Laboratoryinventoryinvestigation(studynumber = Studyidentity.objects.get(studynumber = TempstudyNumber),
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
        
        FollowMed = Medication(studynumber = Studyidentity.objects.get(studynumber = TempstudyNumber),
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
        
        #All data feilds
    return render(request, 'followup-detail.html')