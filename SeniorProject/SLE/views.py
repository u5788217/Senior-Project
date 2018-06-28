from django.shortcuts import render
from django.http import HttpResponse
from django.http import StreamingHttpResponse

from django.urls import reverse
from django.http import HttpResponseRedirect

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required

from django.utils.timezone import datetime
from datetime import timedelta
import datetime

from .models import AuthUser
#Models for enrollment
from .models import Studyidentity, Slicccriteria, Acrcriteria, Medicalcondition, Previousorganinvolvement, Familyhistory, Obgyn, Riskbehavior, Comorbidity, HN, Obgyn, Othermedication
from .models import Labtype, Medicationtype
from .models import Visiting, Clinicalpresentation, Damageindex, Diseaseactivitysledai, Laboratoryinventoryinvestigation, Lnlab, Medication

from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ObjectDoesNotExist

from sklearn.preprocessing import StandardScaler
import pandas as pd
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
from sklearn.externals import joblib

import numpy as np
import os
from django.conf import settings
from django.templatetags.static import static

try:
    from itertools import izip as zip
except ImportError: # will be 3.x series
    pass

from operator import attrgetter

def StringToNone(checkbox,string):
    if checkbox == '0' or checkbox == '' or checkbox == 'off': string = None
    return string

def iscontains(alist,item):
    if item in alist: return True
    else: return False
def NullToZero(value):
    if value is None or value == '': value = 0
    return value

def getRowForPredict(studynumber):
    latest_visit = None
    latest_lab = None
    latest_sledai = None
    latest_med = None
    latest_cp = None
    now = datetime.datetime.now().date()
    try:
        latest_visit = Visiting.objects.filter(studynumber = studynumber).latest('visitdate')
        latest_lab = Laboratoryinventoryinvestigation.objects.get(visitingid = latest_visit)
        latest_sledai = Diseaseactivitysledai.objects.get(visitingid = latest_visit)
        latest_med = Medication.objects.get(visitingid = latest_visit)
        latest_cp = Clinicalpresentation.objects.get(visitingid = latest_visit)
    except ObjectDoesNotExist:
        latest_visit = None
        latest_lab = None
        latest_sledai = None
        latest_med = None
        latest_cp = None
    
    if(latest_visit is not None and latest_visit.bp is not None): 
        if(latest_visit.studynumber.gender == 'Male'):
            Gender = 0
        else: 
            Gender = 1
        if(latest_visit.studynumber.dateofbirth is not None):
            delta = now-latest_visit.studynumber.dateofbirth
            Age = int(delta.total_seconds()*3.17098e-8)
        else: Age = 0
        if(latest_visit.nextvisit is not None):
            temp = latest_visit.nextvisit-latest_visit.visitdate
            LastVisit = int(temp.total_seconds()*1.15741E-5)
        else:
            LastVisit = 62
        BP = latest_visit.bp.split('/')
        try:
            BP1 = NullToZero(BP[0])
            BP2 = NullToZero(BP[1])
        except IndexError:
            BP1 = 0
            BP2 = 0
    else:
        BP1 = 0
        BP2 = 0
        Gender = 0
        Age = 0
        LastVisit = 0
    
    if(latest_lab is not None): 
        Albumin = NullToZero(latest_lab.albumin)
        Anti_CIC = 1 if latest_lab.anticic == 'Negative' else 0
        Anti_dsDNA = NullToZero(latest_lab.anti_dsdna)
        C3 = NullToZero(latest_lab.c3)
        C4 = NullToZero(latest_lab.c4)
        Cr = NullToZero(latest_lab.cr)
        ESR = NullToZero(latest_lab.esr)
        Hb = NullToZero(latest_lab.hb)
        Platelets = NullToZero(latest_lab.platelets)
        RBC_HPF = NullToZero(latest_lab.rbc_hpf1)
        UPCI = NullToZero(latest_lab.upci)
        WBC = NullToZero(latest_lab.wbc)
        WBC_HPF = NullToZero(latest_lab.wbc_hpf1)
    else:
        Albumin = 0
        Anti_CIC = 0
        Anti_dsDNA =0
        C3 = 0
        C4 = 0
        Cr = 0
        ESR = 0
        Hb = 0
        Platelets = 0
        RBC_HPF = 0
        UPCI = 0
        WBC = 0
        WBC_HPF =0
    if(latest_cp is not None): 
        Fatigue = NullToZero(latest_cp.cp_1 )
        WeightLoss = NullToZero(latest_cp.cp_2)
        MalarRash = NullToZero(latest_cp.cp_3)
        if(latest_cp.cp_6 is not None): OtherRash = 1
        else: OtherRash = 0
        OralOrNasopharyngealUlcers = NullToZero(latest_cp.cp_8)
        Photosensitivity = NullToZero(latest_cp.cp_7)
        Dif_Alopecia = NullToZero(latest_cp.cp_10)
        Edema = NullToZero(latest_cp.cp_16)
        Oliguria = NullToZero(latest_cp.cp_17)
        Arthralgias = NullToZero(latest_cp.cp_28)
    else:
        Fatigue = 0
        WeightLoss = 0
        MalarRash = 0
        OtherRash = 0
        OralOrNasopharyngealUlcers = 0
        Photosensitivity = 0
        Dif_Alopecia = 0
        Edema = 0
        Oliguria = 0
        Arthralgias = 0
    if(latest_med is not None): 
        CQ = 0 if latest_med.msle_2_1 is None else NullToZero(latest_med.msle_2_1.doseperdate)
        HCQ = 0 if latest_med.msle_2_2 is None else NullToZero(latest_med.msle_2_2.doseperdate)
        Prednisolone = 0 if latest_med.msle_3_1 is None else NullToZero(latest_med.msle_3_1.doseperdate)
        MethylprednisoloneIV = 0 if latest_med.msle_3_3 is None else NullToZero(latest_med.msle_3_2.doseperdate)
        DexamethasoneIV = 0 if latest_med.msle_3_3 is None else NullToZero(latest_med.msle_3_3.doseperdate)
        MTX = 0 if latest_med.msle_4_1 is None else NullToZero(latest_med.msle_4_1.doseperdate)
        Azathioprine = 0 if latest_med.msle_4_2 is None else NullToZero(latest_med.msle_4_2.doseperdate)
        CyclophosphamideOral = 0 if latest_med.msle_4_3 is None else NullToZero(latest_med.msle_4_3.doseperdate)
        CyclophosphamideIV = 0 if latest_med.msle_4_4 is None else NullToZero(latest_med.msle_4_4.doseperdate)
        MMF = 0 if latest_med.msle_4_5 is None else NullToZero(latest_med.msle_4_5.doseperdate)
        Myfortic = 0 if latest_med.msle_4_6 is None else NullToZero(latest_med.msle_4_6.doseperdate)
        CyclosporinA = 0 if latest_med.msle_4_7 is None else NullToZero(latest_med.msle_4_7.doseperdate)
        Tacrolimus_Prograft = 0 if latest_med.msle_4_8 is None else NullToZero(latest_med.msle_4_8.doseperdate)
        Danazol = 0 if latest_med.msle_4_9 is None else NullToZero(latest_med.msle_4_9.doseperdate)
        Colchicine = 0 if latest_med.msle_4_11 is None else NullToZero(latest_med.msle_4_11.doseperdate)
        Statins = 0 if latest_med.mgt_2_1 is None else NullToZero(latest_med.mgt_2_1.doseperdate)
        Bisphosphonates = 0 if latest_med.mgt_3_1 is None else NullToZero(latest_med.mgt_3_1.doseperdate)
        CaCO3 = 0 if latest_med.mgt_3_2 is None else NullToZero(latest_med.mgt_3_2.doseperdate)
        VitaminD = 0 if latest_med.mgt_3_3 is None else NullToZero(latest_med.mgt_3_3.doseperdate)
        ASA = 0 if latest_med.mgt_4_1 is None else NullToZero(latest_med.mgt_4_1.doseperdate)
        Warfarin = 0 if latest_med.mgt_4_2 is None else NullToZero(latest_med.mgt_4_2.doseperdate)
        FolicAcid = 0 if latest_med.mgt_4_3 is None else NullToZero(latest_med.mgt_4_3.doseperdate)
        Other = 1 if latest_med.mgt_4_4 == 'True' else 0
    else:
        CQ = 0
        HCQ = 0
        Prednisolone = 0
        MethylprednisoloneIV = 0
        DexamethasoneIV = 0
        MTX = 0
        Azathioprine = 0
        CyclophosphamideOral = 0
        CyclophosphamideIV = 0
        MMF = 0
        Myfortic = 0
        CyclosporinA = 0
        Tacrolimus_Prograft = 0
        #Danazol = 0
        Colchicine = 0
        Statins = 0
        Bisphosphonates = 0
        CaCO3 = 0
        VitaminD = 0
        ASA = 0
        Warfarin = 0
        FolicAcid = 0
        Other = 0
    if(latest_sledai is not None): 
        Psychosis = NullToZero(latest_sledai.psychosis)
        OrganicBrainSyndrome = NullToZero(latest_sledai.organicbrainsyndrome)
        LupusHeadache = NullToZero(latest_sledai.lupusheadache)
        CVA = NullToZero(latest_sledai.cva)
        Vasculitis = NullToZero(latest_sledai.vasculitis)
        Arthritis = NullToZero(latest_sledai.arthritis)
        Casts = NullToZero(latest_sledai.casts)
        Pyuria = NullToZero(latest_sledai.pyuria)
        NewRash = NullToZero(latest_sledai.rash)
        Alopecia = NullToZero(latest_sledai.alopecia)
        MucousMembrane = NullToZero(latest_sledai.mucousmembrane)
        Pleurisy = NullToZero(latest_sledai.pleurisy)
        Pericarditis = NullToZero(latest_sledai.pericarditis)
    else:
        Psychosis = 0
        OrganicBrainSyndrome = 0
        LupusHeadache = 0
        CVA = 0
        Vasculitis = 0
        Arthritis = 0
        Casts = 0
        Pyuria = 0
        NewRash = 0
        Alopecia = 0
        MucousMembrane = 0
        Pleurisy = 0
        Pericarditis = 0
        
    Case = np.array([[Gender,Age,LastVisit,BP1,BP2,Albumin,Anti_CIC,Anti_dsDNA,C3,C4,Cr,ESR,Hb,Platelets,RBC_HPF,UPCI,WBC,WBC_HPF,Fatigue,WeightLoss,MalarRash,OtherRash,Photosensitivity,OralOrNasopharyngealUlcers,Dif_Alopecia,Edema,Oliguria,Arthralgias,CQ,HCQ,Prednisolone,MethylprednisoloneIV,DexamethasoneIV,MTX,Azathioprine,CyclophosphamideOral,CyclophosphamideIV,MMF,Myfortic,CyclosporinA,Tacrolimus_Prograft,Colchicine,Statins,Bisphosphonates,CaCO3,VitaminD,ASA,Warfarin,FolicAcid,Other,Psychosis,OrganicBrainSyndrome,LupusHeadache,CVA,Vasculitis,Arthritis,Casts,Pyuria,NewRash,Alopecia,MucousMembrane,Pleurisy,Pericarditis]], np.float64)
    project_path = settings.PROJECT_ROOT
    scFile = project_path+'/sc.sav'
    loaded_sc = joblib.load(scFile)
    Case = loaded_sc.transform(Case)

    return Case

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
    if lab is not None:
        if lab.lnlabid is not None:
            try:
                ln = Lnlab.objects.get(lnlabid = lab.lnlabid.lnlabid) 
                return True
            except ObjectDoesNotExist:
                ln = None
                return False
        else:
            return False
    else:return False
        
def CheckboxToInt(string):
    if string == 'on' or string == 'Pos' or string is True or string=='On': string = 1
    else : 
        if string == 'off' or string == 'Neg' or string is False or string is None or string == '' or string == 'No': string = 0
    return int(string)

def ToFloat(string):
    if string == '0.0' or string == '' or string is None: return None
    else: return float(string)

def ToFloatMed(string):
    if string == '0.0' or string == '' or string is None: return 0
    else: return float(string)
    
def ToFloatNone(string):
    if string == '0.0' or string == '' or string is None: return None
    else: return float(string)

def CheckboxToBool(string):
    if string == '1' or string == 'on': return 'True'
    else : return 'False'

def DateToNone(date):
    if date == '': date = None
    return date

def login(request):
    if request.user.is_authenticated is True:
        return render(request, 'index.html',{'patients': Studyidentity.objects.all()})
    else :
        return render(request, 'login.html')

def getACRdata():
    ACRdata =[]
    acrsum1=0
    acrsum2=0
    acrsum3=0
    acrsum4=0
    acrsum5=0
    acrsum6=0
    acrsum7=0
    acrsum8=0
    acrsum9=0
    acrsum10=0
    acrsum11=0
    for d in Acrcriteria.objects.all():
        if d.acr1 is True: acrsum1 += 1
        if d.acr2 is True: acrsum2 += 1
        if d.acr3 is True: acrsum3 += 1
        if d.acr4 is True: acrsum4 += 1
        if d.acr5 is True: acrsum5 += 1
        if d.acr6 is True: acrsum6 += 1
        if d.acr7 is True: acrsum7 += 1
        if d.acr8 is True: acrsum8 += 1
        if d.acr9 is True: acrsum9 += 1
        if d.acr10 is True: acrsum10 += 1
        if d.acr11 is True: acrsum11 += 1
    ACRdata.append({'name':'Serositis','sum':acrsum1})    
    ACRdata.append({'name':'Malar Rash','sum':acrsum2})
    ACRdata.append({'name':'Renal Disorder','sum':acrsum3})
    ACRdata.append({'name':'Discoid Rash','sum':acrsum4})
    ACRdata.append({'name':'Neurological Disorder','sum':acrsum5})
    ACRdata.append({'name':'Photosensitivity','sum':acrsum6})
    ACRdata.append({'name':'Haematological Disorder','sum':acrsum7})
    ACRdata.append({'name':'Oral Ulcers','sum':acrsum8})
    ACRdata.append({'name':'Immunological Disorder','sum':acrsum9})
    ACRdata.append({'name':'Arthritis','sum':acrsum10})
    ACRdata.append({'name':'PositiveANA','sum':acrsum11})
    return ACRdata

def SLICCdataTop5():
    SLICCdata =[]
    slicc1=0
    slicc2=0
    slicc3=0
    slicc4=0
    slicc5=0
    slicc6=0
    slicc7=0
    slicc8=0
    slicc9=0
    slicc10=0
    slicc11=0
    slicc12=0
    slicc13=0
    slicc14=0
    slicc15=0
    slicc16=0
    slicc17=0
    for d in Slicccriteria.objects.all():
        if d.slicc1 is True: slicc1 += 1
        if d.slicc2 is True: slicc2 += 1
        if d.slicc3 is True: slicc3 += 1
        if d.slicc4 is True: slicc4 += 1
        if d.slicc5 is True: slicc5 += 1
        if d.slicc6 is True: slicc6 += 1
        if d.slicc7 is True: slicc7 += 1
        if d.slicc8 is True: slicc8 += 1
        if d.slicc9 is True: slicc9 += 1
        if d.slicc10 is True: slicc10 += 1
        if d.slicc11 is True: slicc11 += 1
        if d.slicc12 is True: slicc12 += 1
        if d.slicc13 is True: slicc13 += 1
        if d.slicc14 is True: slicc14 += 1
        if d.slicc15 is True: slicc15 += 1
        if d.slicc16 is True: slicc16 += 1
        if d.slicc17 is True: slicc17 += 1
    SLICCdata.append({'name':'AcuteCutaneous', 'sum':slicc1})    
    SLICCdata.append({'name':'ChronicCutaneous', 'sum':slicc2})
    SLICCdata.append({'name':'MucosalUlcer', 'sum':slicc3})
    SLICCdata.append({'name':'NonScaringAlopecia', 'sum':slicc4})
    SLICCdata.append({'name':'Arthritis', 'sum':slicc5})
    SLICCdata.append({'name':'Serositis', 'sum':slicc6})
    SLICCdata.append({'name':'Renal', 'sum':slicc7})
    SLICCdata.append({'name':'Neuro', 'sum':slicc8})
    SLICCdata.append({'name':'HemolyticAnemia', 'sum':slicc9})
    SLICCdata.append({'name':'Leukopenia', 'sum':slicc10})
    SLICCdata.append({'name':'Thrombocytopenia', 'sum':slicc11})
    SLICCdata.append({'name':'ANA', 'sum':slicc12})
    SLICCdata.append({'name':'AntiDNA', 'sum':slicc13})
    SLICCdata.append({'name':'AntiSm', 'sum':slicc14})
    SLICCdata.append({'name':'AntiPhospholipid', 'sum':slicc15})
    SLICCdata.append({'name':'LowComplement', 'sum':slicc16})
    SLICCdata.append({'name':'DirectCoombsTest', 'sum':slicc17})
    SLICCdata = sorted(SLICCdata, key=lambda SLICC: int(SLICC['sum']), reverse=True)
    slicc_top5 = SLICCdata[:5] 
    return slicc_top5

def getGenderdata():
    Gender = []
    Gender.append({'Gender':'Female', 'num':Studyidentity.objects.filter(gender = 'Female').count()})    
    Gender.append({'Gender':'Male', 'num':Studyidentity.objects.filter(gender = 'Male').count()})
    return Gender


def getCurrentStatus():
    Status = []
    flare = 0
    active = 0
    inactive = 0
    total = 0
    donthavevisit = []
    for patient in Studyidentity.objects.all():
        latest_visit = None
        try:
            latest_visit = Diseaseactivitysledai.objects.filter(studynumber = patient).latest('visitdate')
            if(latest_visit.status == 'flare'): flare += 1
            if(latest_visit.status == 'active'): active += 1
            if(latest_visit.status == 'inactive'): inactive += 1
        except ObjectDoesNotExist:
            latest_visit = None
            donthavevisit.append(patient)
    Status.append({'Status':'Flare', 'num':flare})    
    Status.append({'Status':'Active', 'num':active})
    Status.append({'Status':'Inactive', 'num':inactive})
    Status.append({'Status':'Total', 'num':Studyidentity.objects.all().count})
    Status.append({'Status':'donthavevisit', 'num':donthavevisit})
    return Status

def getAges():
    Ages = []
    now = datetime.datetime.now().date()
    Group1 = 0
    Group2 = 0
    Group3 = 0
    Group4 = 0
    Group5 = 0
    Group6 = 0
    Group7 = 0
    for patient in Studyidentity.objects.all():
        if(patient.dateofbirth is not None):
            delta = now-patient.dateofbirth
            age = int(delta.total_seconds()*3.17098e-8)
            if(age < 21): Group1 += 1
            if(age > 20 and age < 31): Group2 += 1
            if(age > 30 and age < 41): Group3 += 1
            if(age > 40 and age < 51): Group4 += 1
            if(age > 50 and age < 61): Group5 += 1
            if(age > 60): Group6 += 1
        else: Group7 += 1
    Ages.append({'Group':'less 20', 'Number':Group1}) 
    Ages.append({'Group':'20-30', 'Number':Group2}) 
    Ages.append({'Group':'30-40', 'Number':Group3}) 
    Ages.append({'Group':'40-50', 'Number':Group4}) 
    Ages.append({'Group':'50-60', 'Number':Group5}) 
    Ages.append({'Group':'more 60', 'Number':Group6}) 
    Ages.append({'Group':'Missing', 'Number':Group7})
    return Ages


def index(request):
    if request.method == "POST": 
        user_auth = request.POST.get('username',)
        user = authenticate(request, username = user_auth, password = request.POST.get('password',))
        if user is not None:
            auth_login(request, user)
            ACRdata = getACRdata()
            slicc_top5 = SLICCdataTop5()
            Gender = getGenderdata()
            Status = getCurrentStatus()
            Ages = getAges()
            project_path = settings.PROJECT_ROOT
            modelFile = project_path+'/final_gbmodel_joblib.sav'
            loaded_model = joblib.load(modelFile)
            Result = []
            for p in Studyidentity.objects.all(): 
                test = getRowForPredict(p)
                result = loaded_model.predict(test)
                if result[0] == 1: 
                    Result.append({'St':p, 'status':'Flare'})
                else:
                    Result.append({'St':p, 'status':'Not flare'})
            result_list = []
            for sn in Studyidentity.objects.all():
                result_list.append({'sn':sn, 'hn': HN.objects.get(studynumber = sn.studynumber)})
            return render(request, 'index.html',{'patients': result_list, 
                                                 'ACRdata':ACRdata, 
                                                 'SLICCdata':slicc_top5,
                                                 'Gender':Gender,
                                                 'Status':Status,
                                                 'Ages':Ages,
                                                 'PredictResult':Result})
        else:
            return render(request, 'login.html',{
                'login_message' : 'Incorrect username or password.',})
    else:
        if request.user.is_authenticated:
            ACRdata = getACRdata()
            slicc_top5 = SLICCdataTop5()
            Gender = getGenderdata()
            Status = getCurrentStatus()
            Ages = getAges()
            project_path = settings.PROJECT_ROOT
            modelFile = project_path+'/final_gbmodel_joblib.sav'
            loaded_model = joblib.load(modelFile)
            Result = []
            for p in Studyidentity.objects.all(): 
                test = getRowForPredict(p)
                result = loaded_model.predict(test)
                if result[0] == 1: 
                    Result.append({'St':p, 'status':'Flare'})
                else:
                    Result.append({'St':p, 'status':'Not flare'})
            result_list = []
            for sn in Studyidentity.objects.all():
                result_list.append({'sn':sn, 'hn': HN.objects.get(studynumber = sn.studynumber)})
           
            return render(request, 'index.html',{'patients': result_list, 
                                                 'ACRdata':ACRdata, 
                                                 'SLICCdata':slicc_top5,
                                                 'Gender':Gender,
                                                 'Status':Status,
                                                 'Ages':Ages,
                                                 'PredictResult':Result})
        else:
            return render(request, 'login.html',{
                'login_message' : 'Incorrect username or password.',})

def logout(request):
    #clear session
    auth_logout(request)
    return render(request, 'login.html')

@login_required(login_url='login')
def patientrecord(request, studynum):
    project_path = settings.PROJECT_ROOT
    modelFile = project_path+'/final_gbmodel_joblib.sav'
    loaded_model = joblib.load(modelFile)
    test = getRowForPredict(studynum)
    result = loaded_model.predict(test)
    
    SLEDAIdata =[]   
    sledai1 = []
    sledai2 = []
    sledai3 = []
    sledai4 = []
    sledai5 = []
    sledai6 = []
    sledai7 = []
    sledai8 = []
    sledai9 = []
    sledai10 = []
    sledai11 = []
    sledai12 = []
    sledai13 = []
    sledai14 = []
    sledai15 = []
    sledai16 = []
    sledai17 = []
    sledai18 = []
    sledai19 = []
    sledai20 = []
    sledai21 = []
    sledai22 = []
    sledai23 = []
    sledai24 = []
    sledai25 = []
    sledai26 = []
    sledai27 = []
    all_sledai = Diseaseactivitysledai.objects.filter(studynumber = studynum)
    for each_sledai in all_sledai:
        sledai1.append(CheckboxToInt(each_sledai.seizure))
        sledai2.append(CheckboxToInt(each_sledai.psychosis))
        sledai3.append(CheckboxToInt(each_sledai.organicbrainsyndrome))
        sledai4.append(CheckboxToInt(each_sledai.visualdisturbance))
        sledai5.append(CheckboxToInt(each_sledai.cranialnerve))
#        sledai6.append(CheckboxToInt(each_sledai.cranialnervedetail))
        sledai7.append(CheckboxToInt(each_sledai.lupusheadache))
        sledai8.append(CheckboxToInt(each_sledai.cva))
        sledai9.append(CheckboxToInt(each_sledai.vasculitis))
        sledai10.append(CheckboxToInt(each_sledai.arthritis))
        sledai11.append(CheckboxToInt(each_sledai.arthritisjointamount))
        sledai12.append(CheckboxToInt(each_sledai.myositis))
        sledai13.append(CheckboxToInt(each_sledai.casts))
        sledai14.append(CheckboxToInt(each_sledai.hematuria))
        sledai15.append(CheckboxToInt(each_sledai.proteinuria))
        sledai16.append(CheckboxToInt(each_sledai.pyuria))
        sledai17.append(CheckboxToInt(each_sledai.lowcomplement))
        sledai18.append(CheckboxToInt(each_sledai.increaseddnabinding))
        sledai19.append(CheckboxToInt(each_sledai.rash))
        sledai20.append(CheckboxToInt(each_sledai.alopecia))
        sledai21.append(CheckboxToInt(each_sledai.mucousmembrane))
        sledai22.append(CheckboxToInt(each_sledai.pleurisy))
        sledai23.append(CheckboxToInt(each_sledai.pericarditis))
        sledai24.append(CheckboxToInt(each_sledai.thrombocytopenia))
        sledai25.append(CheckboxToInt(each_sledai.leukopenia))
        sledai26.append(CheckboxToInt(each_sledai.fever))
        sledai27.append(each_sledai.sledai_total)
    SLEDAIdata.append({'name':'Seizure', 'values':sledai1})    
    SLEDAIdata.append({'name':'Psychosis', 'values':sledai2})
    SLEDAIdata.append({'name':'OrganicBrainSyndrome', 'values':sledai3})
    SLEDAIdata.append({'name':'VisualDisturbance', 'values':sledai4})
    SLEDAIdata.append({'name':'CranialNerve', 'values':sledai5})
#    SLEDAIdata.append({'name':'CranialNerveDetail', 'values':sledai6})
    SLEDAIdata.append({'name':'LupusHeadache', 'values':sledai7})
    SLEDAIdata.append({'name':'CVA', 'values':sledai8})
    SLEDAIdata.append({'name':'Vasculitis', 'values':sledai9})
    SLEDAIdata.append({'name':'Arthritis', 'values':sledai10})
    SLEDAIdata.append({'name':'ArthritisJointAmount', 'values':sledai11})
    SLEDAIdata.append({'name':'Myositis', 'values':sledai12})
    SLEDAIdata.append({'name':'Casts', 'values':sledai13})
    SLEDAIdata.append({'name':'Hematuria', 'values':sledai14})
    SLEDAIdata.append({'name':'Proteinuria', 'values':sledai15})
    SLEDAIdata.append({'name':'Pyuria', 'values':sledai16})
    SLEDAIdata.append({'name':'LowComplement', 'values':sledai17})
    SLEDAIdata.append({'name':'IncreasedDNAbinding', 'values':sledai18})
    SLEDAIdata.append({'name':'Rash', 'values':sledai19})
    SLEDAIdata.append({'name':'Alopecia', 'values':sledai20})
    SLEDAIdata.append({'name':'MucousMembrane', 'values':sledai21})
    SLEDAIdata.append({'name':'Pleurisy', 'values':sledai22})
    SLEDAIdata.append({'name':'Pericarditis', 'values':sledai23})
    SLEDAIdata.append({'name':'Thrombocytopenia', 'values':sledai24})
    SLEDAIdata.append({'name':'Leukopenia', 'values':sledai25})
    SLEDAIdata.append({'name':'Fever', 'values':sledai26})
    SLEDAIdata.append({'name':'Total', 'values':sledai27})
    
    MEDdata = []
    med1 = []
    med2 = []
    med3 = []
    med4 = []
    med5 = []
    med6 = []
    med7 = []
    med8 = []
    med9 = []
    all_med = Medication.objects.filter(studynumber = studynum)
    for each_med in all_med:
        if each_med.msle_2_1 is not None: med1.append(ToFloat(each_med.msle_2_1.doseperdate))
        if each_med.msle_2_2 is not None: med2.append(ToFloat(each_med.msle_2_2.doseperdate))
        if each_med.msle_3_1 is not None: med3.append(ToFloat(each_med.msle_3_1.doseperdate))
        if each_med.msle_4_1 is not None: med4.append(ToFloat(each_med.msle_4_1.doseperdate))
        if each_med.msle_4_2 is not None: med5.append(ToFloat(each_med.msle_4_2.doseperdate))
        if each_med.msle_4_3 is not None: med6.append(ToFloat(each_med.msle_4_3.doseperdate))
        if each_med.msle_4_5 is not None: med7.append(ToFloat(each_med.msle_4_5.doseperdate))
        if each_med.msle_4_7 is not None: med8.append(ToFloat(each_med.msle_4_7.doseperdate))
        if each_med.msle_4_8 is not None: med9.append(ToFloat(each_med.msle_4_8.doseperdate))
    MEDdata.append({'name':'CQ', 'values':med1})  
    MEDdata.append({'name':'HCQ', 'values':med2})
    MEDdata.append({'name':'Prednisolone', 'values':med3})
    MEDdata.append({'name':'MTX', 'values':med4})
    MEDdata.append({'name':'Azathioprine', 'values':med5})
    MEDdata.append({'name':'Cyclophosphamide', 'values':med6})
    MEDdata.append({'name':'MMF', 'values':med7})
    MEDdata.append({'name':'Cyclosporin A', 'values':med8})
    MEDdata.append({'name':'Tacrolimus', 'values':med9})    
    
    LABdata = []
    lab1 = []
    lab2 = []
    lab3 = []
    lab4 = []
    lab5 = []
    lab6 = []
    lab7 = []
    lab8 = []
    lab9 = []
    lab10 = []
    lab11 = []
    lab12 = []
    lab13 = []
    lab14 = []
    lab15 = []
    lab16 = []
    all_lab = Laboratoryinventoryinvestigation.objects.filter(studynumber = studynum)
    for each_lab in all_lab:
        lab1.append(ToFloat(each_lab.hb))
        lab2.append(ToFloat(each_lab.wbc)) 
        lab3.append(ToFloat(each_lab.n)) 
        lab4.append(ToFloat(each_lab.l)) 
        lab5.append(ToFloat(each_lab.platelets))
        lab6.append(ToFloat(each_lab.esr))
        lab7.append(ToFloat(each_lab.wbc_hpf1)) 
        lab8.append(ToFloat(each_lab.rbc_hpf1))
#        lab10.append(ToFloat(each_lab.anticic))
        lab11.append(ToFloat(each_lab.anti_dsdna))
        lab12.append(ToFloat(each_lab.upci))
        lab13.append(ToFloat(each_lab.cr))
        lab14.append(ToFloat(each_lab.albumin))
        lab15.append(ToFloat(each_lab.c3))
        lab16.append(ToFloat(each_lab.c4))
    LABdata.append({'name':'Hb', 'values':lab1})
    LABdata.append({'name':'WBC', 'values':lab2})
    LABdata.append({'name':'N', 'values':lab3})
    LABdata.append({'name':'L', 'values':lab4})
    LABdata.append({'name':'Platelets', 'values':lab5})
    LABdata.append({'name':'ESR', 'values':lab6})
    LABdata.append({'name':'WBC_HPF', 'values':lab7})
    LABdata.append({'name':'RBC_HPF', 'values':lab8})
#    LABdata.append({'name':'AntiCIC', 'values':lab10})
    LABdata.append({'name':'Anti_dsDNA', 'values':lab11})
    LABdata.append({'name':'UPCI', 'values':lab12})
    LABdata.append({'name':'Cr', 'values':lab13})
    LABdata.append({'name':'Albumin', 'values':lab14})
    LABdata.append({'name':'C3', 'values':lab15})
    LABdata.append({'name':'C4', 'values':lab16})
    
        
    return render(request, 'patient-records.html',{'visit_list': Diseaseactivitysledai.objects.filter(studynumber = studynum).order_by('visitdate'),
    'patient':Studyidentity.objects.get(studynumber = studynum),
    'ACRpatient':Acrcriteria.objects.get(studynumber = studynum),
    'SLICCpatient':Slicccriteria.objects.get(studynumber = studynum),
    'SLEDAIdata':SLEDAIdata,'MEDdata':MEDdata, 'LABdata':LABdata, 'Result':result[0]})

@login_required(login_url='login')
def followupnew(request, studynum):
    visitdate_list = []
    visits = Visiting.objects.filter(studynumber = studynum).order_by('visitdate')
    for vs in visits:
        d = datetime.datetime.strptime(str(vs.visitdate), '%Y-%m-%d')
        visitdate_list.append({'value': str(datetime.datetime.strftime(d, '%Y-%m-%d'))})
    return render(request, 'followup-add.html',{'patient':Studyidentity.objects.get(studynumber = studynum),
                                                'visitdate_list':visitdate_list})

@login_required(login_url='login')
def enrollAdd(request):
    hn_list = []
    hns = HN.objects.exclude(hn__isnull=True).exclude(hn__exact='')
    for hn in hns:
        hn_list.append({'value': str(hn.hn)})
    return render(request, 'enrollment-add.html',{'hn_list':hn_list})

@login_required(login_url='login')
def enrollPatient(request):
    if request.method == "POST":
        now = str(datetime.datetime.now().year+543)
        current_year = now[-2:]+"0000"
        max_id_list = Studyidentity.objects.all().filter(studynumber__gte = current_year)
        max_year = None
        try:
            max_year = int(max_id_list.latest('studynumber').studynumber)
        except ObjectDoesNotExist:
            max_year = current_year
   
        stnum = int(max_year)+1
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
        hn = HN(studynumber = stnum, hn = request.POST.get('HN',))
        hn.save()
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
                mc4_9 = request.POST.get('mc4_9',))
        EnrollMedicalcondition.save()
        
        other01 = CheckboxToBool(request.POST.get('other01',))
        other02 = CheckboxToBool(request.POST.get('other02',))
        other03 = CheckboxToBool(request.POST.get('other03',))
        other04 = CheckboxToBool(request.POST.get('other04',))        
        othertype = request.POST.getlist('othertype[]',)
        otherdetail = request.POST.getlist('otherdetail[]',)
        otherdate = request.POST.getlist('otherdate[]',)
        if other01 is not 'True':
            while 'inflection' in othertype: 
                index = othertype.index('inflection')
                othertype.remove('inflection')
                del otherdetail[index]
                del otherdate[index]
        if other02 is not 'True':
            while 'majorsurgery' in othertype:
                index = othertype.index('majorsurgery')
                othertype.remove('majorsurgery')
                del otherdetail[index]
                del otherdate[index]
        if other03 is not 'True':
            while 'osteoporosis' in othertype:
                index = othertype.index('osteoporosis')
                othertype.remove('osteoporosis')
                del otherdetail[index]
                del otherdate[index]
        if other04 is not 'True':
            while 'malignancy' in othertype:
                index = othertype.index('malignancy')
                othertype.remove('malignancy')
                del otherdetail[index]
                del otherdate[index]
        a = []
        for index in range(0, len(othertype)):
            if(othertype[index] != 'None'):
                EnrollComorbidity = Comorbidity(studynumber = EnrollStudyidentity,
                                        comorbiditytype = othertype[index],
                                        detail = otherdetail[index],
                                        diagnosedate = DateToNone(otherdate[index]))
                EnrollComorbidity.save()

        famlist = []
        famlist.append(request.POST.get('familydisease01',))
        famlist.append(request.POST.get('familydisease02',))
        famlist.append(request.POST.get('familydisease03',))
        famlist.append(request.POST.get('familydisease04',))
        famlist.append(request.POST.get('familydisease05',))
        famlist.append(request.POST.get('familydisease06',))
        famlist.append(request.POST.get('familydisease07',))
        famlist.append(request.POST.get('familydisease08',))
        famlist.append(request.POST.get('familydisease09',))
        famlist.append(request.POST.get('familydisease10',))
        father = request.POST.getlist('father[]',)
        mother = request.POST.getlist('mother[]',)
        son = request.POST.getlist('son[]',)
        daughter = request.POST.getlist('daughter[]',)
        sibling = request.POST.getlist('sibling[]',)
        for eachdisease in famlist:
            if eachdisease is not "0":
                EnrollFam = Familyhistory(studynumber = EnrollStudyidentity,
                    disease = eachdisease,
                    father = iscontains(father,eachdisease),
                    mother = iscontains(mother,eachdisease),
                    sibling = iscontains(sibling,eachdisease),
                    daughter = iscontains(daughter,eachdisease),
                    son = iscontains(son,eachdisease),
                    relative = request.POST.get(''+eachdisease,) if request.POST.get(''+eachdisease,) != '' else None)
                EnrollFam.save()

        renal = request.POST.get('organ1',)
        if renal == "renal":
            start = DateToNone(request.POST.get('startrenal',))
            remis = DateToNone(request.POST.get('remisrenal',))
            EnrollOrgan = Previousorganinvolvement(studynumber = EnrollStudyidentity, 
                    organ = renal, detail = None, startdate = start, remissiondate = remis)
            EnrollOrgan.save()
        
        organlist = []
        organlist.append(request.POST.get('organ2',))
        organlist.append(request.POST.get('organ3',))
        organlist.append(request.POST.get('organ4',))
        organlist.append(request.POST.get('organ5',))
        organlist.append(request.POST.get('organ6',))
        organlist.append(request.POST.get('organ7',))
        organlist.append(request.POST.get('organ8',))
        
        for each_organ in organlist:
            if each_organ is not None:
                for each_detail in request.POST.getlist(str(each_organ)+'[]',):
                    remiss = DateToNone(request.POST.get('remis'+str(each_detail),))
                    start = DateToNone(request.POST.get('start'+str(each_detail),))
                    EnrollOrgan = Previousorganinvolvement(studynumber = EnrollStudyidentity, 
                        organ = each_organ, detail = each_detail, startdate = start, remissiondate = remiss)
                    EnrollOrgan.save()    
        newObgyn = Obgyn(studynumber = EnrollStudyidentity,
                     recorddate = request.POST.get('obgyndate',),
                     gscore = NullToZero(request.POST.get('gscore',)),
                     pscore = NullToZero(request.POST.get('pscore',)),
                     ascore = NullToZero(request.POST.get('ascore',)),
                     menstrualcycle = request.POST.get('menstrualcycle',),
                     pregnant = NullToZero(request.POST.get('pregnant',)),
                     modeofcontraceptives = request.POST.get('modeofcontraceptives',))
        newObgyn.save()
        return patientrecord(request, stnum)

@login_required(login_url='login')
def enrollDetail(request, studynum):
    try: obgyn = Obgyn.objects.filter(studynumber = studynum).latest('recorddate')
    except ObjectDoesNotExist:
        obgyn = None
    return render(request, 'enrollment-detail.html',
                  {'patient':Studyidentity.objects.get(studynumber = studynum),
                   'acrcriteria':Acrcriteria.objects.get(studynumber = studynum),
                   'slicccriteria':Slicccriteria.objects.get(studynumber = studynum),
                    'familyhistory':Familyhistory.objects.filter(studynumber = studynum),
                    'comorbidity':Comorbidity.objects.filter(studynumber = studynum),
                    'medicalcondition':Medicalcondition.objects.get(studynumber = studynum),
                    'previousorganinvolvement':Previousorganinvolvement.objects.filter(studynumber = studynum),
                  'obgyn':obgyn})


@login_required(login_url='login')
def followPatient(request):
    if request.method == "POST":
        TempstudyNumber = request.POST.get('studynum', '')
        if ValidateVisiting(TempstudyNumber, request.POST.get('visitdate', '')) == True :
            if request.POST.get('visitfile',) is not "":
                uploaded_file_name = str(TempstudyNumber)+'_'+str(request.POST.get('visitdate', ''))+'.'+str(request.FILES['visitfile'].content_type.split('/')[1])
                handle_uploaded_file(request.FILES['visitfile'], uploaded_file_name)
                despath = '/uploads/'+uploaded_file_name
            else: despath = None
            
            Followvisiting = Visiting(studynumber = Studyidentity.objects.get(studynumber = TempstudyNumber),
                                visitdate =  request.POST.get('visitdate', ''),
                                bp = request.POST.get('bp', ''),
                                height = ToFloatNone(request.POST.get('height', '')),
                                weight = ToFloatNone(request.POST.get('weight', '')),
                                username = AuthUser.objects.get(username = request.user),
                                nextvisit = DateToNone(request.POST.get('nextvisitdate', '')),
                                visitnote = request.POST.get('addnote',''),
                                visitfile = despath)
            Followvisiting.save()
#            1-2
#            3-11
#            12-15
#            16-20
#            21-23
#            24-27
#            cpcheck007 28-29
#            
            cp_6 = None
            if CheckboxToBool(request.POST.get('ckcp_6', '')) is 'True':
                cp_6 = request.POST.get('cp_6', '')
            Followclinic = Clinicalpresentation(visitingid = Followvisiting,
                                studynumber = Studyidentity.objects.get(studynumber = TempstudyNumber),
                                visitdate =  request.POST.get('visitdate', ''),
                                cp_1 = None if CheckboxToBool(request.POST.get('cpcheck001',)) is 'True' else CheckboxToBool(request.POST.get('cp_1', '')),
                                cp_2 = None if CheckboxToBool(request.POST.get('cpcheck001',)) is 'True' else CheckboxToBool(request.POST.get('cp_2', '')),
                                cp_3 = None if CheckboxToBool(request.POST.get('cpcheck002',)) is 'True' else CheckboxToBool(request.POST.get('cp_3', '')),
                                cp_4 = None if CheckboxToBool(request.POST.get('cpcheck002',)) is 'True' else CheckboxToBool(request.POST.get('cp_4', '')),
                                cp_5 = None if CheckboxToBool(request.POST.get('cpcheck002',)) is 'True' else CheckboxToBool(request.POST.get('cp_5', '')),
                                cp_6 = None if CheckboxToBool(request.POST.get('cpcheck002',)) is 'True' else cp_6,
                                cp_7 = None if CheckboxToBool(request.POST.get('cpcheck002',)) is 'True' else CheckboxToBool(request.POST.get('cp_7', '')),
                                cp_8 = None if CheckboxToBool(request.POST.get('cpcheck002',)) is 'True' else CheckboxToBool(request.POST.get('cp_8', '')),
                                cp_9 = None if CheckboxToBool(request.POST.get('cpcheck002',)) is 'True' else CheckboxToBool(request.POST.get('cp_9', '')),
                                cp_10 = None if CheckboxToBool(request.POST.get('cpcheck002',)) is 'True' else CheckboxToBool(request.POST.get('cp_10', '')),
                                cp_11 = None if CheckboxToBool(request.POST.get('cpcheck002',)) is 'True' else CheckboxToBool(request.POST.get('cp_11', '')),
                                cp_12 = None if CheckboxToBool(request.POST.get('cpcheck003',)) is 'True' else CheckboxToBool(request.POST.get('cp_12', '')),
                                cp_13 = None if CheckboxToBool(request.POST.get('cpcheck003',)) is 'True' else CheckboxToBool(request.POST.get('cp_13', '')),
                                cp_14 = None if CheckboxToBool(request.POST.get('cpcheck003',)) is 'True' else CheckboxToBool(request.POST.get('cp_14', '')),
                                cp_15 = None if CheckboxToBool(request.POST.get('cpcheck003',)) is 'True' else CheckboxToBool(request.POST.get('cp_15', '')),
                                cp_16 = None if CheckboxToBool(request.POST.get('cpcheck004',)) is 'True' else CheckboxToBool(request.POST.get('cp_16', '')),
                                cp_17 = None if CheckboxToBool(request.POST.get('cpcheck004',)) is 'True' else CheckboxToBool(request.POST.get('cp_17', '')),
                                cp_18 = None if CheckboxToBool(request.POST.get('cpcheck004',)) is 'True' else CheckboxToBool(request.POST.get('cp_18', '')),
                                cp_19 = None if CheckboxToBool(request.POST.get('cpcheck004',)) is 'True' else CheckboxToBool(request.POST.get('cp_19', '')),
                                cp_20 = None if CheckboxToBool(request.POST.get('cpcheck004',)) is 'True' else CheckboxToBool(request.POST.get('cp_20', '')),
                                cp_21 = None if CheckboxToBool(request.POST.get('cpcheck005',)) is 'True' else CheckboxToBool(request.POST.get('cp_21', '')),
                                cp_22 = None if CheckboxToBool(request.POST.get('cpcheck005',)) is 'True' else CheckboxToBool(request.POST.get('cp_22', '')),
                                cp_23 = None if CheckboxToBool(request.POST.get('cpcheck005',)) is 'True' else CheckboxToBool(request.POST.get('cp_23', '')),
                                cp_24 = None if CheckboxToBool(request.POST.get('cpcheck006',)) is 'True' else CheckboxToBool(request.POST.get('cp_24', '')),
                                cp_25 = None if CheckboxToBool(request.POST.get('cpcheck006',)) is 'True' else CheckboxToBool(request.POST.get('cp_25', '')),
                                cp_26 = None if CheckboxToBool(request.POST.get('cpcheck006',)) is 'True' else CheckboxToBool(request.POST.get('cp_26', '')),
                                cp_27 = None if CheckboxToBool(request.POST.get('cpcheck006',)) is 'True' else CheckboxToBool(request.POST.get('cp_27', '')),
                                cp_28 = None if CheckboxToBool(request.POST.get('cpcheck007',)) is 'True' else CheckboxToBool(request.POST.get('cp_28', '')),
                                cp_29 = None if CheckboxToBool(request.POST.get('cpcheck007',)) is 'True' else CheckboxToBool(request.POST.get('cp_29', '')))
            Followclinic.save()

            Totaldamage = CheckboxToInt(request.POST.get('di_1', '')) + CheckboxToInt(request.POST.get('di_2', '')) + CheckboxToInt(request.POST.get('di_3', '')) + CheckboxToInt(request.POST.get('di_4', '')) + CheckboxToInt(request.POST.get('di_6', '')) + CheckboxToInt(request.POST.get('di_7', '')) + CheckboxToInt(request.POST.get('di_8', '')) + CheckboxToInt(request.POST.get('di_9', '')) + CheckboxToInt(request.POST.get('di_10', '')) + CheckboxToInt(request.POST.get('di_11', '')) + CheckboxToInt(request.POST.get('di_13', '')) + CheckboxToInt(request.POST.get('di_14', '')) + CheckboxToInt(request.POST.get('di_15', '')) + CheckboxToInt(request.POST.get('di_16', '')) + CheckboxToInt(request.POST.get('di_17', '')) + CheckboxToInt(request.POST.get('di_19', '')) + CheckboxToInt(request.POST.get('di_20', '')) + CheckboxToInt(request.POST.get('di_21', '')) + CheckboxToInt(request.POST.get('di_22', '')) + CheckboxToInt(request.POST.get('di_23', '')) + CheckboxToInt(request.POST.get('di_24', '')) + CheckboxToInt(request.POST.get('di_26', '')) + CheckboxToInt(request.POST.get('di_27', '')) + CheckboxToInt(request.POST.get('di_28', '')) + CheckboxToInt(request.POST.get('di_29', '')) + CheckboxToInt(request.POST.get('di_30', '')) + CheckboxToInt(request.POST.get('di_31', '')) + CheckboxToInt(request.POST.get('di_32', '')) + CheckboxToInt(request.POST.get('di_34', '')) + CheckboxToInt(request.POST.get('di_35', '')) + CheckboxToInt(request.POST.get('di_36', '')) + CheckboxToInt(request.POST.get('di_37', '')) + CheckboxToInt(request.POST.get('di_38', '')) + CheckboxToInt(request.POST.get('di_39', '')) + CheckboxToInt(request.POST.get('di_40', ''))

#            slicccheck001
            
            Followdamage = Damageindex(visitingid = Followvisiting,
                            studynumber = Studyidentity.objects.get(studynumber = TempstudyNumber),
                            visitdate =  request.POST.get('visitdate', ''),
                            di_1 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_1', '')),
                            di_2 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_2', '')),
                            di_3 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_3', '')),
                            di_4 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_4', '')),
                            di_5 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToInt(request.POST.get('di_5', '')),
                            di_6 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_6', '')),
                            di_7 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_7', '')),
                            di_8 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_8', '')),
                            di_9 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_9', '')),
                            di_10 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_10', '')),
                            di_11 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_11', '')),
                            di_12 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToInt(request.POST.get('di_12', '')),
                            di_13 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_13', '')),
                            di_14 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_14', '')),
                            di_15 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_15', '')),
                            di_16 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_16', '')),
                            di_17 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_17', '')),
                            di_18 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToInt(request.POST.get('di_18', '')),
                            di_19 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_19', '')),
                            di_20 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_20', '')),
                            di_21 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_21', '')),
                            di_22 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_22', '')),
                            di_23 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_23', '')),
                            di_24 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_24', '')),
                            di_25 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToInt(request.POST.get('di_25', '')),
                            di_26 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_26', '')),
                            di_27 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_27', '')),
                            di_28 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_28', '')),
                            di_29 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_29', '')),
                            di_30 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_30', '')),
                            di_31 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_31', '')),
                            di_32 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_32', '')),
                            di_33 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToInt(request.POST.get('di_33', '')),
                            di_34 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_34', '')),
                            di_35 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_35', '')),
                            di_36 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_36', '')),
                            di_37 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_37', '')),
                            di_38 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_38', '')),
                            di_39 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_39', '')),
                            di_40 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_40', '')),
                            di_41 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToInt(request.POST.get('di_41', '')),
                            di_total = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else Totaldamage)
            Followdamage.save()

            totalSLEDAI = (CheckboxToInt(request.POST.get('seizure', '')) + CheckboxToInt(request.POST.get('psychosis', '')) + CheckboxToInt(request.POST.get('organicbrainsyndrome', '')) + CheckboxToInt(request.POST.get('visualdisturbance', '')) + CheckboxToInt(request.POST.get('cranialnerve', '')) + CheckboxToInt(request.POST.get('lupusheadache', '')) + CheckboxToInt(request.POST.get('cva', '')) + CheckboxToInt(request.POST.get('vasculitis', '')))*8 + (CheckboxToInt(request.POST.get('arthritis', '')) + CheckboxToInt(request.POST.get('myositis', '')) + CheckboxToInt(request.POST.get('casts', '')) + CheckboxToInt(request.POST.get('hematuria', '')) + CheckboxToInt(request.POST.get('proteinuria', '')) + CheckboxToInt(request.POST.get('pyuria', '')))*4 + (CheckboxToInt(request.POST.get('lowcomplement', '')) + CheckboxToInt(request.POST.get('increaseddnabinding', '')) + CheckboxToInt(request.POST.get('rash', '')) + CheckboxToInt(request.POST.get('alopecia', '')) + CheckboxToInt(request.POST.get('mucousmembrane', '')) + CheckboxToInt(request.POST.get('pleurisy', '')) + CheckboxToInt(request.POST.get('pericarditis', '')))*2 + CheckboxToInt(request.POST.get('thrombocytopenia', '')) + CheckboxToInt(request.POST.get('leukopenia', '')) + CheckboxToInt(request.POST.get('fever', '')) 

#            sledaicheck001 physiciansglobalassessment
#            sledaicheck002 status
#            sledaicheck003 all
            
            FollowSLEDAI = Diseaseactivitysledai(visitingid = Followvisiting,
                        studynumber = Studyidentity.objects.get(studynumber = TempstudyNumber),
                        visitdate =  request.POST.get('visitdate', ''),
                        physiciansglobalassessment = None if CheckboxToBool(request.POST.get('sledaicheck001',)) is 'True' else request.POST.get('physiciansglobalassessment', ''),
                        seizure = None if CheckboxToBool(request.POST.get('sledaicheck003',)) is 'True' else CheckboxToBool(request.POST.get('seizure', '')),
                        psychosis = None if CheckboxToBool(request.POST.get('sledaicheck003',)) is 'True' else CheckboxToBool(request.POST.get('psychosis', '')),
                        organicbrainsyndrome = None if CheckboxToBool(request.POST.get('sledaicheck003',)) is 'True' else CheckboxToBool(request.POST.get('organicbrainsyndrome', '')),
                        visualdisturbance = None if CheckboxToBool(request.POST.get('sledaicheck003',)) is 'True' else CheckboxToBool(request.POST.get('visualdisturbance', '')),
                        cranialnerve = None if CheckboxToBool(request.POST.get('sledaicheck003',)) is 'True' else CheckboxToBool(request.POST.get('cranialnerve', '')),
                        cranialnervedetail = None if CheckboxToBool(request.POST.get('sledaicheck003',)) is 'True' else request.POST.get('cranialnervedetail', ''),
                        lupusheadache = None if CheckboxToBool(request.POST.get('sledaicheck003',)) is 'True' else CheckboxToBool(request.POST.get('lupusheadache', '')),
                        cva = None if CheckboxToBool(request.POST.get('sledaicheck003',)) is 'True' else CheckboxToBool(request.POST.get('cva', '')),
                        vasculitis = None if CheckboxToBool(request.POST.get('sledaicheck003',)) is 'True' else CheckboxToBool(request.POST.get('vasculitis', '')),
                        arthritis = None if CheckboxToBool(request.POST.get('sledaicheck003',)) is 'True' else CheckboxToBool(request.POST.get('arthritis', '')),
                        arthritisjointamount = None if CheckboxToBool(request.POST.get('sledaicheck003',)) is 'True' else CheckboxToInt(request.POST.get('arthritisjointamount', '')),
                        myositis = None if CheckboxToBool(request.POST.get('sledaicheck003',)) is 'True' else CheckboxToBool(request.POST.get('myositis', '')),
                        casts = None if CheckboxToBool(request.POST.get('sledaicheck003',)) is 'True' else CheckboxToBool(request.POST.get('casts', '')),
                        hematuria = None if CheckboxToBool(request.POST.get('sledaicheck003',)) is 'True' else CheckboxToBool(request.POST.get('hematuria', '')),
                        proteinuria = None if CheckboxToBool(request.POST.get('sledaicheck003',)) is 'True' else CheckboxToBool(request.POST.get('proteinuria', '')),
                        pyuria = None if CheckboxToBool(request.POST.get('sledaicheck003',)) is 'True' else CheckboxToBool(request.POST.get('pyuria', '')),
                        lowcomplement = None if CheckboxToBool(request.POST.get('sledaicheck003',)) is 'True' else CheckboxToBool(request.POST.get('lowcomplement', '')),
                        increaseddnabinding = CheckboxToBool(request.POST.get('increaseddnabinding', '')),
                        rash = None if CheckboxToBool(request.POST.get('sledaicheck003',)) is 'True' else CheckboxToBool(request.POST.get('rash', '')),
                        alopecia = None if CheckboxToBool(request.POST.get('sledaicheck003',)) is 'True' else CheckboxToBool(request.POST.get('alopecia', '')),
                        mucousmembrane = None if CheckboxToBool(request.POST.get('sledaicheck003',)) is 'True' else CheckboxToBool(request.POST.get('mucousmembrane', '')),
                        pleurisy = None if CheckboxToBool(request.POST.get('sledaicheck003',)) is 'True' else CheckboxToBool(request.POST.get('pleurisy', '')),
                        pericarditis = None if CheckboxToBool(request.POST.get('sledaicheck003',)) is 'True' else CheckboxToBool(request.POST.get('pericarditis', '')),
                        thrombocytopenia = None if CheckboxToBool(request.POST.get('sledaicheck003',)) is 'True' else CheckboxToBool(request.POST.get('thrombocytopenia', '')),
                        leukopenia = None if CheckboxToBool(request.POST.get('sledaicheck003',)) is 'True' else CheckboxToBool(request.POST.get('leukopenia', '')),
                        fever = None if CheckboxToBool(request.POST.get('sledaicheck003',)) is 'True' else CheckboxToBool(request.POST.get('fever', '')),
                        sledai_total = None if CheckboxToBool(request.POST.get('sledaicheck003',)) is 'True' else totalSLEDAI, 
                        status = None if CheckboxToBool(request.POST.get('sledaicheck002',)) is 'True' else request.POST.get('patientstatus', ''))
            FollowSLEDAI.save()
            
            FollowLn = None
            if CheckboxToBool(request.POST.get('labcheck11', '')) is 'True':
                if CheckboxToBool(request.POST.get('labcheck011', '')) is 'False':
                    FollowLn = Lnlab(renalbiopsyclass = request.POST.get('renalbiopsyclass', ''),
                    renalbiopsydate = DateToNone(request.POST.get('renalbiopsydate', '')),
                    activityindex = ToFloat(request.POST.get('activityindex', '')),
                    chronicityindex = ToFloat(request.POST.get('chronicityindex', '')),
                    ln_1 = ToFloat(request.POST.get('ln_1', '')),
                    ln_2 = ToFloat(request.POST.get('ln_2', '')),
                    ln_3 = request.POST.get('ln_3', ''),
                    ln_4 = request.POST.get('ln_4', ''),
                    ln_5 = ToFloat(request.POST.get('ln_5', '')),
                    renalbiopsystatus = request.POST.get('RenalShow', ''))
                    FollowLn.save()  
                    
                
            labcheck07 = CheckboxToBool(request.POST.get('labcheck07', ''))
            labcheck08 = CheckboxToBool(request.POST.get('labcheck08', ''))
            labcheck09 = CheckboxToBool(request.POST.get('labcheck09', ''))
            labcheck10 = CheckboxToBool(request.POST.get('labcheck10', ''))
            stoolparasite = None
            cxr=None
            ekg=None
            echo=None
            if labcheck07 is 'True':
                if request.POST.get('stoolparasite',) != 'Abnormal':
                    stoolparasite = Labtype(status = request.POST.get('stoolparasite',), date = None, detail = None)
                else: 
                    stoolparasite = Labtype(status = request.POST.get('stoolparasite', ''), 
                                date = DateToNone(request.POST.get('stoolparasite2', '')),
                                detail = request.POST.get('stoolparasite1', ''))
            if labcheck08 is 'True':
                if request.POST.get('cxr',) != 'Abnormal':
                    cxr = Labtype(status = request.POST.get('cxr',), date = None, detail = None)
                else: 
                    cxr = Labtype(status = request.POST.get('cxr', ''), 
                                date = DateToNone(request.POST.get('cxr2', '')),                                 
                                detail = request.POST.get('cxr1', ''))
            if labcheck09 is 'True':
                if request.POST.get('ekg',) != 'Abnormal':
                    ekg = Labtype(status = request.POST.get('ekg',), date = None, detail = None)
                else:
                    ekg = Labtype(status = request.POST.get('ekg', ''), 
                                date = DateToNone(request.POST.get('ekg2', '')),
                                detail = request.POST.get('ekg1', ''))
            if labcheck10 is 'True':
                if request.POST.get('echo',) != 'Abnormal':
                    echo = Labtype(status = request.POST.get('echo',), date = None, detail = None)
                else:
                    echo = Labtype(status = request.POST.get('echo', ''), 
                                date = DateToNone(request.POST.get('echo2', '')),
                                detail = request.POST.get('echo1', ''))
            
            Followlab = Laboratoryinventoryinvestigation(visitingid = Followvisiting,
                            studynumber = Studyidentity.objects.get(studynumber = TempstudyNumber),
                            lnlabid = FollowLn,
                            visitdate =  request.POST.get('visitdate', ''),
                            hb = None if CheckboxToBool(request.POST.get('labcheck001',)) is 'True' else ToFloatNone(request.POST.get('hb', '')),
                            wbc = None if CheckboxToBool(request.POST.get('labcheck001',)) is 'True' else ToFloatNone(request.POST.get('wbc', '')),
                            n = None if CheckboxToBool(request.POST.get('labcheck001',)) is 'True' else ToFloatNone(request.POST.get('n', '')),
                            l = None if CheckboxToBool(request.POST.get('labcheck001',)) is 'True' else ToFloatNone(request.POST.get('l', '')),
                            platelets = None if CheckboxToBool(request.POST.get('labcheck001',)) is 'True' else ToFloatNone(request.POST.get('platelets', '')),
                            esr = None if CheckboxToBool(request.POST.get('labcheck001',)) is 'True' else ToFloatNone(request.POST.get('esr', '')),
                            wbc_hpf1 = None if CheckboxToBool(request.POST.get('labcheck002',)) is 'True' else ToFloatNone(request.POST.get('wbc_hpf1', '')),
                            rbc_hpf1 = None if CheckboxToBool(request.POST.get('labcheck002',)) is 'True' else ToFloatNone(request.POST.get('rbc_hpf1', '')),
                            wbccasts1 = None if CheckboxToBool(request.POST.get('labcheck002',)) is 'True' else ToFloatNone(request.POST.get('wbccasts1', '')),
                            rbccasts1 = None if CheckboxToBool(request.POST.get('labcheck002',)) is 'True' else ToFloatNone(request.POST.get('rbccasts1', '')),
                            granularcasts1 = None if CheckboxToBool(request.POST.get('labcheck002',)) is 'True' else ToFloatNone(request.POST.get('granularcasts1', '')),
                            wbc_hpf2 = None if CheckboxToBool(request.POST.get('labcheck002',)) is 'True' else ToFloatNone(request.POST.get('wbc_hpf2', '')),
                            rbc_hpf2 = None if CheckboxToBool(request.POST.get('labcheck002',)) is 'True' else ToFloatNone(request.POST.get('rbc_hpf2', '')),
                            wbccasts2 = None if CheckboxToBool(request.POST.get('labcheck002',)) is 'True' else ToFloatNone(request.POST.get('wbccasts2', '')),
                            rbccasts2 = None if CheckboxToBool(request.POST.get('labcheck002',)) is 'True' else ToFloatNone(request.POST.get('rbccasts2', '')),
                            granularcasts2 = None if CheckboxToBool(request.POST.get('labcheck002',)) is 'True' else ToFloatNone(request.POST.get('granularcasts2', '')),
                            glucose = None if CheckboxToBool(request.POST.get('labcheck002',)) is 'True' else StringToNone(request.POST.get('ckglucose', ''),request.POST.get('glucose', '')),
                            protein = None if CheckboxToBool(request.POST.get('labcheck002',)) is 'True' else StringToNone(request.POST.get('ckprotein', ''),request.POST.get('protein', '')),
                            tp_spoturineprotein = None if CheckboxToBool(request.POST.get('labcheck002',)) is 'True' else ToFloatNone(request.POST.get('tp_spoturineprotein', '')),
                            cre_spoturinecreatinine = None if CheckboxToBool(request.POST.get('labcheck002',)) is 'True' else ToFloatNone(request.POST.get('cre_spoturinecreatinine', '')),
                            tfhr_urineprotein = None if CheckboxToBool(request.POST.get('labcheck002',)) is 'True' else ToFloatNone(request.POST.get('tfhr_urineprotein', '')),
                            tfhr_urinecreatinine = None if CheckboxToBool(request.POST.get('labcheck002',)) is 'True' else ToFloatNone(request.POST.get('tfhr_urinecreatinine', '')),
                            upci = None if CheckboxToBool(request.POST.get('labcheck002',)) is 'True' else ToFloatNone(request.POST.get('upci', '')),
                            fbs = None if CheckboxToBool(request.POST.get('labcheck003',)) is 'True' else ToFloatNone(request.POST.get('fbs', '')),
                            hba1c = None if CheckboxToBool(request.POST.get('labcheck003',)) is 'True' else ToFloatNone(request.POST.get('hba1c', '')),
                            bun = None if CheckboxToBool(request.POST.get('labcheck003',)) is 'True' else ToFloatNone(request.POST.get('bun', '')),
                            cr =None if CheckboxToBool(request.POST.get('labcheck003',)) is 'True' else ToFloatNone(request.POST.get('cr', '')),
                            alp = None if CheckboxToBool(request.POST.get('labcheck003',)) is 'True' else ToFloatNone(request.POST.get('alp', '')),
                            ast = None if CheckboxToBool(request.POST.get('labcheck003',)) is 'True' else ToFloatNone(request.POST.get('ast', '')),
                            alt =None if CheckboxToBool(request.POST.get('labcheck003',)) is 'True' else ToFloatNone(request.POST.get('alt', '')),
                            ggt = None if CheckboxToBool(request.POST.get('labcheck003',)) is 'True' else ToFloatNone(request.POST.get('ggt', '')),
                            ldh = None if CheckboxToBool(request.POST.get('labcheck003',)) is 'True' else ToFloatNone(request.POST.get('ldh', '')),
                            albumin = None if CheckboxToBool(request.POST.get('labcheck003',)) is 'True' else ToFloatNone(request.POST.get('albumin', '')),
                            tdbilirubin = None if CheckboxToBool(request.POST.get('labcheck003',)) is 'True' else [ToFloatNone(request.POST.get('tdbilirubin1','')),ToFloatNone(request.POST.get('tdbilirubin2', ''))],
                            crp = None if CheckboxToBool(request.POST.get('labcheck003',)) is 'True' else ToFloatNone(request.POST.get('crp', '')),
                            choles = None if CheckboxToBool(request.POST.get('labcheck003',)) is 'True' else ToFloatNone(request.POST.get('choles', '')),
                            tg = None if CheckboxToBool(request.POST.get('labcheck003',)) is 'True' else ToFloatNone(request.POST.get('tg', '')),
                            ldl = None if CheckboxToBool(request.POST.get('labcheck003',)) is 'True' else ToFloatNone(request.POST.get('ldl', '')),
                            hdl = None if CheckboxToBool(request.POST.get('labcheck003',)) is 'True' else ToFloatNone(request.POST.get('hdl', '')),
                            inr = None if CheckboxToBool(request.POST.get('labcheck003',)) is 'True' else ToFloatNone(request.POST.get('inr', '')),
                            anti_dsdna = None if CheckboxToBool(request.POST.get('labcheck004',)) is 'True' else ToFloatNone(request.POST.get('anti_dsdna', '')),
                            antism = None if CheckboxToBool(request.POST.get('labcheck004',)) is 'True' else StringToNone(request.POST.get('ckantism', ''),request.POST.get('antism', '')),
                            antirnp = None if CheckboxToBool(request.POST.get('labcheck004',)) is 'True' else StringToNone(request.POST.get('ckantirnp', ''),request.POST.get('antirnp', '')),
                            antiro = None if CheckboxToBool(request.POST.get('labcheck004',)) is 'True' else StringToNone(request.POST.get('ckantiro', ''),request.POST.get('antiro', '')),
                            antila = None if CheckboxToBool(request.POST.get('labcheck004',)) is 'True' else StringToNone(request.POST.get('ckantila', ''),request.POST.get('antila', '')),
                            aca = None if CheckboxToBool(request.POST.get('labcheck004',)) is 'True' else ToFloatNone(request.POST.get('aca', '')),
                            lupusanticoagulant = None if CheckboxToBool(request.POST.get('labcheck004',)) is 'True' else StringToNone(request.POST.get('cklupusanticoagulant', ''),request.POST.get('lupusanticoagulant', '')),
                            b2gpi = None if CheckboxToBool(request.POST.get('labcheck004',)) is 'True' else ToFloatNone(request.POST.get('b2gpi', '')),
                            c3 = None if CheckboxToBool(request.POST.get('labcheck004',)) is 'True' else ToFloatNone(request.POST.get('c3', '')),
                            c4 = None if CheckboxToBool(request.POST.get('labcheck004',)) is 'True' else ToFloatNone(request.POST.get('c4', '')),
                            ch50 = None if CheckboxToBool(request.POST.get('labcheck004',)) is 'True' else ToFloatNone(request.POST.get('ch50', '')),
                            hbsag = None if CheckboxToBool(request.POST.get('labcheck005',)) is 'True' else StringToNone(request.POST.get('ckhbsag', ''),request.POST.get('hbsag', '')),
                            antihbs = None if CheckboxToBool(request.POST.get('labcheck005',)) is 'True' else StringToNone(request.POST.get('ckantihbs', ''),request.POST.get('antihbs', '')),
                            antihbc = None if CheckboxToBool(request.POST.get('labcheck005',)) is 'True' else StringToNone(request.POST.get('ckantihbc', ''),request.POST.get('antihbc', '')),
                            antihcv = None if CheckboxToBool(request.POST.get('labcheck005',)) is 'True' else StringToNone(request.POST.get('ckantihcv', ''),request.POST.get('antihcv', '')),
                            antihiv = None if CheckboxToBool(request.POST.get('labcheck005',)) is 'True' else StringToNone(request.POST.get('ckantihiv', ''),request.POST.get('antihiv', '')),
                            anticic = None if CheckboxToBool(request.POST.get('labcheck004',)) is 'True' else ToFloatNone(request.POST.get('anticic', '')),
                            il6 = None if CheckboxToBool(request.POST.get('labcheck004',)) is 'True' else ToFloatNone(request.POST.get('il6', '')),
                            mpa = None if CheckboxToBool(request.POST.get('labcheck005extra',)) is 'True' else ToFloatNone(request.POST.get('mpa', '')),
                            fk507 = None if CheckboxToBool(request.POST.get('labcheck005extra',)) is 'True' else ToFloatNone(request.POST.get('fk507', '')),
                            cyclosporin = None if CheckboxToBool(request.POST.get('labcheck005extra',)) is 'True' else ToFloatNone(request.POST.get('cyclosporin', '')),
                            cytokine = None if CheckboxToBool(request.POST.get('labcheck005extra',)) is 'True' else StringToNone(request.POST.get('ckcytokine', ''),request.POST.get('cytokine', '')),
                            l1l4spine_bmd = None if CheckboxToBool(request.POST.get('labcheck006',)) is 'True' else ToFloatNone(request.POST.get('l1l4spine_bmd','')),
                            l1l4spine_tscore = None if CheckboxToBool(request.POST.get('labcheck006',)) is 'True' else ToFloatNone(request.POST.get('l1l4spine_tscore','')),
                            l1l4spine_date = None if CheckboxToBool(request.POST.get('labcheck006',)) is 'True' else DateToNone(request.POST.get('l1l4spine_date','')),
                            hip_bmd = None if CheckboxToBool(request.POST.get('labcheck006',)) is 'True' else ToFloatNone(request.POST.get('hip_bmd','')),
                            hip_tscore = None if CheckboxToBool(request.POST.get('labcheck006',)) is 'True' else ToFloatNone(request.POST.get('hip_tscore','')),
                            hip_date = None if CheckboxToBool(request.POST.get('labcheck006',)) is 'True' else DateToNone(request.POST.get('hip_date','')),
                            radius_bmd = None if CheckboxToBool(request.POST.get('labcheck006',)) is 'True' else ToFloatNone(request.POST.get('radius_bmd','')),
                            radius_tscore = None if CheckboxToBool(request.POST.get('labcheck006',)) is 'True' else ToFloatNone(request.POST.get('radius_tscore','')),
                            radius_date = None if CheckboxToBool(request.POST.get('labcheck006',)) is 'True' else DateToNone(request.POST.get('radius_date','')),
                            stoolparasite = None if CheckboxToBool(request.POST.get('labcheck007',)) is 'True' else stoolparasite,
                            cxr = None if CheckboxToBool(request.POST.get('labcheck008',)) is 'True' else cxr,
                            ekg = None if CheckboxToBool(request.POST.get('labcheck009',)) is 'True' else ekg,
                            echo = None if CheckboxToBool(request.POST.get('labcheck010',)) is 'True' else echo)
            Followlab.save()

            FollowMed = Medication(visitingid = Followvisiting,
                            studynumber = Studyidentity.objects.get(studynumber = TempstudyNumber),
                            visitdate =  request.POST.get('visitdate',),
                            msle_1_1 = None if CheckboxToBool(request.POST.get('ckmedi001',)) is 'True' else Medicationtype(generic = request.POST.get('gen1',), doseperdate = ToFloatMed(request.POST.get('dose1',)), startdate = DateToNone(request.POST.get('start1',)), stopdate = DateToNone(request.POST.get('end1',))),
                            msle_1_2 = None if CheckboxToBool(request.POST.get('ckmedi001',)) is 'True' else Medicationtype(generic = request.POST.get('gen2',), doseperdate = ToFloatMed(request.POST.get('dose2',)), startdate = DateToNone(request.POST.get('start2',)), stopdate = DateToNone(request.POST.get('end2',))),
                            msle_1_3 = None if CheckboxToBool(request.POST.get('ckmedi001',)) is 'True' else Medicationtype(generic = request.POST.get('gen3',), doseperdate = ToFloatMed(request.POST.get('dose3',)), startdate = DateToNone(request.POST.get('start3',)), stopdate = DateToNone(request.POST.get('end3',))),
                            msle_2_1 = None if CheckboxToBool(request.POST.get('ckmedi001',)) is 'True' else Medicationtype(generic = request.POST.get('gen4',), doseperdate = ToFloatMed(request.POST.get('dose4',)), startdate = DateToNone(request.POST.get('start4',)), stopdate = DateToNone(request.POST.get('end4',))),
                            msle_2_2 = None if CheckboxToBool(request.POST.get('ckmedi001',)) is 'True' else Medicationtype(generic = request.POST.get('gen5',), doseperdate = ToFloatMed(request.POST.get('dose5',)), startdate = DateToNone(request.POST.get('start5',)), stopdate = DateToNone(request.POST.get('end5',))),
                            msle_3_1 = None if CheckboxToBool(request.POST.get('ckmedi001',)) is 'True' else Medicationtype(generic = request.POST.get('gen6',), doseperdate = ToFloatMed(request.POST.get('dose6',)), startdate = DateToNone(request.POST.get('start6',)), stopdate = DateToNone(request.POST.get('end6',))),
                            msle_3_2 = None if CheckboxToBool(request.POST.get('ckmedi001',)) is 'True' else Medicationtype(generic = request.POST.get('gen7',), doseperdate = ToFloatMed(request.POST.get('dose7',)), startdate = DateToNone(request.POST.get('start7',)), stopdate = DateToNone(request.POST.get('end7',))),
                            msle_3_3 = None if CheckboxToBool(request.POST.get('ckmedi001',)) is 'True' else Medicationtype(generic = request.POST.get('gen8',), doseperdate = ToFloatMed(request.POST.get('dose8',)), startdate = DateToNone(request.POST.get('start8',)), stopdate = DateToNone(request.POST.get('end8',))),
                            msle_3_4 = None if CheckboxToBool(request.POST.get('ckmedi001',)) is 'True' else Medicationtype(generic = request.POST.get('gen9',), doseperdate = ToFloatMed(request.POST.get('dose9',)), startdate = DateToNone(request.POST.get('start9',)), stopdate = DateToNone(request.POST.get('end9',))),
                            msle_4_1 = None if CheckboxToBool(request.POST.get('ckmedi001',)) is 'True' else Medicationtype(generic = request.POST.get('gen10',), doseperdate = ToFloatMed(request.POST.get('dose10',)), startdate = DateToNone(request.POST.get('start10',)), stopdate = DateToNone(request.POST.get('end10',))),
                            msle_4_2 = None if CheckboxToBool(request.POST.get('ckmedi001',)) is 'True' else Medicationtype(generic = request.POST.get('gen11',), doseperdate = ToFloatMed(request.POST.get('dose11',)), startdate = DateToNone(request.POST.get('start11',)), stopdate = DateToNone(request.POST.get('end11',))),
                            msle_4_3 = None if CheckboxToBool(request.POST.get('ckmedi001',)) is 'True' else Medicationtype(generic = request.POST.get('gen12',), doseperdate = ToFloatMed(request.POST.get('dose12',)), startdate = DateToNone(request.POST.get('start12',)), stopdate = DateToNone(request.POST.get('end12',))),
                            msle_4_4 = None if CheckboxToBool(request.POST.get('ckmedi001',)) is 'True' else Medicationtype(generic = request.POST.get('gen13',), doseperdate = ToFloatMed(request.POST.get('dose13',)), startdate = DateToNone(request.POST.get('start13',)), stopdate = DateToNone(request.POST.get('end13',))),
                            msle_4_5 = None if CheckboxToBool(request.POST.get('ckmedi001',)) is 'True' else Medicationtype(generic = request.POST.get('gen14',), doseperdate = ToFloatMed(request.POST.get('dose14',)), startdate = DateToNone(request.POST.get('start14',)), stopdate = DateToNone(request.POST.get('end14',))),
                            msle_4_6 = None if CheckboxToBool(request.POST.get('ckmedi001',)) is 'True' else Medicationtype(generic = request.POST.get('gen15',), doseperdate = ToFloatMed(request.POST.get('dose15',)), startdate = DateToNone(request.POST.get('start15',)), stopdate = DateToNone(request.POST.get('end15',))),
                            msle_4_7 = None if CheckboxToBool(request.POST.get('ckmedi001',)) is 'True' else Medicationtype(generic = request.POST.get('gen16',), doseperdate = ToFloatMed(request.POST.get('dose16',)), startdate = DateToNone(request.POST.get('start16',)), stopdate = DateToNone(request.POST.get('end16',))),
                            msle_4_8 = None if CheckboxToBool(request.POST.get('ckmedi001',)) is 'True' else Medicationtype(generic = request.POST.get('gen17',), doseperdate = ToFloatMed(request.POST.get('dose17',)), startdate = DateToNone(request.POST.get('start17',)), stopdate = DateToNone(request.POST.get('end17',))),
                            msle_4_9 = None if CheckboxToBool(request.POST.get('ckmedi001',)) is 'True' else Medicationtype(generic = request.POST.get('gen18',), doseperdate = ToFloatMed(request.POST.get('dose18',)), startdate = DateToNone(request.POST.get('start18',)), stopdate = DateToNone(request.POST.get('end18',))),
                            msle_4_10 = None if CheckboxToBool(request.POST.get('ckmedi001',)) is 'True' else Medicationtype(generic = request.POST.get('gen19',), doseperdate = ToFloatMed(request.POST.get('dose19',)), startdate = DateToNone(request.POST.get('start19',)), stopdate = DateToNone(request.POST.get('end19',))),
                            msle_4_11 = None if CheckboxToBool(request.POST.get('ckmedi001',)) is 'True' else Medicationtype(generic = request.POST.get('gen20',), doseperdate = ToFloatMed(request.POST.get('dose20',)), startdate = DateToNone(request.POST.get('start20',)), stopdate = DateToNone(request.POST.get('end20',))),
                            mgt_1_1 = None if CheckboxToBool(request.POST.get('ckmedi002',)) is 'True' else Medicationtype(generic = request.POST.get('gen21',), doseperdate = ToFloatMed(request.POST.get('dose21',)), startdate = DateToNone(request.POST.get('start21',)), stopdate = DateToNone(request.POST.get('end21',))),
                            mgt_1_2 = None if CheckboxToBool(request.POST.get('ckmedi002',)) is 'True' else Medicationtype(generic = request.POST.get('gen22',), doseperdate = ToFloatMed(request.POST.get('dose22',)), startdate = DateToNone(request.POST.get('start22',)), stopdate = DateToNone(request.POST.get('end22',))),
                            mgt_1_3 = None if CheckboxToBool(request.POST.get('ckmedi002',)) is 'True' else Medicationtype(generic = request.POST.get('gen23',), doseperdate = ToFloatMed(request.POST.get('dose23',)), startdate = DateToNone(request.POST.get('start23',)), stopdate = DateToNone(request.POST.get('end23',))),
                            mgt_1_4 = None if CheckboxToBool(request.POST.get('ckmedi002',)) is 'True' else Medicationtype(generic = request.POST.get('gen24',), doseperdate = ToFloatMed(request.POST.get('dose24',)), startdate = DateToNone(request.POST.get('start24',)), stopdate = DateToNone(request.POST.get('end24',))),
                            mgt_1_5 = None if CheckboxToBool(request.POST.get('ckmedi002',)) is 'True' else Medicationtype(generic = request.POST.get('gen25',), doseperdate = ToFloatMed(request.POST.get('dose25',)), startdate = DateToNone(request.POST.get('start25',)), stopdate = DateToNone(request.POST.get('end25',))),
                            mgt_2_1 = None if CheckboxToBool(request.POST.get('ckmedi002',)) is 'True' else Medicationtype(generic = request.POST.get('gen26',), doseperdate = ToFloatMed(request.POST.get('dose26',)), startdate = DateToNone(request.POST.get('start26',)), stopdate = DateToNone(request.POST.get('end26',))),
                            mgt_2_2 = None if CheckboxToBool(request.POST.get('ckmedi002',)) is 'True' else Medicationtype(generic = request.POST.get('gen27',), doseperdate = ToFloatMed(request.POST.get('dose27',)), startdate = DateToNone(request.POST.get('start27',)), stopdate = DateToNone(request.POST.get('end27',))),
                            mgt_2_3 = None if CheckboxToBool(request.POST.get('ckmedi002',)) is 'True' else Medicationtype(generic = request.POST.get('gen28',), doseperdate = ToFloatMed(request.POST.get('dose28',)), startdate = DateToNone(request.POST.get('start28',)), stopdate = DateToNone(request.POST.get('end28',))),
                            mgt_2_4 = None if CheckboxToBool(request.POST.get('ckmedi002',)) is 'True' else Medicationtype(generic = request.POST.get('gen29',), doseperdate = ToFloatMed(request.POST.get('dose29',)), startdate = DateToNone(request.POST.get('start29',)), stopdate = DateToNone(request.POST.get('end29',))),
                            mgt_3_1 = None if CheckboxToBool(request.POST.get('ckmedi002',)) is 'True' else Medicationtype(generic = request.POST.get('gen30',), doseperdate = ToFloatMed(request.POST.get('dose30',)), startdate = DateToNone(request.POST.get('start30',)), stopdate = DateToNone(request.POST.get('end30',))),
                            mgt_3_2 = None if CheckboxToBool(request.POST.get('ckmedi002',)) is 'True' else Medicationtype(generic = request.POST.get('gen31',), doseperdate = ToFloatMed(request.POST.get('dose31',)), startdate = DateToNone(request.POST.get('start31',)), stopdate = DateToNone(request.POST.get('end31',))),
                            mgt_3_3 = None if CheckboxToBool(request.POST.get('ckmedi002',)) is 'True' else Medicationtype(generic = request.POST.get('gen32',), doseperdate = ToFloatMed(request.POST.get('dose32',)), startdate = DateToNone(request.POST.get('start32',)), stopdate = DateToNone(request.POST.get('end32',))),
                            mgt_4_1 = None if CheckboxToBool(request.POST.get('ckmedi002',)) is 'True' else Medicationtype(generic = request.POST.get('gen33',), doseperdate = ToFloatMed(request.POST.get('dose33',)), startdate = DateToNone(request.POST.get('start33',)), stopdate = DateToNone(request.POST.get('end33',))),
                            mgt_4_2 = None if CheckboxToBool(request.POST.get('ckmedi002',)) is 'True' else Medicationtype(generic = request.POST.get('gen34',), doseperdate = ToFloatMed(request.POST.get('dose34',)), startdate = DateToNone(request.POST.get('start34',)), stopdate = DateToNone(request.POST.get('end34',))),
                            mgt_4_3 = None if CheckboxToBool(request.POST.get('ckmedi002',)) is 'True' else Medicationtype(generic = request.POST.get('gen35',), doseperdate = ToFloatMed(request.POST.get('dose35',)), startdate = DateToNone(request.POST.get('start35',)), stopdate = DateToNone(request.POST.get('end35',))),
                            mgt_4_4 = None if CheckboxToBool(request.POST.get('ckmedi002',)) is 'True' else Medicationtype(generic = request.POST.get('gen36',), doseperdate = ToFloatMed(request.POST.get('dose36',)), startdate = DateToNone(request.POST.get('start36',)), stopdate = DateToNone(request.POST.get('end36',))),
                            mgt_other = CheckboxToBool(request.POST.get('ckmgt_other',)))
            FollowMed.save()
            mgt_other = CheckboxToBool(request.POST.get('ckmgt_other',))
            othermed = request.POST.getlist('mgt_other_detail[]',)
            othermed_doseperdate = request.POST.getlist('otherdose[]',) 
            if mgt_other is 'True':
                for index in range(0, len(othermed)):
                    if(othermed[index] != ''):
                        FollowOtherMed = Othermedication(visitingid = Followvisiting,
                                        medicationname = othermed[index],
                                        doseperdate = othermed_doseperdate[index])
                        FollowOtherMed.save()
                    
            return patientrecord(request, TempstudyNumber)    
        else:
#            return index(request)
            return patientrecord(request, TempstudyNumber)

        
def handle_uploaded_file(file, filename):
    path = os.path.join(settings.UPLOAD_ROOT)
    if not os.path.exists(path):
        os.mkdir(path)
        os.remove(path + filename)
    with open(path + filename, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
            
@login_required(login_url='login')
def followDetail(request, visitid):
    studynum = int(Visiting.objects.get(visitingid = visitid).studynumber.studynumber)
    try: lab = Laboratoryinventoryinvestigation.objects.get(visitingid = visitid)
    except ObjectDoesNotExist: lab = None
    except IndexError: lab = None
    if haslnlab(lab) is True:
        lnlab = Lnlab.objects.get(lnlabid = lab.lnlabid.lnlabid) 
    else: 
        lnlab = None
    this_date = Visiting.objects.get(visitingid = visitid).visitdate

    try: med = Medication.objects.get(visitingid = visitid)
    except ObjectDoesNotExist: med = None
    except IndexError: med = None
    try: PreviousVisit = Visiting.objects.filter(studynumber = studynum).order_by('visitdate').filter(visitdate__lt = this_date).reverse()[0]
    except ObjectDoesNotExist: PreviousVisit = None
    except IndexError: PreviousVisit = None
    try: PreviousLab = Laboratoryinventoryinvestigation.objects.get(visitingid = PreviousVisit)
    except ObjectDoesNotExist: PreviousLab = None
    except IndexError: PreviousLab = None
    try: PreviousMed = Medication.objects.get(visitingid = PreviousVisit)
    except ObjectDoesNotExist: PreviousMed = None
    except IndexError: PreviousMed = None
    try: PreviousDM = Damageindex.objects.get(visitingid = PreviousVisit).di_total
    except ObjectDoesNotExist: PreviousDM = None
    except IndexError: PreviousDM = None
    try: PreviousSLEDAI = Diseaseactivitysledai.objects.get(visitingid = PreviousVisit).sledai_total
    except ObjectDoesNotExist: PreviousSLEDAI = None
    except IndexError: PreviousSLEDAI = None
    try: othermed = Othermedication.objects.filter(visitingid = visitid)
    except ObjectDoesNotExist: othermed = None
    except IndexError: othermed = None
        
    return render(request, 'followup-detail.html',
                      {'visiting':Visiting.objects.get(visitingid = visitid),
                      'med':med,
                      'othermed':othermed,
                      'lab':lab,
                      'lnlab':lnlab,
                      'sledai':Diseaseactivitysledai.objects.get(visitingid = visitid),
                      'damageindex':Damageindex.objects.get(visitingid = visitid),
                      'clinicalpresentation':Clinicalpresentation.objects.get(visitingid = visitid),
                      'PreviousLab':PreviousLab,
                      'PreviousMed':PreviousMed,
                      'PreviousDM':PreviousDM,
                      'PreviousSLEDAI':PreviousSLEDAI})


@login_required(login_url='login')
def followEditPost(request):
    if request.method == "POST":
        temp_visitid = request.POST.get('visitid',)
        old_visiting = Visiting.objects.get(visitingid = temp_visitid)
        old_visiting.visitdate =  request.POST.get('visitdate',)
        old_visiting.bp = request.POST.get('bp',)
        old_visiting.height = ToFloat(request.POST.get('height',))
        old_visiting.weight = ToFloat(request.POST.get('weight',))
        old_visiting.nextvisit = DateToNone(request.POST.get('nextvisitdate', ''))
        old_visiting.visitnote = request.POST.get('addnote','')
        
        if request.POST.get('visitfile',) is not "":
            uploaded_file_name = str(old_visiting.studynumber.studynumber)+'_'+str(old_visiting.visitdate)+'.'+str(request.FILES['visitfile'].content_type.split('/')[1])
            handle_uploaded_file(request.FILES['visitfile'], uploaded_file_name)
            despath = '/uploads/'+uploaded_file_name
        else: despath = None
        
        old_visiting.visitfile = despath
        old_visiting.save()   
        
        cp_6 = None
        if CheckboxToBool(request.POST.get('ckcp_6', '')) is 'True':
            cp_6 = request.POST.get('cp_6', '')
        
        old_clinic = Clinicalpresentation.objects.get(visitingid = temp_visitid)
        old_clinic.visitdate =  request.POST.get('visitdate', '')
        old_clinic.cp_1 = None if CheckboxToBool(request.POST.get('cpcheck001',)) is 'True' else CheckboxToBool(request.POST.get('cp_1', ''))
        old_clinic.cp_2 = None if CheckboxToBool(request.POST.get('cpcheck001',)) is 'True' else CheckboxToBool(request.POST.get('cp_2', ''))
        old_clinic.cp_3 = None if CheckboxToBool(request.POST.get('cpcheck002',)) is 'True' else CheckboxToBool(request.POST.get('cp_3', ''))
        old_clinic.cp_4 = None if CheckboxToBool(request.POST.get('cpcheck002',)) is 'True' else CheckboxToBool(request.POST.get('cp_4', ''))
        old_clinic.cp_5 = None if CheckboxToBool(request.POST.get('cpcheck002',)) is 'True' else CheckboxToBool(request.POST.get('cp_5', ''))
        old_clinic.cp_6 = None if CheckboxToBool(request.POST.get('cpcheck002',)) is 'True' else cp_6
        old_clinic.cp_7 = None if CheckboxToBool(request.POST.get('cpcheck002',)) is 'True' else CheckboxToBool(request.POST.get('cp_7', ''))
        old_clinic.cp_8 = None if CheckboxToBool(request.POST.get('cpcheck002',)) is 'True' else CheckboxToBool(request.POST.get('cp_8', ''))
        old_clinic.cp_9 = None if CheckboxToBool(request.POST.get('cpcheck002',)) is 'True' else CheckboxToBool(request.POST.get('cp_9', ''))
        old_clinic.cp_10 = None if CheckboxToBool(request.POST.get('cpcheck002',)) is 'True' else CheckboxToBool(request.POST.get('cp_10', ''))
        old_clinic.cp_11 = None if CheckboxToBool(request.POST.get('cpcheck002',)) is 'True' else CheckboxToBool(request.POST.get('cp_11', ''))
        old_clinic.cp_12 = None if CheckboxToBool(request.POST.get('cpcheck003',)) is 'True' else CheckboxToBool(request.POST.get('cp_12', ''))
        old_clinic.cp_13 = None if CheckboxToBool(request.POST.get('cpcheck003',)) is 'True' else CheckboxToBool(request.POST.get('cp_13', ''))
        old_clinic.cp_14 = None if CheckboxToBool(request.POST.get('cpcheck003',)) is 'True' else CheckboxToBool(request.POST.get('cp_14', ''))
        old_clinic.cp_15 = None if CheckboxToBool(request.POST.get('cpcheck003',)) is 'True' else CheckboxToBool(request.POST.get('cp_15', ''))
        old_clinic.cp_16 = None if CheckboxToBool(request.POST.get('cpcheck004',)) is 'True' else CheckboxToBool(request.POST.get('cp_16', ''))
        old_clinic.cp_17 = None if CheckboxToBool(request.POST.get('cpcheck004',)) is 'True' else CheckboxToBool(request.POST.get('cp_17', ''))
        old_clinic.cp_18 = None if CheckboxToBool(request.POST.get('cpcheck004',)) is 'True' else CheckboxToBool(request.POST.get('cp_18', ''))
        old_clinic.cp_19 = None if CheckboxToBool(request.POST.get('cpcheck004',)) is 'True' else CheckboxToBool(request.POST.get('cp_19', ''))
        old_clinic.cp_20 = None if CheckboxToBool(request.POST.get('cpcheck004',)) is 'True' else CheckboxToBool(request.POST.get('cp_20', ''))
        old_clinic.cp_21 = None if CheckboxToBool(request.POST.get('cpcheck005',)) is 'True' else CheckboxToBool(request.POST.get('cp_21', ''))
        old_clinic.cp_22 = None if CheckboxToBool(request.POST.get('cpcheck005',)) is 'True' else CheckboxToBool(request.POST.get('cp_22', ''))
        old_clinic.cp_23 = None if CheckboxToBool(request.POST.get('cpcheck005',)) is 'True' else CheckboxToBool(request.POST.get('cp_23', ''))
        old_clinic.cp_24 = None if CheckboxToBool(request.POST.get('cpcheck006',)) is 'True' else CheckboxToBool(request.POST.get('cp_24', ''))
        old_clinic.cp_25 = None if CheckboxToBool(request.POST.get('cpcheck006',)) is 'True' else CheckboxToBool(request.POST.get('cp_25', ''))
        old_clinic.cp_26 = None if CheckboxToBool(request.POST.get('cpcheck006',)) is 'True' else CheckboxToBool(request.POST.get('cp_26', ''))
        old_clinic.cp_27 = None if CheckboxToBool(request.POST.get('cpcheck006',)) is 'True' else CheckboxToBool(request.POST.get('cp_27', ''))
        old_clinic.cp_28 = None if CheckboxToBool(request.POST.get('cpcheck007',)) is 'True' else CheckboxToBool(request.POST.get('cp_28', ''))
        old_clinic.cp_29 = None if CheckboxToBool(request.POST.get('cpcheck007',)) is 'True' else CheckboxToBool(request.POST.get('cp_29', ''))
        old_clinic.save()

        Totaldamage = CheckboxToInt(request.POST.get('di_1', '')) + CheckboxToInt(request.POST.get('di_2', '')) + CheckboxToInt(request.POST.get('di_3', '')) + CheckboxToInt(request.POST.get('di_4', '')) + CheckboxToInt(request.POST.get('di_6', '')) + CheckboxToInt(request.POST.get('di_7', '')) + CheckboxToInt(request.POST.get('di_8', '')) + CheckboxToInt(request.POST.get('di_9', '')) + CheckboxToInt(request.POST.get('di_10', '')) + CheckboxToInt(request.POST.get('di_11', '')) + CheckboxToInt(request.POST.get('di_13', '')) + CheckboxToInt(request.POST.get('di_14', '')) + CheckboxToInt(request.POST.get('di_15', '')) + CheckboxToInt(request.POST.get('di_16', '')) + CheckboxToInt(request.POST.get('di_17', '')) + CheckboxToInt(request.POST.get('di_19', '')) + CheckboxToInt(request.POST.get('di_20', '')) + CheckboxToInt(request.POST.get('di_21', '')) + CheckboxToInt(request.POST.get('di_22', '')) + CheckboxToInt(request.POST.get('di_23', '')) + CheckboxToInt(request.POST.get('di_24', '')) + CheckboxToInt(request.POST.get('di_26', '')) + CheckboxToInt(request.POST.get('di_27', '')) + CheckboxToInt(request.POST.get('di_28', '')) + CheckboxToInt(request.POST.get('di_29', '')) + CheckboxToInt(request.POST.get('di_30', '')) + CheckboxToInt(request.POST.get('di_31', '')) + CheckboxToInt(request.POST.get('di_32', '')) + CheckboxToInt(request.POST.get('di_34', '')) + CheckboxToInt(request.POST.get('di_35', '')) + CheckboxToInt(request.POST.get('di_36', '')) + CheckboxToInt(request.POST.get('di_37', '')) + CheckboxToInt(request.POST.get('di_38', '')) + CheckboxToInt(request.POST.get('di_39', '')) + CheckboxToInt(request.POST.get('di_40', ''))

        old_damage = Damageindex.objects.get(visitingid = temp_visitid)
        old_damage.visitdate =  request.POST.get('visitdate', '')
        old_damage.di_1 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_1', ''))
        old_damage.di_2 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_2', ''))
        old_damage.di_3 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_3', ''))
        old_damage.di_4 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_4', ''))
        old_damage.di_5 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else request.POST.get('di_5', '')
        old_damage.di_6 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_6', ''))
        old_damage.di_7 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_7', ''))
        old_damage.di_8 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_8', ''))
        old_damage.di_9 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_9', ''))
        old_damage.di_10 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_10', ''))
        old_damage.di_11 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_11', ''))
        old_damage.di_12 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else request.POST.get('di_12', '')
        old_damage.di_13 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_13', ''))
        old_damage.di_14 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_14', ''))
        old_damage.di_15 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_15', ''))
        old_damage.di_16 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_16', ''))
        old_damage.di_17 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_17', ''))
        old_damage.di_18 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else request.POST.get('di_18', '')
        old_damage.di_19 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_19', ''))
        old_damage.di_20 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_20', ''))
        old_damage.di_21 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_21', ''))
        old_damage.di_22 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_22', ''))
        old_damage.di_23 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_23', ''))
        old_damage.di_24 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_24', ''))
        old_damage.di_25 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else request.POST.get('di_25', '')
        old_damage.di_26 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_26', ''))
        old_damage.di_27 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_27', ''))
        old_damage.di_28 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_28', ''))
        old_damage.di_29 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_29', ''))
        old_damage.di_30 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_30', ''))
        old_damage.di_31 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_31', ''))
        old_damage.di_32 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_32', ''))
        old_damage.di_33 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else request.POST.get('di_33', '')
        old_damage.di_34 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_34', ''))
        old_damage.di_35 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_35', ''))
        old_damage.di_36 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_36', ''))
        old_damage.di_37 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_37', ''))
        old_damage.di_38 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_38', ''))
        old_damage.di_39 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_39', ''))
        old_damage.di_40 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else CheckboxToBool(request.POST.get('di_40', ''))
        old_damage.di_41 = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else request.POST.get('di_41', '')
        old_damage.di_total = None if CheckboxToBool(request.POST.get('slicccheck001',)) is 'True' else Totaldamage
        old_damage.save()

        totalSLEDAI = (CheckboxToInt(request.POST.get('seizure', '')) + CheckboxToInt(request.POST.get('psychosis', '')) + CheckboxToInt(request.POST.get('organicbrainsyndrome', '')) + CheckboxToInt(request.POST.get('visualdisturbance', '')) + CheckboxToInt(request.POST.get('cranialnerve', '')) + CheckboxToInt(request.POST.get('lupusheadache', '')) + CheckboxToInt(request.POST.get('cva', '')) + CheckboxToInt(request.POST.get('vasculitis', '')))*8 + (CheckboxToInt(request.POST.get('arthritis', '')) + CheckboxToInt(request.POST.get('myositis', '')) + CheckboxToInt(request.POST.get('casts', '')) + CheckboxToInt(request.POST.get('hematuria', '')) + CheckboxToInt(request.POST.get('proteinuria', '')) + CheckboxToInt(request.POST.get('pyuria', '')))*4 + (CheckboxToInt(request.POST.get('lowcomplement', '')) + CheckboxToInt(request.POST.get('increaseddnabinding', '')) + CheckboxToInt(request.POST.get('rash', '')) + CheckboxToInt(request.POST.get('alopecia', '')) + CheckboxToInt(request.POST.get('mucousmembrane', '')) + CheckboxToInt(request.POST.get('pleurisy', '')) + CheckboxToInt(request.POST.get('pericarditis', '')))*2 + CheckboxToInt(request.POST.get('thrombocytopenia', '')) + CheckboxToInt(request.POST.get('leukopenia', '')) + CheckboxToInt(request.POST.get('fever', '')) 

        old_sledai = Diseaseactivitysledai.objects.get(visitingid = temp_visitid)
        old_sledai.visitdate =  request.POST.get('visitdate', '')
        old_sledai.physiciansglobalassessment = None if CheckboxToBool(request.POST.get('sledaicheck001',)) is 'True' else request.POST.get('physiciansglobalassessment', '')
        old_sledai.seizure = None if CheckboxToBool(request.POST.get('sledaicheck003',)) is 'True' else CheckboxToBool(request.POST.get('seizure', ''))
        old_sledai.psychosis = None if CheckboxToBool(request.POST.get('sledaicheck003',)) is 'True' else CheckboxToBool(request.POST.get('psychosis', ''))
        old_sledai.organicbrainsyndrome = None if CheckboxToBool(request.POST.get('sledaicheck003',)) is 'True' else CheckboxToBool(request.POST.get('organicbrainsyndrome', ''))
        old_sledai.visualdisturbance = None if CheckboxToBool(request.POST.get('sledaicheck003',)) is 'True' else CheckboxToBool(request.POST.get('visualdisturbance', ''))
        old_sledai.cranialnerve = None if CheckboxToBool(request.POST.get('sledaicheck003',)) is 'True' else CheckboxToBool(request.POST.get('cranialnerve', ''))
        old_sledai.cranialnervedetail = None if CheckboxToBool(request.POST.get('sledaicheck003',)) is 'True' else request.POST.get('cranialnervedetail', '')
        old_sledai.lupusheadache = None if CheckboxToBool(request.POST.get('sledaicheck003',)) is 'True' else CheckboxToBool(request.POST.get('lupusheadache', ''))
        old_sledai.cva = None if CheckboxToBool(request.POST.get('sledaicheck003',)) is 'True' else CheckboxToBool(request.POST.get('cva', ''))
        old_sledai.vasculitis = None if CheckboxToBool(request.POST.get('sledaicheck003',)) is 'True' else CheckboxToBool(request.POST.get('vasculitis', ''))
        old_sledai.arthritis = None if CheckboxToBool(request.POST.get('sledaicheck003',)) is 'True' else CheckboxToBool(request.POST.get('arthritis', ''))
        old_sledai.arthritisjointamount = None if CheckboxToBool(request.POST.get('sledaicheck003',)) is 'True' else CheckboxToInt(request.POST.get('arthritisjointamount', ''))
        old_sledai.myositis = None if CheckboxToBool(request.POST.get('sledaicheck003',)) is 'True' else CheckboxToBool(request.POST.get('myositis', ''))
        old_sledai.casts = None if CheckboxToBool(request.POST.get('sledaicheck003',)) is 'True' else CheckboxToBool(request.POST.get('casts', ''))
        old_sledai.hematuria = None if CheckboxToBool(request.POST.get('sledaicheck003',)) is 'True' else CheckboxToBool(request.POST.get('hematuria', ''))
        old_sledai.proteinuria = None if CheckboxToBool(request.POST.get('sledaicheck003',)) is 'True' else CheckboxToBool(request.POST.get('proteinuria', ''))
        old_sledai.pyuria = None if CheckboxToBool(request.POST.get('sledaicheck003',)) is 'True' else CheckboxToBool(request.POST.get('pyuria', ''))
        old_sledai.lowcomplement = None if CheckboxToBool(request.POST.get('sledaicheck003',)) is 'True' else CheckboxToBool(request.POST.get('lowcomplement', ''))
        old_sledai.increaseddnabinding = None if CheckboxToBool(request.POST.get('sledaicheck003',)) is 'True' else CheckboxToBool(request.POST.get('increaseddnabinding', ''))
        old_sledai.rash = None if CheckboxToBool(request.POST.get('sledaicheck003',)) is 'True' else CheckboxToBool(request.POST.get('rash', ''))
        old_sledai.alopecia = None if CheckboxToBool(request.POST.get('sledaicheck003',)) is 'True' else CheckboxToBool(request.POST.get('alopecia', ''))
        old_sledai.mucousmembrane = None if CheckboxToBool(request.POST.get('sledaicheck003',)) is 'True' else CheckboxToBool(request.POST.get('mucousmembrane', ''))
        old_sledai.pleurisy = None if CheckboxToBool(request.POST.get('sledaicheck003',)) is 'True' else CheckboxToBool(request.POST.get('pleurisy', ''))
        old_sledai.pericarditis = None if CheckboxToBool(request.POST.get('sledaicheck003',)) is 'True' else CheckboxToBool(request.POST.get('pericarditis', ''))
        old_sledai.thrombocytopenia = None if CheckboxToBool(request.POST.get('sledaicheck003',)) is 'True' else CheckboxToBool(request.POST.get('thrombocytopenia', ''))
        old_sledai.leukopenia = None if CheckboxToBool(request.POST.get('sledaicheck003',)) is 'True' else CheckboxToBool(request.POST.get('leukopenia', ''))
        old_sledai.fever = None if CheckboxToBool(request.POST.get('sledaicheck003',)) is 'True' else CheckboxToBool(request.POST.get('fever', ''))
        old_sledai.sledai_total = None if CheckboxToBool(request.POST.get('sledaicheck003',)) is 'True' else totalSLEDAI
        old_sledai.status = None if CheckboxToBool(request.POST.get('sledaicheck002',)) is 'True' else request.POST.get('patientstatus', '')
        old_sledai.save()
        
        old_ln = None
        if CheckboxToBool(request.POST.get('labcheck11', '')) is 'True':
            if Laboratoryinventoryinvestigation.objects.get(visitingid = temp_visitid).lnlabid is not None:
                ln_id = int(Laboratoryinventoryinvestigation.objects.get(visitingid = temp_visitid).lnlabid.lnlabid)
                if CheckboxToBool(request.POST.get('labcheck011', '')) is 'False':
                    
                    old_ln = Lnlab.objects.get(lnlabid = ln_id)
                    old_ln.renalbiopsyclass = request.POST.get('renalbiopsyclass', '')
                    old_ln.renalbiopsydate = DateToNone(request.POST.get('renalbiopsydate', ''))
                    old_ln.activityindex = ToFloat(request.POST.get('activityindex', ''))
                    old_ln.chronicityindex = ToFloat(request.POST.get('chronicityindex', ''))
                    old_ln.ln_1 = ToFloat(request.POST.get('ln_1', ''))
                    old_ln.ln_2 = ToFloat(request.POST.get('ln_2', ''))
                    old_ln.ln_3 = request.POST.get('ln_3', '')
                    old_ln.ln_4 = request.POST.get('ln_4', '')
                    old_ln.ln_5 = ToFloat(request.POST.get('ln_5', ''))
                    old_ln.renalbiopsystatus = request.POST.get('RenalShow', '') 
                    old_ln.save()
                else: Lnlab.objects.get(lnlabid = ln_id).delete()
            else : 
                if CheckboxToBool(request.POST.get('labcheck011', '')) is 'False':
                    old_ln = Lnlab(renalbiopsyclass = request.POST.get('renalbiopsyclass', ''),
                    renalbiopsydate = DateToNone(request.POST.get('renalbiopsydate', '')),
                    activityindex = ToFloat(request.POST.get('activityindex', '')),
                    chronicityindex = ToFloat(request.POST.get('chronicityindex', '')),
                    ln_1 = ToFloat(request.POST.get('ln_1', '')),
                    ln_2 = ToFloat(request.POST.get('ln_2', '')),
                    ln_3 = request.POST.get('ln_3', ''),
                    ln_4 = request.POST.get('ln_4', ''),
                    ln_5 = ToFloat(request.POST.get('ln_5', '')),
                    renalbiopsystatus = request.POST.get('RenalShow', ''))
                    old_ln.save()
                
        labcheck07 = CheckboxToBool(request.POST.get('labcheck07', ''))
        labcheck08 = CheckboxToBool(request.POST.get('labcheck08', ''))
        labcheck09 = CheckboxToBool(request.POST.get('labcheck09', ''))
        labcheck10 = CheckboxToBool(request.POST.get('labcheck10', ''))
        stoolparasite = None
        cxr=None
        ekg=None
        echo=None
        if labcheck07 is 'True':
            if request.POST.get('stoolparasite',) != 'Abnormal':
                stoolparasite = Labtype(status = request.POST.get('stoolparasite',), date = None, detail = None)
            else: 
                stoolparasite = Labtype(status = request.POST.get('stoolparasite', ''), 
                                date = DateToNone(request.POST.get('stoolparasite2', '')),
                                detail = request.POST.get('stoolparasite1', ''))
        if labcheck08 is 'True':
            if request.POST.get('cxr',) != 'Abnormal':
                cxr = Labtype(status = request.POST.get('cxr',), date = None, detail = None)
            else: 
                cxr = Labtype(status = request.POST.get('cxr', ''), 
                                date = DateToNone(request.POST.get('cxr2', '')),                                 
                              detail = request.POST.get('cxr1', ''))
        if labcheck09 is 'True':
            if request.POST.get('ekg',) != 'Abnormal':
                ekg = Labtype(status = request.POST.get('ekg',), date = None, detail = None)
            else:
                ekg = Labtype(status = request.POST.get('ekg', ''), 
                                date = DateToNone(request.POST.get('ekg2', '')),
                                detail = request.POST.get('ekg1', ''))
        if labcheck10 is 'True':
            if request.POST.get('echo',) != 'Abnormal':
                echo = Labtype(status = request.POST.get('echo',), date = None, detail = None)
            else:
                echo = Labtype(status = request.POST.get('echo', ''), 
                                date = DateToNone(request.POST.get('echo2', '')),
                                detail = request.POST.get('echo1', ''))
        try:  
            old_lab = Laboratoryinventoryinvestigation.objects.get(visitingid = temp_visitid)
            old_lab.lnlabid = old_ln
            old_lab.visitdate =  request.POST.get('visitdate', '')
            old_lab.hb = None if CheckboxToBool(request.POST.get('labcheck001',)) is 'True' else ToFloat(request.POST.get('hb', ''))
            old_lab.wbc = None if CheckboxToBool(request.POST.get('labcheck001',)) is 'True' else ToFloat(request.POST.get('wbc', ''))
            old_lab.n = None if CheckboxToBool(request.POST.get('labcheck001',)) is 'True' else ToFloat(request.POST.get('n', ''))
            old_lab.l = None if CheckboxToBool(request.POST.get('labcheck001',)) is 'True' else ToFloat(request.POST.get('l', ''))
            old_lab.platelets = None if CheckboxToBool(request.POST.get('labcheck001',)) is 'True' else ToFloat(request.POST.get('platelets', ''))
            old_lab.esr = None if CheckboxToBool(request.POST.get('labcheck001',)) is 'True' else ToFloat(request.POST.get('esr', ''))
            old_lab.wbc_hpf1 = None if CheckboxToBool(request.POST.get('labcheck002',)) is 'True' else ToFloat(request.POST.get('wbc_hpf1', ''))
            old_lab.rbc_hpf1 = None if CheckboxToBool(request.POST.get('labcheck002',)) is 'True' else ToFloat(request.POST.get('rbc_hpf1', ''))
            old_lab.wbccasts1 = None if CheckboxToBool(request.POST.get('labcheck002',)) is 'True' else ToFloat(request.POST.get('wbccasts1', ''))
            old_lab.rbccasts1 = None if CheckboxToBool(request.POST.get('labcheck002',)) is 'True' else ToFloat(request.POST.get('rbccasts1', ''))
            old_lab.granularcasts1 = None if CheckboxToBool(request.POST.get('labcheck002',)) is 'True' else ToFloat(request.POST.get('granularcasts1', ''))
            old_lab.wbc_hpf2 = None if CheckboxToBool(request.POST.get('labcheck002',)) is 'True' else ToFloat(request.POST.get('wbc_hpf2', ''))
            old_lab.rbc_hpf2 = None if CheckboxToBool(request.POST.get('labcheck002',)) is 'True' else ToFloat(request.POST.get('rbc_hpf2', ''))
            old_lab.wbccasts2 = None if CheckboxToBool(request.POST.get('labcheck002',)) is 'True' else ToFloat(request.POST.get('wbccasts2', ''))
            old_lab.rbccasts2 = None if CheckboxToBool(request.POST.get('labcheck002',)) is 'True' else ToFloat(request.POST.get('rbccasts2', ''))
            old_lab.granularcasts2 = None if CheckboxToBool(request.POST.get('labcheck002',)) is 'True' else ToFloat(request.POST.get('granularcasts2', ''))
            old_lab.glucose = None if CheckboxToBool(request.POST.get('labcheck002',)) is 'True' else StringToNone(request.POST.get('ckglucose', ''),request.POST.get('glucose', ''))
            old_lab.protein = None if CheckboxToBool(request.POST.get('labcheck002',)) is 'True' else StringToNone(request.POST.get('ckprotein', ''),request.POST.get('protein', ''))
            old_lab.tp_spoturineprotein = None if CheckboxToBool(request.POST.get('labcheck002',)) is 'True' else ToFloat(request.POST.get('tp_spoturineprotein', ''))
            old_lab.cre_spoturinecreatinine = None if CheckboxToBool(request.POST.get('labcheck002',)) is 'True' else ToFloat(request.POST.get('cre_spoturinecreatinine', ''))
            old_lab.tfhr_urineprotein = None if CheckboxToBool(request.POST.get('labcheck002',)) is 'True' else ToFloat(request.POST.get('tfhr_urineprotein', ''))
            old_lab.tfhr_urinecreatinine = None if CheckboxToBool(request.POST.get('labcheck002',)) is 'True' else ToFloat(request.POST.get('tfhr_urinecreatinine', ''))
            old_lab.upci = None if CheckboxToBool(request.POST.get('labcheck002',)) is 'True' else ToFloat(request.POST.get('upci', ''))
            old_lab.fbs =  None if CheckboxToBool(request.POST.get('labcheck003',)) is 'True' else ToFloat(request.POST.get('fbs', ''))
            old_lab.hba1c =  None if CheckboxToBool(request.POST.get('labcheck003',)) is 'True' else ToFloat(request.POST.get('hba1c', ''))
            old_lab.bun =  None if CheckboxToBool(request.POST.get('labcheck003',)) is 'True' else ToFloat(request.POST.get('bun', ''))
            old_lab.cr = None if CheckboxToBool(request.POST.get('labcheck003',)) is 'True' else ToFloat(request.POST.get('cr', ''))
            old_lab.alp =  None if CheckboxToBool(request.POST.get('labcheck003',)) is 'True' else ToFloat(request.POST.get('alp', ''))
            old_lab.ast =  None if CheckboxToBool(request.POST.get('labcheck003',)) is 'True' else ToFloat(request.POST.get('ast', ''))
            old_lab.alt = None if CheckboxToBool(request.POST.get('labcheck003',)) is 'True' else ToFloat(request.POST.get('alt', ''))
            old_lab.ggt =  None if CheckboxToBool(request.POST.get('labcheck003',)) is 'True' else ToFloat(request.POST.get('ggt', ''))
            old_lab.ldh =  None if CheckboxToBool(request.POST.get('labcheck003',)) is 'True' else ToFloat(request.POST.get('ldh', ''))
            old_lab.albumin =  None if CheckboxToBool(request.POST.get('labcheck003',)) is 'True' else ToFloat(request.POST.get('albumin', ''))
            old_lab.tdbilirubin =  None if CheckboxToBool(request.POST.get('labcheck003',)) is 'True' else [ToFloat(request.POST.get('tdbilirubin1','')),ToFloat(request.POST.get('tdbilirubin2', ''))]
            old_lab.crp =  None if CheckboxToBool(request.POST.get('labcheck003',)) is 'True' else ToFloat(request.POST.get('crp', ''))
            old_lab.choles =  None if CheckboxToBool(request.POST.get('labcheck003',)) is 'True' else ToFloat(request.POST.get('choles', ''))
            old_lab.tg =  None if CheckboxToBool(request.POST.get('labcheck003',)) is 'True' else ToFloat(request.POST.get('tg', ''))
            old_lab.ldl =  None if CheckboxToBool(request.POST.get('labcheck003',)) is 'True' else ToFloat(request.POST.get('ldl', ''))
            old_lab.hdl =  None if CheckboxToBool(request.POST.get('labcheck003',)) is 'True' else ToFloat(request.POST.get('hdl', ''))
            old_lab.inr =  None if CheckboxToBool(request.POST.get('labcheck003',)) is 'True' else ToFloat(request.POST.get('inr', ''))
            old_lab.anti_dsdna = None if CheckboxToBool(request.POST.get('labcheck004',)) is 'True' else ToFloat(request.POST.get('anti_dsdna', ''))
            old_lab.antism = None if CheckboxToBool(request.POST.get('labcheck004',)) is 'True' else StringToNone(request.POST.get('ckantism', ''),request.POST.get('antism', ''))
            old_lab.antirnp = None if CheckboxToBool(request.POST.get('labcheck004',)) is 'True' else StringToNone(request.POST.get('ckantirnp', ''),request.POST.get('antirnp', ''))
            old_lab.antiro = None if CheckboxToBool(request.POST.get('labcheck004',)) is 'True' else StringToNone(request.POST.get('ckantiro', ''),request.POST.get('antiro', ''))
            old_lab.antila = None if CheckboxToBool(request.POST.get('labcheck004',)) is 'True' else StringToNone(request.POST.get('ckantila', ''),request.POST.get('antila', ''))
            old_lab.aca = None if CheckboxToBool(request.POST.get('labcheck004',)) is 'True' else ToFloat(request.POST.get('aca', ''))
            old_lab.lupusanticoagulant = None if CheckboxToBool(request.POST.get('labcheck004',)) is 'True' else StringToNone(request.POST.get('cklupusanticoagulant', ''),request.POST.get('lupusanticoagulant', ''))
            old_lab.b2gpi = None if CheckboxToBool(request.POST.get('labcheck004',)) is 'True' else ToFloat(request.POST.get('b2gpi', ''))
            old_lab.c3 = None if CheckboxToBool(request.POST.get('labcheck004',)) is 'True' else ToFloat(request.POST.get('c3', ''))
            old_lab.c4 = None if CheckboxToBool(request.POST.get('labcheck004',)) is 'True' else ToFloat(request.POST.get('c4', ''))
            old_lab.ch50 = None if CheckboxToBool(request.POST.get('labcheck004',)) is 'True' else ToFloat(request.POST.get('ch50', ''))
            old_lab.hbsag = None if CheckboxToBool(request.POST.get('labcheck005',)) is 'True' else StringToNone(request.POST.get('ckhbsag', ''),request.POST.get('hbsag', ''))
            old_lab.antihbs = None if CheckboxToBool(request.POST.get('labcheck005',)) is 'True' else StringToNone(request.POST.get('ckantihbs', ''),request.POST.get('antihbs', ''))
            old_lab.antihbc = None if CheckboxToBool(request.POST.get('labcheck005',)) is 'True' else StringToNone(request.POST.get('ckantihbc', ''),request.POST.get('antihbc', ''))
            old_lab.antihcv = None if CheckboxToBool(request.POST.get('labcheck005',)) is 'True' else StringToNone(request.POST.get('ckantihcv', ''),request.POST.get('antihcv', ''))
            old_lab.antihiv = None if CheckboxToBool(request.POST.get('labcheck005',)) is 'True' else StringToNone(request.POST.get('ckantihiv', ''),request.POST.get('antihiv', ''))
            old_lab.anticic = None if CheckboxToBool(request.POST.get('labcheck004',)) is 'True' else ToFloatNone(request.POST.get('anticic', ''))
            old_lab.il6 = None if CheckboxToBool(request.POST.get('labcheck004',)) is 'True' else ToFloatNone(request.POST.get('il6', ''))
            old_lab.mpa = None if CheckboxToBool(request.POST.get('labcheck005extra',)) is 'True' else ToFloat(request.POST.get('mpa', ''))
            old_lab.fk507 = None if CheckboxToBool(request.POST.get('labcheck005extra',)) is 'True' else ToFloat(request.POST.get('fk507', ''))
            old_lab.cyclosporin = None if CheckboxToBool(request.POST.get('labcheck005extra',)) is 'True' else ToFloat(request.POST.get('cyclosporin', ''))
            old_lab.cytokine = None if CheckboxToBool(request.POST.get('labcheck005extra',)) is 'True' else StringToNone(request.POST.get('ckcytokine', ''),request.POST.get('cytokine', ''))
            old_lab.l1l4spine_bmd = None if CheckboxToBool(request.POST.get('labcheck006',)) is 'True' else ToFloatNone(request.POST.get('l1l4spine_bmd',''))
            old_lab.l1l4spine_tscore = None if CheckboxToBool(request.POST.get('labcheck006',)) is 'True' else ToFloatNone(request.POST.get('l1l4spine_tscore',''))
            old_lab.l1l4spine_date = None if CheckboxToBool(request.POST.get('labcheck006',)) is 'True' else DateToNone(request.POST.get('l1l4spine_date',''))
            old_lab.hip_bmd = None if CheckboxToBool(request.POST.get('labcheck006',)) is 'True' else ToFloatNone(request.POST.get('hip_bmd',''))
            old_lab.hip_tscore = None if CheckboxToBool(request.POST.get('labcheck006',)) is 'True' else ToFloatNone(request.POST.get('hip_tscore',''))
            old_lab.hip_date = None if CheckboxToBool(request.POST.get('labcheck006',)) is 'True' else DateToNone(request.POST.get('hip_date',''))
            old_lab.radius_bmd = None if CheckboxToBool(request.POST.get('labcheck006',)) is 'True' else ToFloatNone(request.POST.get('radius_bmd',''))
            old_lab.radius_tscore = None if CheckboxToBool(request.POST.get('labcheck006',)) is 'True' else ToFloatNone(request.POST.get('radius_tscore',''))
            old_lab.radius_date = None if CheckboxToBool(request.POST.get('labcheck006',)) is 'True' else DateToNone(request.POST.get('radius_date',''))
            old_lab.stoolparasite = None if CheckboxToBool(request.POST.get('labcheck007',)) is 'True' else stoolparasite
            old_lab.cxr = None if CheckboxToBool(request.POST.get('labcheck008',)) is 'True' else cxr
            old_lab.ekg = None if CheckboxToBool(request.POST.get('labcheck009',)) is 'True' else ekg
            old_lab.echo = None if CheckboxToBool(request.POST.get('labcheck010',)) is 'True' else echo
            old_lab.save()
        except ObjectDoesNotExist:
            Followlab = Laboratoryinventoryinvestigation(visitingid = old_visiting, studynumber = old_visiting.studynumber, lnlabid = old_ln, visitdate =  request.POST.get('visitdate', ''),
            hb = None if CheckboxToBool(request.POST.get('labcheck001',)) is 'True' else ToFloatNone(request.POST.get('hb', '')),
            wbc = None if CheckboxToBool(request.POST.get('labcheck001',)) is 'True' else ToFloatNone(request.POST.get('wbc', '')),
            n = None if CheckboxToBool(request.POST.get('labcheck001',)) is 'True' else ToFloatNone(request.POST.get('n', '')),
            l = None if CheckboxToBool(request.POST.get('labcheck001',)) is 'True' else ToFloatNone(request.POST.get('l', '')),
            platelets = None if CheckboxToBool(request.POST.get('labcheck001',)) is 'True' else ToFloatNone(request.POST.get('platelets', '')),
            esr = None if CheckboxToBool(request.POST.get('labcheck001',)) is 'True' else ToFloatNone(request.POST.get('esr', '')),
            wbc_hpf1 = None if CheckboxToBool(request.POST.get('labcheck002',)) is 'True' else ToFloatNone(request.POST.get('wbc_hpf1', '')),
            rbc_hpf1 = None if CheckboxToBool(request.POST.get('labcheck002',)) is 'True' else ToFloatNone(request.POST.get('rbc_hpf1', '')),
            wbccasts1 = None if CheckboxToBool(request.POST.get('labcheck002',)) is 'True' else ToFloatNone(request.POST.get('wbccasts1', '')),
            rbccasts1 = None if CheckboxToBool(request.POST.get('labcheck002',)) is 'True' else ToFloatNone(request.POST.get('rbccasts1', '')),
            granularcasts1 = None if CheckboxToBool(request.POST.get('labcheck002',)) is 'True' else ToFloatNone(request.POST.get('granularcasts1', '')),
            wbc_hpf2 = None if CheckboxToBool(request.POST.get('labcheck002',)) is 'True' else ToFloatNone(request.POST.get('wbc_hpf2', '')),
            rbc_hpf2 = None if CheckboxToBool(request.POST.get('labcheck002',)) is 'True' else ToFloatNone(request.POST.get('rbc_hpf2', '')),
            wbccasts2 = None if CheckboxToBool(request.POST.get('labcheck002',)) is 'True' else ToFloatNone(request.POST.get('wbccasts2', '')),
            rbccasts2 = None if CheckboxToBool(request.POST.get('labcheck002',)) is 'True' else ToFloatNone(request.POST.get('rbccasts2', '')),
            granularcasts2 = None if CheckboxToBool(request.POST.get('labcheck002',)) is 'True' else ToFloatNone(request.POST.get('granularcasts2', '')),
            glucose = None if CheckboxToBool(request.POST.get('labcheck002',)) is 'True' else StringToNone(request.POST.get('ckglucose', ''),request.POST.get('glucose', '')),
            protein = None if CheckboxToBool(request.POST.get('labcheck002',)) is 'True' else StringToNone(request.POST.get('ckprotein', ''),request.POST.get('protein', '')),
            tp_spoturineprotein = None if CheckboxToBool(request.POST.get('labcheck002',)) is 'True' else ToFloatNone(request.POST.get('tp_spoturineprotein', '')),
            cre_spoturinecreatinine = None if CheckboxToBool(request.POST.get('labcheck002',)) is 'True' else ToFloatNone(request.POST.get('cre_spoturinecreatinine', '')),
            tfhr_urineprotein = None if CheckboxToBool(request.POST.get('labcheck002',)) is 'True' else ToFloatNone(request.POST.get('tfhr_urineprotein', '')),
            tfhr_urinecreatinine = None if CheckboxToBool(request.POST.get('labcheck002',)) is 'True' else ToFloatNone(request.POST.get('tfhr_urinecreatinine', '')),
            upci = None if CheckboxToBool(request.POST.get('labcheck002',)) is 'True' else ToFloatNone(request.POST.get('upci', '')),
            fbs = None if CheckboxToBool(request.POST.get('labcheck003',)) is 'True' else ToFloatNone(request.POST.get('fbs', '')),
            hba1c = None if CheckboxToBool(request.POST.get('labcheck003',)) is 'True' else ToFloatNone(request.POST.get('hba1c', '')),
            bun = None if CheckboxToBool(request.POST.get('labcheck003',)) is 'True' else ToFloatNone(request.POST.get('bun', '')),
            cr =None if CheckboxToBool(request.POST.get('labcheck003',)) is 'True' else ToFloatNone(request.POST.get('cr', '')),
            alp = None if CheckboxToBool(request.POST.get('labcheck003',)) is 'True' else ToFloatNone(request.POST.get('alp', '')),
            ast = None if CheckboxToBool(request.POST.get('labcheck003',)) is 'True' else ToFloatNone(request.POST.get('ast', '')),
            alt =None if CheckboxToBool(request.POST.get('labcheck003',)) is 'True' else ToFloatNone(request.POST.get('alt', '')),
            ggt = None if CheckboxToBool(request.POST.get('labcheck003',)) is 'True' else ToFloatNone(request.POST.get('ggt', '')),
            ldh = None if CheckboxToBool(request.POST.get('labcheck003',)) is 'True' else ToFloatNone(request.POST.get('ldh', '')),
            albumin = None if CheckboxToBool(request.POST.get('labcheck003',)) is 'True' else ToFloatNone(request.POST.get('albumin', '')),
            tdbilirubin = None if CheckboxToBool(request.POST.get('labcheck003',)) is 'True' else [ToFloatNone(request.POST.get('tdbilirubin1','')),ToFloatNone(request.POST.get('tdbilirubin2', ''))],
            crp = None if CheckboxToBool(request.POST.get('labcheck003',)) is 'True' else ToFloatNone(request.POST.get('crp', '')),
            choles = None if CheckboxToBool(request.POST.get('labcheck003',)) is 'True' else ToFloatNone(request.POST.get('choles', '')),
            tg = None if CheckboxToBool(request.POST.get('labcheck003',)) is 'True' else ToFloatNone(request.POST.get('tg', '')),
            ldl = None if CheckboxToBool(request.POST.get('labcheck003',)) is 'True' else ToFloatNone(request.POST.get('ldl', '')),
            hdl = None if CheckboxToBool(request.POST.get('labcheck003',)) is 'True' else ToFloatNone(request.POST.get('hdl', '')),
            inr = None if CheckboxToBool(request.POST.get('labcheck003',)) is 'True' else ToFloatNone(request.POST.get('inr', '')),
            anti_dsdna = None if CheckboxToBool(request.POST.get('labcheck004',)) is 'True' else ToFloatNone(request.POST.get('anti_dsdna', '')),
            antism = None if CheckboxToBool(request.POST.get('labcheck004',)) is 'True' else StringToNone(request.POST.get('ckantism', ''),request.POST.get('antism', '')),
            antirnp = None if CheckboxToBool(request.POST.get('labcheck004',)) is 'True' else StringToNone(request.POST.get('ckantirnp', ''),request.POST.get('antirnp', '')),
            antiro = None if CheckboxToBool(request.POST.get('labcheck004',)) is 'True' else StringToNone(request.POST.get('ckantiro', ''),request.POST.get('antiro', '')),
            antila = None if CheckboxToBool(request.POST.get('labcheck004',)) is 'True' else StringToNone(request.POST.get('ckantila', ''),request.POST.get('antila', '')),
            aca = None if CheckboxToBool(request.POST.get('labcheck004',)) is 'True' else ToFloatNone(request.POST.get('aca', '')),
            lupusanticoagulant = None if CheckboxToBool(request.POST.get('labcheck004',)) is 'True' else StringToNone(request.POST.get('cklupusanticoagulant', ''),request.POST.get('lupusanticoagulant', '')),
            b2gpi = None if CheckboxToBool(request.POST.get('labcheck004',)) is 'True' else ToFloatNone(request.POST.get('b2gpi', '')),
            c3 = None if CheckboxToBool(request.POST.get('labcheck004',)) is 'True' else ToFloatNone(request.POST.get('c3', '')),
            c4 = None if CheckboxToBool(request.POST.get('labcheck004',)) is 'True' else ToFloatNone(request.POST.get('c4', '')),
            ch50 = None if CheckboxToBool(request.POST.get('labcheck004',)) is 'True' else ToFloatNone(request.POST.get('ch50', '')),
            hbsag = None if CheckboxToBool(request.POST.get('labcheck005',)) is 'True' else StringToNone(request.POST.get('ckhbsag', ''),request.POST.get('hbsag', '')),
            antihbs = None if CheckboxToBool(request.POST.get('labcheck005',)) is 'True' else StringToNone(request.POST.get('ckantihbs', ''),request.POST.get('antihbs', '')),
            antihbc = None if CheckboxToBool(request.POST.get('labcheck005',)) is 'True' else StringToNone(request.POST.get('ckantihbc', ''),request.POST.get('antihbc', '')),
            antihcv = None if CheckboxToBool(request.POST.get('labcheck005',)) is 'True' else StringToNone(request.POST.get('ckantihcv', ''),request.POST.get('antihcv', '')),
            antihiv = None if CheckboxToBool(request.POST.get('labcheck005',)) is 'True' else StringToNone(request.POST.get('ckantihiv', ''),request.POST.get('antihiv', '')),
            anticic = None if CheckboxToBool(request.POST.get('labcheck004',)) is 'True' else ToFloatNone(request.POST.get('anticic', '')),
            il6 = None if CheckboxToBool(request.POST.get('labcheck004',)) is 'True' else ToFloatNone(request.POST.get('il6', '')),
            mpa = None if CheckboxToBool(request.POST.get('labcheck005extra',)) is 'True' else ToFloatNone(request.POST.get('mpa', '')),
            fk507 = None if CheckboxToBool(request.POST.get('labcheck005extra',)) is 'True' else ToFloatNone(request.POST.get('fk507', '')),
            cyclosporin = None if CheckboxToBool(request.POST.get('labcheck005extra',)) is 'True' else ToFloatNone(request.POST.get('cyclosporin', '')),
            cytokine = None if CheckboxToBool(request.POST.get('labcheck005extra',)) is 'True' else StringToNone(request.POST.get('ckcytokine', ''),request.POST.get('cytokine', '')),
            l1l4spine_bmd = None if CheckboxToBool(request.POST.get('labcheck006',)) is 'True' else ToFloatNone(request.POST.get('l1l4spine_bmd','')),
            l1l4spine_tscore = None if CheckboxToBool(request.POST.get('labcheck006',)) is 'True' else ToFloatNone(request.POST.get('l1l4spine_tscore','')),
            l1l4spine_date = None if CheckboxToBool(request.POST.get('labcheck006',)) is 'True' else DateToNone(request.POST.get('l1l4spine_date','')),
            hip_bmd = None if CheckboxToBool(request.POST.get('labcheck006',)) is 'True' else ToFloatNone(request.POST.get('hip_bmd','')),
            hip_tscore = None if CheckboxToBool(request.POST.get('labcheck006',)) is 'True' else ToFloatNone(request.POST.get('hip_tscore','')),
            hip_date = None if CheckboxToBool(request.POST.get('labcheck006',)) is 'True' else DateToNone(request.POST.get('hip_date','')),
            radius_bmd = None if CheckboxToBool(request.POST.get('labcheck006',)) is 'True' else ToFloatNone(request.POST.get('radius_bmd','')),
            radius_tscore = None if CheckboxToBool(request.POST.get('labcheck006',)) is 'True' else ToFloatNone(request.POST.get('radius_tscore','')),
            radius_date = None if CheckboxToBool(request.POST.get('labcheck006',)) is 'True' else DateToNone(request.POST.get('radius_date','')),
            stoolparasite = None if CheckboxToBool(request.POST.get('labcheck007',)) is 'True' else stoolparasite,
            cxr = None if CheckboxToBool(request.POST.get('labcheck008',)) is 'True' else cxr,
            ekg = None if CheckboxToBool(request.POST.get('labcheck009',)) is 'True' else ekg,
            echo = None if CheckboxToBool(request.POST.get('labcheck010',)) is 'True' else echo)
            Followlab.save()
            
        old_med = Medication.objects.get(visitingid = temp_visitid)
        old_med.visitdate =  request.POST.get('visitdate',)
        old_med.msle_1_1 = None if CheckboxToBool(request.POST.get('ckmedi001',)) is 'True' else Medicationtype(generic = request.POST.get('gen1',), doseperdate = ToFloatMed(request.POST.get('dose1',)), startdate = DateToNone(request.POST.get('start1',)), stopdate = DateToNone(request.POST.get('end1',)))
        old_med.msle_1_2 = None if CheckboxToBool(request.POST.get('ckmedi001',)) is 'True' else Medicationtype(generic = request.POST.get('gen2',), doseperdate = ToFloatMed(request.POST.get('dose2',)), startdate = DateToNone(request.POST.get('start2',)), stopdate = DateToNone(request.POST.get('end2',)))
        old_med.msle_1_3 = None if CheckboxToBool(request.POST.get('ckmedi001',)) is 'True' else Medicationtype(generic = request.POST.get('gen3',), doseperdate = ToFloatMed(request.POST.get('dose3',)), startdate = DateToNone(request.POST.get('start3',)), stopdate = DateToNone(request.POST.get('end3',)))
        if request.POST.get('ckmed2',) == 'cq':
            old_med.msle_2_1 = None if CheckboxToBool(request.POST.get('ckmedi001',)) is 'True' else Medicationtype(generic = request.POST.get('gen4',), doseperdate = ToFloatMed(request.POST.get('dose4',)), startdate = DateToNone(request.POST.get('start4',)), stopdate = DateToNone(request.POST.get('end4',)))
            old_med.msle_2_2 = None if CheckboxToBool(request.POST.get('ckmedi001',)) is 'True' else Medicationtype(generic = None, doseperdate = None, startdate = None, stopdate = None)
        else:
            old_med.msle_2_1 = None if CheckboxToBool(request.POST.get('ckmedi001',)) is 'True' else Medicationtype(generic = None, doseperdate = None, startdate = None, stopdate = None)
            old_med.msle_2_2 = None if CheckboxToBool(request.POST.get('ckmedi001',)) is 'True' else Medicationtype(generic = request.POST.get('gen5',), doseperdate = ToFloatMed(request.POST.get('dose5',)), startdate = DateToNone(request.POST.get('start5',)), stopdate = DateToNone(request.POST.get('end5',)))
        old_med.msle_3_1 = None if CheckboxToBool(request.POST.get('ckmedi001',)) is 'True' else Medicationtype(generic = request.POST.get('gen6',), doseperdate = ToFloatMed(request.POST.get('dose6',)), startdate = DateToNone(request.POST.get('start6',)), stopdate = DateToNone(request.POST.get('end6',)))
        old_med.msle_3_2 = None if CheckboxToBool(request.POST.get('ckmedi001',)) is 'True' else Medicationtype(generic = request.POST.get('gen7',), doseperdate = ToFloatMed(request.POST.get('dose7',)), startdate = DateToNone(request.POST.get('start7',)), stopdate = DateToNone(request.POST.get('end7',)))
        old_med.msle_3_3 = None if CheckboxToBool(request.POST.get('ckmedi001',)) is 'True' else Medicationtype(generic = request.POST.get('gen8',), doseperdate = ToFloatMed(request.POST.get('dose8',)), startdate = DateToNone(request.POST.get('start8',)), stopdate = DateToNone(request.POST.get('end8',))),
        old_med.msle_3_4 = None if CheckboxToBool(request.POST.get('ckmedi001',)) is 'True' else Medicationtype(generic = request.POST.get('gen9',), doseperdate = ToFloatMed(request.POST.get('dose9',)), startdate = DateToNone(request.POST.get('start9',)), stopdate = DateToNone(request.POST.get('end9',)))
        old_med.msle_4_1 = None if CheckboxToBool(request.POST.get('ckmedi001',)) is 'True' else Medicationtype(generic = request.POST.get('gen10',), doseperdate = ToFloatMed(request.POST.get('dose10',)), startdate = DateToNone(request.POST.get('start10',)), stopdate = DateToNone(request.POST.get('end10',)))
        old_med.msle_4_2 = None if CheckboxToBool(request.POST.get('ckmedi001',)) is 'True' else Medicationtype(generic = request.POST.get('gen11',), doseperdate = ToFloatMed(request.POST.get('dose11',)), startdate = DateToNone(request.POST.get('start11',)), stopdate = DateToNone(request.POST.get('end11',)))
        old_med.msle_4_3 = None if CheckboxToBool(request.POST.get('ckmedi001',)) is 'True' else Medicationtype(generic = request.POST.get('gen12',), doseperdate = ToFloatMed(request.POST.get('dose12',)), startdate = DateToNone(request.POST.get('start12',)), stopdate = DateToNone(request.POST.get('end12',)))
        old_med.msle_4_4 = None if CheckboxToBool(request.POST.get('ckmedi001',)) is 'True' else Medicationtype(generic = request.POST.get('gen13',), doseperdate = ToFloatMed(request.POST.get('dose13',)), startdate = DateToNone(request.POST.get('start13',)), stopdate = DateToNone(request.POST.get('end13',)))
        old_med.msle_4_5 = None if CheckboxToBool(request.POST.get('ckmedi001',)) is 'True' else Medicationtype(generic = request.POST.get('gen14',), doseperdate = ToFloatMed(request.POST.get('dose14',)), startdate = DateToNone(request.POST.get('start14',)), stopdate = DateToNone(request.POST.get('end14',)))
        old_med.msle_4_6 = None if CheckboxToBool(request.POST.get('ckmedi001',)) is 'True' else Medicationtype(generic = request.POST.get('gen15',), doseperdate = ToFloatMed(request.POST.get('dose15',)), startdate = DateToNone(request.POST.get('start15',)), stopdate = DateToNone(request.POST.get('end15',)))
        old_med.msle_4_7 = None if CheckboxToBool(request.POST.get('ckmedi001',)) is 'True' else Medicationtype(generic = request.POST.get('gen16',), doseperdate = ToFloatMed(request.POST.get('dose16',)), startdate = DateToNone(request.POST.get('start16',)), stopdate = DateToNone(request.POST.get('end16',)))
        old_med.msle_4_8 = None if CheckboxToBool(request.POST.get('ckmedi001',)) is 'True' else Medicationtype(generic = request.POST.get('gen17',), doseperdate = ToFloatMed(request.POST.get('dose17',)), startdate = DateToNone(request.POST.get('start17',)), stopdate = DateToNone(request.POST.get('end17',)))
        old_med.msle_4_9 = None if CheckboxToBool(request.POST.get('ckmedi001',)) is 'True' else Medicationtype(generic = request.POST.get('gen18',), doseperdate = ToFloatMed(request.POST.get('dose18',)), startdate = DateToNone(request.POST.get('start18',)), stopdate = DateToNone(request.POST.get('end18',)))
        old_med.msle_4_10 = None if CheckboxToBool(request.POST.get('ckmedi001',)) is 'True' else Medicationtype(generic = request.POST.get('gen19',), doseperdate = ToFloatMed(request.POST.get('dose19',)), startdate = DateToNone(request.POST.get('start19',)), stopdate = DateToNone(request.POST.get('end19',)))
        old_med.msle_4_11 = None if CheckboxToBool(request.POST.get('ckmedi001',)) is 'True' else Medicationtype(generic = request.POST.get('gen20',), doseperdate = ToFloatMed(request.POST.get('dose20',)), startdate = DateToNone(request.POST.get('start20',)), stopdate = DateToNone(request.POST.get('end20',)))
        old_med.mgt_1_1 = None if CheckboxToBool(request.POST.get('ckmedi002',)) is 'True' else Medicationtype(generic = request.POST.get('gen21',), doseperdate = ToFloatMed(request.POST.get('dose21',)), startdate = DateToNone(request.POST.get('start21',)), stopdate = DateToNone(request.POST.get('end21',)))
        old_med.mgt_1_2 = None if CheckboxToBool(request.POST.get('ckmedi002',)) is 'True' else Medicationtype(generic = request.POST.get('gen22',), doseperdate = ToFloatMed(request.POST.get('dose22',)), startdate = DateToNone(request.POST.get('start22',)), stopdate = DateToNone(request.POST.get('end22',)))
        old_med.mgt_1_3 = None if CheckboxToBool(request.POST.get('ckmedi002',)) is 'True' else Medicationtype(generic = request.POST.get('gen23',), doseperdate = ToFloatMed(request.POST.get('dose23',)), startdate = DateToNone(request.POST.get('start23',)), stopdate = DateToNone(request.POST.get('end23',)))
        old_med.mgt_1_4 = None if CheckboxToBool(request.POST.get('ckmedi002',)) is 'True' else Medicationtype(generic = request.POST.get('gen24',), doseperdate = ToFloatMed(request.POST.get('dose24',)), startdate = DateToNone(request.POST.get('start24',)), stopdate = DateToNone(request.POST.get('end24',)))
        old_med.mgt_1_5 = None if CheckboxToBool(request.POST.get('ckmedi002',)) is 'True' else Medicationtype(generic = request.POST.get('gen25',), doseperdate = ToFloatMed(request.POST.get('dose25',)), startdate = DateToNone(request.POST.get('start25',)), stopdate = DateToNone(request.POST.get('end25',)))
        old_med.mgt_2_1 = None if CheckboxToBool(request.POST.get('ckmedi002',)) is 'True' else Medicationtype(generic = request.POST.get('gen26',), doseperdate = ToFloatMed(request.POST.get('dose26',)), startdate = DateToNone(request.POST.get('start26',)), stopdate = DateToNone(request.POST.get('end26',)))
        old_med.mgt_2_2 = None if CheckboxToBool(request.POST.get('ckmedi002',)) is 'True' else Medicationtype(generic = request.POST.get('gen27',), doseperdate = ToFloatMed(request.POST.get('dose27',)), startdate = DateToNone(request.POST.get('start27',)), stopdate = DateToNone(request.POST.get('end27',)))
        old_med.mgt_2_3 = None if CheckboxToBool(request.POST.get('ckmedi002',)) is 'True' else Medicationtype(generic = request.POST.get('gen28',), doseperdate = ToFloatMed(request.POST.get('dose28',)), startdate = DateToNone(request.POST.get('start28',)), stopdate = DateToNone(request.POST.get('end28',)))
        old_med.mgt_2_4 = None if CheckboxToBool(request.POST.get('ckmedi002',)) is 'True' else Medicationtype(generic = request.POST.get('gen29',), doseperdate = ToFloatMed(request.POST.get('dose29',)), startdate = DateToNone(request.POST.get('start29',)), stopdate = DateToNone(request.POST.get('end29',)))
        old_med.mgt_3_1 = None if CheckboxToBool(request.POST.get('ckmedi002',)) is 'True' else Medicationtype(generic = request.POST.get('gen30',), doseperdate = ToFloatMed(request.POST.get('dose30',)), startdate = DateToNone(request.POST.get('start30',)), stopdate = DateToNone(request.POST.get('end30',)))
        old_med.mgt_3_2 = None if CheckboxToBool(request.POST.get('ckmedi002',)) is 'True' else Medicationtype(generic = request.POST.get('gen31',), doseperdate = ToFloatMed(request.POST.get('dose31',)), startdate = DateToNone(request.POST.get('start31',)), stopdate = DateToNone(request.POST.get('end31',)))
        old_med.mgt_3_3 = None if CheckboxToBool(request.POST.get('ckmedi002',)) is 'True' else Medicationtype(generic = request.POST.get('gen32',), doseperdate = ToFloatMed(request.POST.get('dose32',)), startdate = DateToNone(request.POST.get('start32',)), stopdate = DateToNone(request.POST.get('end32',)))
        old_med.mgt_4_1 = None if CheckboxToBool(request.POST.get('ckmedi002',)) is 'True' else Medicationtype(generic = request.POST.get('gen33',), doseperdate = ToFloatMed(request.POST.get('dose33',)), startdate = DateToNone(request.POST.get('start33',)), stopdate = DateToNone(request.POST.get('end33',)))
        old_med.mgt_4_2 = None if CheckboxToBool(request.POST.get('ckmedi002',)) is 'True' else Medicationtype(generic = request.POST.get('gen34',), doseperdate = ToFloatMed(request.POST.get('dose34',)), startdate = DateToNone(request.POST.get('start34',)), stopdate = DateToNone(request.POST.get('end34',)))
        old_med.mgt_4_3 = None if CheckboxToBool(request.POST.get('ckmedi002',)) is 'True' else Medicationtype(generic = request.POST.get('gen35',), doseperdate = ToFloatMed(request.POST.get('dose35',)), startdate = DateToNone(request.POST.get('start35',)), stopdate = DateToNone(request.POST.get('end35',)))
        old_med.mgt_4_4 = None if CheckboxToBool(request.POST.get('ckmedi002',)) is 'True' else Medicationtype(generic = request.POST.get('gen36',), doseperdate = ToFloatMed(request.POST.get('dose36',)), startdate = DateToNone(request.POST.get('start36',)), stopdate = DateToNone(request.POST.get('end36',)))
        old_med.mgt_other = CheckboxToBool(request.POST.get('ckmgt_other',))
        old_med.save()
        
        this_date = old_visiting.visitdate
        mgt_other = CheckboxToBool(request.POST.get('ckmgt_other',))
        Othermedication.objects.filter(visitingid = temp_visitid).delete()
        othermed = request.POST.getlist('mgt_other_detail[]',)
        othermed_doseperdate = request.POST.getlist('otherdose[]',) 
        if mgt_other is 'True':
            for index in range(0, len(othermed)):
                if(othermed[index] != ''):
                    FollowOtherMed = Othermedication(visitingid = old_visiting,
                                    medicationname = othermed[index],
                                    doseperdate = othermed_doseperdate[index])
                    FollowOtherMed.save()
                        
        return HttpResponseRedirect(reverse('patientrecord', args=(old_visiting.studynumber.studynumber,)))
    

@login_required(login_url='login')
def followEdit(request, visitid):
    try: lab = Laboratoryinventoryinvestigation.objects.get(visitingid = visitid)
    except ObjectDoesNotExist: lab = None
    except IndexError: lab = None
    if haslnlab(lab) is True:
        lnlab = Lnlab.objects.get(lnlabid = lab.lnlabid.lnlabid) 
    else: 
        lnlab = None
    try:
        med = Medication.objects.get(visitingid = visitid)
    except ObjectDoesNotExist:
        med = None
    
    try: othermed = Othermedication.objects.filter(visitingid = visitid)
    except ObjectDoesNotExist: othermed = None
    except IndexError: othermed = None
        
    studynum = Visiting.objects.get(visitingid = visitid).studynumber
    visitdate_list = []
    visits = Visiting.objects.filter(studynumber = studynum).order_by('visitdate')
    for vs in visits:
        if str(vs.visitingid) != str(visitid):
            d = datetime.datetime.strptime(str(vs.visitdate), '%Y-%m-%d')
            visitdate_list.append({'value': str(datetime.datetime.strftime(d, '%Y-%m-%d'))})
        
    return render(request, 'followup-edit.html',
                      {'visiting':Visiting.objects.get(visitingid = visitid),
                      'med':med,
                      'othermed':othermed,
                      'lab':lab,
                      'lnlab':lnlab,
                      'sledai':Diseaseactivitysledai.objects.get(visitingid = visitid),
                      'damageindex':Damageindex.objects.get(visitingid = visitid),
                      'clinicalpresentation':Clinicalpresentation.objects.get(visitingid = visitid),
                      'visitdate_list': visitdate_list})




@login_required(login_url='login')
def enrollEdit(request, studynum):
    try: obgyn = Obgyn.objects.filter(studynumber = studynum).latest('recorddate')
    except ObjectDoesNotExist:
        obgyn = None
    return render(request, 'enrollment-edit.html',
                  {'patient':Studyidentity.objects.get(studynumber = studynum),
                   'acrcriteria':Acrcriteria.objects.get(studynumber = studynum),
                   'slicccriteria':Slicccriteria.objects.get(studynumber = studynum),
                    'familyhistory':Familyhistory.objects.filter(studynumber = studynum),
                    'comorbidity':Comorbidity.objects.filter(studynumber = studynum),
                    'medicalcondition':Medicalcondition.objects.get(studynumber = studynum),
                    'previousorganinvolvement':Previousorganinvolvement.objects.filter(studynumber = studynum),
                    'obgyn':obgyn})


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
        old_condition.mc4_9 = request.POST.get('mc4_9',)
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
        
        Familyhistory.objects.filter(studynumber = stnum).delete()
        Comorbidity.objects.filter(studynumber = stnum).delete()
        Previousorganinvolvement.objects.filter(studynumber = stnum).delete()

        other01 = CheckboxToBool(request.POST.get('other01',))
        other02 = CheckboxToBool(request.POST.get('other02',))
        other03 = CheckboxToBool(request.POST.get('other03',))
        other04 = CheckboxToBool(request.POST.get('other04',))        
        othertype = request.POST.getlist('othertype[]',)
        otherdetail = request.POST.getlist('otherdetail[]',)
        otherdate = request.POST.getlist('otherdate[]',)
        if other01 is not 'True':
            while 'inflection' in othertype: 
                index = othertype.index('inflection')
                othertype.remove('inflection')
                del otherdetail[index]
                del otherdate[index]
        if other02 is not 'True':
            while 'majorsurgery' in othertype:
                index = othertype.index('majorsurgery')
                othertype.remove('majorsurgery')
                del otherdetail[index]
                del otherdate[index]
        if other03 is not 'True':
            while 'osteoporosis' in othertype:
                index = othertype.index('osteoporosis')
                othertype.remove('osteoporosis')
                del otherdetail[index]
                del otherdate[index]
        if other04 is not 'True':
            while 'malignancy' in othertype:
                index = othertype.index('malignancy')
                othertype.remove('malignancy')
                del otherdetail[index]
                del otherdate[index]
        for index in range(0, len(othertype)):
            EnrollComorbidity = Comorbidity(studynumber = old_studyidentity,
                                        comorbiditytype = othertype[index],
                                        detail = otherdetail[index],
                                        diagnosedate = DateToNone(otherdate[index]))
            EnrollComorbidity.save()

        famlist = []
        famlist.append(request.POST.get('familydisease01',))
        famlist.append(request.POST.get('familydisease02',))
        famlist.append(request.POST.get('familydisease03',))
        famlist.append(request.POST.get('familydisease04',))
        famlist.append(request.POST.get('familydisease05',))
        famlist.append(request.POST.get('familydisease06',))
        famlist.append(request.POST.get('familydisease07',))
        famlist.append(request.POST.get('familydisease08',))
        famlist.append(request.POST.get('familydisease09',))
        famlist.append(request.POST.get('familydisease10',))
        father = request.POST.getlist('father[]',)
        mother = request.POST.getlist('mother[]',)
        son = request.POST.getlist('son[]',)
        daughter = request.POST.getlist('daughter[]',)
        sibling = request.POST.getlist('sibling[]',)
        for eachdisease in famlist:
            if eachdisease is not "0":
                EnrollFam = Familyhistory(studynumber = old_studyidentity,
                    disease = eachdisease,
                    father = iscontains(father,eachdisease),
                    mother = iscontains(mother,eachdisease),
                    sibling = iscontains(sibling,eachdisease),
                    daughter = iscontains(daughter,eachdisease),
                    son = iscontains(son,eachdisease),
                    relative = request.POST.get(eachdisease,))
                EnrollFam.save()

        renal = request.POST.get('organ1',)
        if renal == "renal":
            start = DateToNone(request.POST.get('startrenal',))
            remis = DateToNone(request.POST.get('remisrenal',))
            EnrollOrgan = Previousorganinvolvement(studynumber = old_studyidentity, 
                    organ = renal, detail = None, startdate = start, remissiondate = remis)
            EnrollOrgan.save()
        
        organlist = []
        organlist.append(request.POST.get('organ2',))
        organlist.append(request.POST.get('organ3',))
        organlist.append(request.POST.get('organ4',))
        organlist.append(request.POST.get('organ5',))
        organlist.append(request.POST.get('organ6',))
        organlist.append(request.POST.get('organ7',))
        organlist.append(request.POST.get('organ8',))
        
        for each_organ in organlist:
            if each_organ is not None:
                for each_detail in request.POST.getlist(str(each_organ)+'[]',):
                    remiss = DateToNone(request.POST.get('remis'+str(each_detail),))
                    start = DateToNone(request.POST.get('start'+str(each_detail),))
                    EnrollOrgan = Previousorganinvolvement(studynumber = old_studyidentity, 
                        organ = each_organ, detail = each_detail, startdate = start, remissiondate = remiss)
                    EnrollOrgan.save()
        
        old_Obgy = None
        newObgyn = None
        try:
            old_Obgy = Obgyn.objects.get(studynumber = old_studyidentity, recorddate = request.POST.get('obgyndate',))
            old_Obgy.gscore = NullToZero(request.POST.get('gscore',))
            old_Obgy.pscore = NullToZero(request.POST.get('pscore',))
            old_Obgy.ascore = NullToZero(request.POST.get('ascore',))
            old_Obgy.menstrualcycle = request.POST.get('menstrualcycle',)
            old_Obgy.pregnant = NullToZero(request.POST.get('pregnant',))
            old_Obgy.modeofcontraceptives = request.POST.get('modeofcontraceptives',)
            old_Obgy.save()
        except ObjectDoesNotExist:
            newObgyn = Obgyn(studynumber = old_studyidentity,
                     recorddate = request.POST.get('obgyndate',),
                     gscore = NullToZero(request.POST.get('gscore',)),
                     pscore = NullToZero(request.POST.get('pscore',)),
                     ascore = NullToZero(request.POST.get('ascore',)),
                     menstrualcycle = request.POST.get('menstrualcycle',),
                     pregnant = NullToZero(request.POST.get('pregnant',)),
                     modeofcontraceptives = request.POST.get('modeofcontraceptives',))
            newObgyn.save()
        
        return HttpResponseRedirect(reverse('patientrecord', args=(stnum,)))


    
from io import BytesIO as IO
from collections import OrderedDict
def download(request):
    sio = IO()
    PandasWriter = pd.ExcelWriter(sio, engine='xlsxwriter')
    
    df1 = pd.DataFrame(list(Studyidentity.objects.values_list(named=True)))
    df1.to_excel(PandasWriter, sheet_name='Studyidentity')
    df2 = pd.DataFrame(list(Acrcriteria.objects.values_list(named=True)))
    df2.to_excel(PandasWriter, sheet_name='Acrcriteria')
    df3 = pd.DataFrame(list(Slicccriteria.objects.values_list(named=True)))
    df3.to_excel(PandasWriter, sheet_name='Slicccriteria')
    df4 = pd.DataFrame(list(Familyhistory.objects.values_list(named=True)))
    df4.to_excel(PandasWriter, sheet_name='Familyhistory')
    df5 = pd.DataFrame(list(Medicalcondition.objects.values_list(named=True)))
    df5.to_excel(PandasWriter, sheet_name='Medicalcondition')
    df6 = pd.DataFrame(list(Obgyn.objects.values_list(named=True)))
    df6.to_excel(PandasWriter, sheet_name='Obgyn')
#    a = []
#    for e in Previouscomplication.objects.all():a.append(OrderedDict({'studynumber':e.studynumber.studynumber,'date':e.detail.date,'organ':e.detail.organ,'treatment':e.detail.treatment,'result':e.detail.result}))
#    df7 = pd.DataFrame(a)
#    df7.to_excel(PandasWriter, sheet_name='Previouscomplication')
    b = []
    for e in Previousorganinvolvement.objects.all():b.append(OrderedDict({'studynumber':e.studynumber.studynumber,'organ':e.organ,'detail':e.detail,'startdate':e.startdate,'remissiondate':e.remissiondate}))
    df8 = pd.DataFrame(b)
    df8.to_excel(PandasWriter, sheet_name='Previousorganinvolvement')
    df9 = pd.DataFrame(list(Riskbehavior.objects.values_list(named=True)))
    df9.to_excel(PandasWriter, sheet_name='Riskbehavior')
    
    df10 = pd.DataFrame(list(Visiting.objects.values_list(named=True)))
    df10.to_excel(PandasWriter, sheet_name='Visiting')
    df11 = pd.DataFrame(list(Clinicalpresentation.objects.values_list(named=True)))
    df11.to_excel(PandasWriter, sheet_name='Clinicalpresentation')
    df12 = pd.DataFrame(list(Damageindex.objects.values_list(named=True)))
    df12.to_excel(PandasWriter, sheet_name='Damageindex')
    df13 = pd.DataFrame(list(Diseaseactivitysledai.objects.values_list(named=True)))
    df13.to_excel(PandasWriter, sheet_name='Diseaseactivitysledai')
    c = []
    for m in Medication.objects.all():
        c.append(OrderedDict({'studynumber':m.studynumber.studynumber,
                              'visitingid':m.visitingid.visitingid,
                              'visitdate':m.visitdate,
                              'Traditional':m.msle_1_1.doseperdate,
                              'Selective COX-2 inhibitor':m.msle_1_2.doseperdate,
                              'Specific COX-2 inhibitor':m.msle_1_3.doseperdate,
                              'Chloroquine (Aralen)':m.msle_2_1.doseperdate,
                              'Hydroxychloroquine (Plaquenil)':m.msle_2_2.doseperdate,
                              'Prednisolone':m.msle_3_1.doseperdate,
                              'Methylprednisolone (IV)':m.msle_3_2.doseperdate,
                              'Dexamethasone (IV)':m.msle_3_3.doseperdate,
                              'Dexamethasone (Oral)':m.msle_3_4.doseperdate,
                              'Methotrexate (MTX)':m.msle_4_1.doseperdate,
                              'Azathioprine':m.msle_4_2.doseperdate,
                              'Cyclophosphamide (oral)':m.msle_4_3.doseperdate,
                              'Cyclophosphamide (IV)':m.msle_4_4.doseperdate,
                              'Mycophenolate mofetil (MMF)':m.msle_4_5.doseperdate,
                              'Myfortic (Mycophenolic acid)':m.msle_4_6.doseperdate,
                              'Cyclosporin A':m.msle_4_7.doseperdate,
                              'Tacrolimus':m.msle_4_8.doseperdate,
                              'Danazol':m.msle_4_9.doseperdate,
                              'Dapsone':m.msle_4_10.doseperdate,
                              'Colchicine':m.msle_4_11.doseperdate,
                              'ACEI':m.mgt_1_1.doseperdate,
                              'ARB':m.mgt_1_2.doseperdate,
                              'Diuretics':m.mgt_1_3.doseperdate,
                              'Beta-blockers':m.mgt_1_4.doseperdate,
                              'Ca channel blockers':m.mgt_1_5.doseperdate,
                              'Statins':m.mgt_2_1.doseperdate,
                              'Fibrates(Gemfibrozil,Fenofibrate)':m.mgt_2_2.doseperdate,
                              'Resin(Cholestyramine,Colestipol)':m.mgt_2_3.doseperdate,
                              'Nicotinic acid':m.mgt_2_4.doseperdate,
                              'Bisphosphonates':m.mgt_3_1.doseperdate,
                              'Ca supplement, CaCO3':m.mgt_3_2.doseperdate,
                              'Vitamin D':m.mgt_3_3.doseperdate,
                              'ASA':m.mgt_4_1.doseperdate,
                              'Warfarin':m.mgt_4_2.doseperdate,
                              'Folic acid':m.mgt_4_3.doseperdate,
                              'MTV':m.mgt_4_4.doseperdate,
                              'Other':m.mgt_other}))
    df15 = pd.DataFrame(c)
    df15.to_excel(PandasWriter, sheet_name='Medication')
    d = []
    for l in Laboratoryinventoryinvestigation.objects.all():
        d.append(OrderedDict({'studynumber':l.studynumber.studynumber,
                              'visitingid':l.visitingid.visitingid,
                              'visitdate':l.visitdate,
                              'hb':l.hb,
                              'wbc':l.wbc,
                              'n':l.n,
                              'n':l.l,
                              'platelets':l.platelets,
                              'esr':l.esr,
                              'wbc_hpf1':l.wbc_hpf1,
                              'rbc_hpf1':l.rbc_hpf1,
                              'wbccasts1':l.wbccasts1,
                              'rbccasts1':l.rbccasts1,
                              'granularcasts1':l.granularcasts1,
                              'wbc_hpf2':l.wbc_hpf2,
                              'rbc_hpf2':l.rbc_hpf2,
                              'wbccasts2':l.wbccasts2,
                              'rbccasts2':l.rbccasts2,
                              'granularcasts2':l.granularcasts2,
                              'glucose':l.glucose,
                              'protein':l.protein,
                              'tp_spoturineprotein':l.tp_spoturineprotein,
                              'cre_spoturinecreatinine':l.cre_spoturinecreatinine,
                              'tfhr_urineprotein':l.tfhr_urineprotein,
                              'tfhr_urinecreatinine':l.tfhr_urinecreatinine,
                              'upci':l.upci,
                              'fbs':l.fbs,
                              'hba1c':l.hba1c,
                              'bun':l.bun,
                              'cr':l.cr,
                              'alp':l.alp,
                              'ast':l.ast,
                              'alt':l.alt,
                              'ggt':l.ggt,
                              'ldh':l.ldh,
                              'albumin':l.albumin,
                              'tdbilirubin':l.tdbilirubin,
                              'crp':l.crp,
                              'choles':l.choles,
                              'tg':l.tg,
                              'ldl':l.ldl,
                              'hdl':l.hdl,
                              'inr':l.inr,
                              'anti_dsdna':l.anti_dsdna,
                              'antism':l.antism,
                              'antirnp':l.antirnp,
                              'antiro':l.antiro,
                              'antila':l.antila,
                              'aca':l.aca,
                              'lupusanticoagulant':l.lupusanticoagulant,
                              'b2gpi':l.b2gpi,
                              'c3':l.c3,
                              'c4':l.c4,
                              'ch50':l.ch50,
                              'hbsag':l.hbsag,
                              'antihbs':l.antihbs,
                              'antihbc':l.antihbc,
                              'antihcv':l.antihcv,
                              'antihiv':l.antihiv,
                              'anticic':l.anticic,
                              'il6':l.il6,
                              'mpa':l.mpa,
                              'fk507':l.fk507,
                              'cyclosporin':l.cyclosporin,
                              'cytokine':l.cytokine,
                              'l1l4spine_bmd':l.l1l4spine_bmd, 
                              'l1l4spine_tscore':l.l1l4spine_tscore, 
                              'l1l4spine_date':l.l1l4spine_date, 
                              'hip_bmd':l.hip_bmd, 
                              'hip_tscore':l.hip_tscore,  
                              'hip_date':l.hip_date, 
                              'radius_bmd':l.radius_bmd, 
                              'radius_tscore':l.radius_tscore, 
                              'radius_date':l.radius_date,
                              'stoolparasite_status':l.stoolparasite.status if l.stoolparasite is not None else None,
                              'cxr_status':l.cxr.status if l.cxr is not None else None,
                              'ekg_status':l.ekg.status if l.ekg is not None else None,
                              'echo_status':l.echo.status if l.echo is not None else None,
                              'stoolparasite_date':l.stoolparasite.date if l.stoolparasite is not None else None,
                              'cxr_date':l.cxr.date if l.cxr is not None else None,
                              'ekg_date':l.ekg.date if l.ekg is not None else None,
                              'echo_date':l.echo.date if l.echo is not None else None,
                              'stoolparasite_detail':l.stoolparasite.detail if l.stoolparasite is not None else None,
                              'cxr_detail':l.cxr.detail if l.cxr is not None else None,
                              'ekg_detail':l.ekg.detail if l.ekg is not None else None,
                              'echo_detail':l.echo.detail if l.echo is not None else None}))
        
    df14 = pd.DataFrame(d)
    df14.to_excel(PandasWriter, sheet_name='Lab')
    df16 = pd.DataFrame(list(Lnlab.objects.values_list(named=True)))
    df16.to_excel(PandasWriter, sheet_name='Lnlab')
    
    PandasWriter.save()
    PandasWriter.close()
    
    sio.seek(0)
    response = HttpResponse(sio.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=PatientData.xlsx'

    return response

@login_required(login_url='login')
def hnDetail(request):
    if str(request.user) != 'admin':
        return HttpResponseRedirect('/index/')
    return render(request, 'hn-detail.html',{'hns': HN.objects.all()})

@login_required(login_url='login')
def hnEdit(request):
    if str(request.user) != 'admin':
        return HttpResponseRedirect('/index/')
    hn_list = []
    hns = HN.objects.exclude(hn__isnull=True).exclude(hn__exact='')
    for hn in hns:
        hn_list.append({'st': str(hn.studynumber),'hn': str(hn.hn),})
    return render(request, 'hn-edit.html',{'hns': HN.objects.all(),'hn_list':hn_list})

@login_required(login_url='login')
def hnEditPost(request):
    if str(request.user) != 'admin':
        return HttpResponseRedirect('/index/')
    if request.method == "POST":
        hns = HN.objects.all()
        for hn in hns:
            oldhn = HN.objects.get(studynumber = hn.studynumber)
            newhn = request.POST.get(''+str(hn.studynumber),)
            if oldhn.hn is not newhn:
                oldhn.hn = newhn
                oldhn.save()
#    return render(request, 'hn-edit.html',{'hns': HN.objects.all(),'newhn':newhn})
    return HttpResponseRedirect('/hnDetail/')

def debug(request):
    return render(request, 'debug.html')