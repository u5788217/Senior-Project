# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.postgres.fields import ArrayField
from postgres_composite_types import CompositeType



class Previoustype(CompositeType):
    date = models.DateField(blank=True, null=True)
    organ = models.TextField(blank=True, null=True)
    treatment = models.TextField(blank=True, null=True)
    result = models.TextField(blank=True, null=True)
    class Meta:
        db_type = 'previoustype' #Name in PostgreSQL
        
class Labtype(CompositeType):
    status = models.TextField(blank=True, null=True)
    date =  models.DateField(blank=True, null=True)
    class Meta:
        db_type = 'labtype'
        
class Medicationtype(CompositeType):
    generic = models.TextField(blank=True, null=True)
    doseperdate = models.FloatField(blank=True, null=True)
    startdate = models.DateField(blank=True, null=True)
    stopdate = models.DateField(blank=True, null=True)
    class Meta:
        db_type = 'medicationtype'

class Acrcriteria(models.Model):
    studynumber = models.ForeignKey('Studyidentity', models.DO_NOTHING, db_column='studynumber', primary_key=True)
    acr1 = models.NullBooleanField()
    acr2 = models.NullBooleanField()
    acr3 = models.NullBooleanField()
    acr4 = models.NullBooleanField()
    acr5 = models.NullBooleanField()
    acr6 = models.NullBooleanField()
    acr7 = models.NullBooleanField()
    acr8 = models.NullBooleanField()
    acr9 = models.NullBooleanField()
    acr10 = models.NullBooleanField()
    acr11 = models.NullBooleanField()

    class Meta:
        managed = False
        db_table = 'acrcriteria'


class Clinicalpresentation(models.Model):
    visitingid = models.ForeignKey('Visiting', models.DO_NOTHING, db_column='visitingid', primary_key=True)
    studynumber = models.ForeignKey('Studyidentity', models.DO_NOTHING, db_column='studynumber')
    visitdate = models.DateField()
    cp_1 = models.NullBooleanField()
    cp_2 = models.NullBooleanField()
    cp_3 = models.NullBooleanField()
    cp_4 = models.NullBooleanField()
    cp_5 = models.NullBooleanField()
    cp_6 = models.CharField(max_length=200, blank=True, null=True)
    cp_7 = models.NullBooleanField()
    cp_8 = models.NullBooleanField()
    cp_9 = models.NullBooleanField()
    cp_10 = models.NullBooleanField()
    cp_11 = models.NullBooleanField()
    cp_12 = models.NullBooleanField()
    cp_13 = models.NullBooleanField()
    cp_14 = models.NullBooleanField()
    cp_15 = models.NullBooleanField()
    cp_16 = models.NullBooleanField()
    cp_17 = models.NullBooleanField()
    cp_18 = models.NullBooleanField()
    cp_19 = models.NullBooleanField()
    cp_20 = models.NullBooleanField()
    cp_21 = models.NullBooleanField()
    cp_22 = models.NullBooleanField()
    cp_23 = models.NullBooleanField()
    cp_24 = models.NullBooleanField()
    cp_25 = models.NullBooleanField()
    cp_26 = models.NullBooleanField()
    cp_27 = models.NullBooleanField()
    cp_28 = models.NullBooleanField()
    cp_29 = models.NullBooleanField()

    class Meta:
        managed = False
        db_table = 'clinicalpresentation'
        unique_together = (('studynumber', 'visitdate'),)

class Damageindex(models.Model):
    visitingid = models.ForeignKey('Visiting', models.DO_NOTHING, db_column='visitingid', primary_key=True)
    studynumber = models.ForeignKey('Studyidentity', models.DO_NOTHING, db_column='studynumber')
    visitdate = models.DateField()
    di_1 = models.NullBooleanField()
    di_2 = models.NullBooleanField()
    di_3 = models.NullBooleanField()
    di_4 = models.NullBooleanField()
    di_5 = models.FloatField(blank=True, null=True)
    di_6 = models.NullBooleanField()
    di_7 = models.NullBooleanField()
    di_8 = models.NullBooleanField()
    di_9 = models.NullBooleanField()
    di_10 = models.NullBooleanField()
    di_11 = models.NullBooleanField()
    di_12 = models.FloatField(blank=True, null=True)
    di_13 = models.NullBooleanField()
    di_14 = models.NullBooleanField()
    di_15 = models.NullBooleanField()
    di_16 = models.NullBooleanField()
    di_17 = models.NullBooleanField()
    di_18 = models.FloatField(blank=True, null=True)
    di_19 = models.NullBooleanField()
    di_20 = models.NullBooleanField()
    di_21 = models.NullBooleanField()
    di_22 = models.NullBooleanField()
    di_23 = models.NullBooleanField()
    di_24 = models.NullBooleanField()
    di_25 = models.FloatField(blank=True, null=True)
    di_26 = models.NullBooleanField()
    di_27 = models.NullBooleanField()
    di_28 = models.NullBooleanField()
    di_29 = models.NullBooleanField()
    di_30 = models.NullBooleanField()
    di_31 = models.NullBooleanField()
    di_32 = models.NullBooleanField()
    di_33 = models.FloatField(blank=True, null=True)
    di_34 = models.NullBooleanField()
    di_35 = models.NullBooleanField()
    di_36 = models.NullBooleanField()
    di_37 = models.NullBooleanField()
    di_38 = models.NullBooleanField()
    di_39 = models.NullBooleanField()
    di_40 = models.NullBooleanField()
    di_41 = models.FloatField(blank=True, null=True)
    di_total = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'damageindex'
        unique_together = (('studynumber', 'visitdate'),)

class Diseaseactivitysledai(models.Model):
    visitingid = models.ForeignKey('Visiting', models.DO_NOTHING, db_column='visitingid', primary_key=True)
    studynumber = models.ForeignKey('Studyidentity', models.DO_NOTHING, db_column='studynumber')
    visitdate = models.DateField()
    physiciansglobalassessment = models.IntegerField(blank=True, null=True)
    seizure = models.NullBooleanField()
    psychosis = models.NullBooleanField()
    organicbrainsyndrome = models.NullBooleanField()
    visualdisturbance = models.NullBooleanField()
    cranialnerve = models.NullBooleanField()
    cranialnervedetail = models.CharField(max_length=50, blank=True, null=True)
    lupusheadache = models.NullBooleanField()
    cva = models.NullBooleanField()
    vasculitis = models.NullBooleanField()
    arthritis = models.NullBooleanField()
    arthritisjointamount = models.IntegerField(blank=True, null=True)
    myositis = models.NullBooleanField()
    casts = models.NullBooleanField()
    hematuria = models.NullBooleanField()
    proteinuria = models.NullBooleanField()
    pyuria = models.NullBooleanField()
    lowcomplement = models.NullBooleanField()
    increaseddnabinding = models.NullBooleanField()
    rash = models.NullBooleanField()
    alopecia = models.NullBooleanField()
    mucousmembrane = models.NullBooleanField()
    pleurisy = models.NullBooleanField()
    pericarditis = models.NullBooleanField()
    thrombocytopenia = models.NullBooleanField()
    leukopenia = models.NullBooleanField()
    fever = models.NullBooleanField()
    sledai_total = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'diseaseactivitysledai'
        unique_together = (('studynumber', 'visitdate'),)


class Familyhistory(models.Model):
    famid = models.AutoField(primary_key=True)
    studynumber = models.ForeignKey('Studyidentity', models.DO_NOTHING, db_column='studynumber')
    disease = models.TextField(blank=True, null=True)
    father = models.NullBooleanField()
    mother = models.NullBooleanField()
    sibling = models.NullBooleanField()
    daughter = models.NullBooleanField()
    son = models.NullBooleanField()
    relative = models.TextField(blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'familyhistory'


class Laboratoryinventoryinvestigation(models.Model):
    visitingid = models.ForeignKey('Visiting', models.DO_NOTHING, db_column='visitingid', primary_key=True)
    studynumber = models.ForeignKey('Studyidentity', models.DO_NOTHING, db_column='studynumber')
    lnlabid = models.ForeignKey('Lnlab', models.DO_NOTHING, db_column='lnlabid', blank=True, null=True)
    visitdate = models.DateField()
    hb = models.FloatField(blank=True, null=True)
    wbc = models.FloatField(blank=True, null=True)
    n = models.FloatField(blank=True, null=True)
    l = models.FloatField(blank=True, null=True)
    platelets = models.FloatField(blank=True, null=True)
    esr = models.FloatField(blank=True, null=True)
    wbc_hpf = models.FloatField(blank=True, null=True)
    rbc_hpf = models.FloatField(blank=True, null=True)
    wbccasts = models.FloatField(blank=True, null=True)
    rbccasts = models.FloatField(blank=True, null=True)
    granularcasts = models.FloatField(blank=True, null=True)
    glucose = models.FloatField(blank=True, null=True)
    protein = models.FloatField(blank=True, null=True)
    tp_spoturineprotein = models.FloatField(blank=True, null=True)
    cre_spoturinecreatinine = models.FloatField(blank=True, null=True)
    tfhr_urineprotein = models.FloatField(blank=True, null=True)
    tfhr_urinecreatinine = models.FloatField(blank=True, null=True)
    upci = models.FloatField(blank=True, null=True)
    fbs = models.FloatField(blank=True, null=True)
    hba1c = models.FloatField(blank=True, null=True)
    bun = models.FloatField(blank=True, null=True)
    cr = models.FloatField(blank=True, null=True)
    alp = models.FloatField(blank=True, null=True)
    ast = models.FloatField(blank=True, null=True)
    alt = models.FloatField(blank=True, null=True)
    ggt = models.FloatField(blank=True, null=True)
    ldh = models.FloatField(blank=True, null=True)
    albumin = models.FloatField(blank=True, null=True)
    tdbilirubin = ArrayField(models.FloatField(blank=True), null=True)  # FLOAT[]
    crp = models.FloatField(blank=True, null=True)
    choles = models.FloatField(blank=True, null=True)
    tg = models.FloatField(blank=True, null=True)
    ldl = models.FloatField(blank=True, null=True)
    hdl = models.FloatField(blank=True, null=True)
    inr = models.FloatField(blank=True, null=True)
    anatiter = models.NullBooleanField()
    homogeneous1 = models.FloatField(blank=True, null=True)
    peripheral1 = models.FloatField(blank=True, null=True)
    speckled1 = models.FloatField(blank=True, null=True)
    nucleolar1 = models.FloatField(blank=True, null=True)
    anti_dsdna = models.FloatField(blank=True, null=True)
    antism = models.NullBooleanField()
    antirnp = models.NullBooleanField()
    antiro = models.NullBooleanField()
    antila = models.NullBooleanField()
    aca = models.FloatField(blank=True, null=True)
    lupusanticoagulant = models.NullBooleanField()
    b2gpi = models.FloatField(blank=True, null=True)
    c3 = models.FloatField(blank=True, null=True)
    c4 = models.FloatField(blank=True, null=True)
    ch50 = models.FloatField(blank=True, null=True)
    hbsag = models.NullBooleanField()
    antihbs = models.NullBooleanField()
    antihbc = models.NullBooleanField()
    antihcv = models.NullBooleanField()
    antihiv = models.NullBooleanField()
    anticic = models.FloatField(blank=True, null=True)
    il6 = models.FloatField(blank=True, null=True)
    mpa = models.FloatField(blank=True, null=True)
    fk507 = models.FloatField(blank=True, null=True)
    cyclosporin = models.FloatField(blank=True, null=True)
    cytokine = models.NullBooleanField()
    l1l4spinebmd_tscore = ArrayField(models.FloatField(blank=True), null=True)  # FLOAT[]
    hipbmd_tscore = ArrayField(models.FloatField(blank=True), null=True)   # FLOAT[]
    radiusbmd_tscore = ArrayField(models.FloatField(blank=True), null=True)   # FLOAT[]
    stoolparasite = Labtype.Field()  # LabType
    cxr = Labtype.Field() # LabType
    ekg = Labtype.Field()  # LabType
    echo = Labtype.Field()  # LabType

    class Meta:
        managed = False
        db_table = 'laboratoryinventoryinvestigation'
        unique_together = (('studynumber', 'visitdate'),)

class Lnlab(models.Model):
    lnlabid = models.AutoField(primary_key=True)
    renalbiopsyclass = models.TextField(blank=True, null=True)
    renalbiopsydate = models.DateField(blank=True, null=True)
    activityindex = models.FloatField(blank=True, null=True)
    chronicityindex = models.FloatField(blank=True, null=True)
    ln_1 = models.FloatField(blank=True, null=True)
    ln_2 = models.FloatField(blank=True, null=True)
    ln_3 = models.TextField(blank=True, null=True)
    ln_4 = models.TextField(blank=True, null=True)
    ln_5 = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lnlab'


class Medicalcondition(models.Model):
    studynumber = models.ForeignKey('Studyidentity', models.DO_NOTHING, db_column='studynumber', primary_key=True)
    mc1_1 = models.NullBooleanField()
    mc1_2 = models.NullBooleanField()
    mc1_3 = models.NullBooleanField()
    mc1_4 = models.NullBooleanField()
    mc1_5 = models.NullBooleanField()
    mc1_6 = models.NullBooleanField()
    mc1_7 = models.NullBooleanField()
    mc1_8 = models.NullBooleanField()
    mc1_9 = models.NullBooleanField()
    mc1_10 = models.NullBooleanField()
    mc1_11 = models.NullBooleanField()
    mc2_1 = models.NullBooleanField()
    mc2_2 = models.NullBooleanField()
    mc2_3 = models.NullBooleanField()
    mc2_4 = models.NullBooleanField()
    mc2_5 = models.NullBooleanField()
    mc2_6 = models.NullBooleanField()
    mc3_1 = models.NullBooleanField()
    mc3_2 = models.NullBooleanField()
    mc3_3 = models.NullBooleanField()
    mc3_4 = models.NullBooleanField()
    mc3_5 = models.NullBooleanField()
    mc4_1 = models.NullBooleanField()
    mc4_2 = models.NullBooleanField()
    mc4_3 = models.NullBooleanField()
    mc4_4 = models.NullBooleanField()
    mc4_5 = models.NullBooleanField()
    mc4_6 = models.NullBooleanField()
    mc4_7 = models.NullBooleanField()
    mc4_8 = models.NullBooleanField()
    mc4_9 = ArrayField(models.TextField(blank=True), null=True)

    class Meta:
        managed = False
        db_table = 'medicalcondition'
        
class Comorbidity(models.Model):
    comorbidityid = models.AutoField(primary_key=True)
    studynumber = models.ForeignKey('Studyidentity', models.DO_NOTHING, db_column='studynumber')
    comorbiditytype = models.TextField(blank=True, null=True)
    detail = models.TextField(blank=True, null=True)
    diagnosedate = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comorbidity'

class Medication(models.Model):
    visitingid = models.ForeignKey('Visiting', models.DO_NOTHING, db_column='visitingid', primary_key=True)
    studynumber = models.ForeignKey('Studyidentity', models.DO_NOTHING, db_column='studynumber')
    visitdate = models.DateField()
    msle_1_1 = Medicationtype.Field()  # Medication type
    msle_1_2 = Medicationtype.Field()  # Medication type
    msle_1_3 = Medicationtype.Field()  # This field type is a guess.
    msle_2_1 = Medicationtype.Field()  # This field type is a guess.
    msle_2_2 = Medicationtype.Field()  # This field type is a guess.
    msle_3_1 = Medicationtype.Field()  # This field type is a guess.
    msle_3_2 = Medicationtype.Field()  # This field type is a guess.
    msle_3_3 = Medicationtype.Field()  # This field type is a guess.
    msle_3_4 = Medicationtype.Field()  # This field type is a guess.
    msle_4_1 = Medicationtype.Field()  # This field type is a guess.
    msle_4_2 = Medicationtype.Field()  # This field type is a guess.
    msle_4_3 = Medicationtype.Field()  # This field type is a guess.
    msle_4_4 = Medicationtype.Field()  # This field type is a guess.
    msle_4_5 = Medicationtype.Field()  # This field type is a guess.
    msle_4_6 = Medicationtype.Field()  # This field type is a guess.
    msle_4_7 = Medicationtype.Field()  # This field type is a guess.
    msle_4_8 = Medicationtype.Field()  # This field type is a guess.
    msle_4_9 = Medicationtype.Field()  # This field type is a guess.
    msle_4_10 = Medicationtype.Field()  # This field type is a guess.
    msle_4_11 = Medicationtype.Field()  # This field type is a guess.
    mgt_1_1 = Medicationtype.Field()  # This field type is a guess.
    mgt_1_2 = Medicationtype.Field()  # This field type is a guess.
    mgt_1_3 = Medicationtype.Field()  # This field type is a guess.
    mgt_1_4 = Medicationtype.Field()  # This field type is a guess.
    mgt_1_5 = Medicationtype.Field()  # This field type is a guess.
    mgt_2_1 = Medicationtype.Field()  # This field type is a guess.
    mgt_2_2 = Medicationtype.Field()  # This field type is a guess.
    mgt_2_3 = Medicationtype.Field()  # This field type is a guess.
    mgt_2_4 = Medicationtype.Field()  # This field type is a guess.
    mgt_3_1 = Medicationtype.Field()  # This field type is a guess.
    mgt_3_2 = Medicationtype.Field()  # This field type is a guess.
    mgt_3_3 = Medicationtype.Field()  # This field type is a guess.
    mgt_4_1 = Medicationtype.Field()  # This field type is a guess.
    mgt_4_2 = Medicationtype.Field()  # This field type is a guess.
    mgt_4_3 = Medicationtype.Field()  # Medication type
    mgt_4_4 = Medicationtype.Field()
    mgt_other = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'medication'
        unique_together = (('studynumber', 'visitdate'),)

class Obgyn(models.Model):
    studynumber = models.ForeignKey('Studyidentity', models.DO_NOTHING, db_column='studynumber', primary_key=True)
    recorddate = models.DateField()
    gscore = models.FloatField(blank=True, null=True)
    pscore = models.FloatField(blank=True, null=True)
    ascore = models.FloatField(blank=True, null=True)
    menstrualcycle = models.TextField(blank=True, null=True)
    pregnant = models.FloatField(blank=True, null=True)
    modeofcontraceptives = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'obgyn'
        unique_together = (('studynumber', 'recorddate'),)


class Previouscomplication(models.Model):
    pcid = models.AutoField(primary_key=True)
    studynumber = models.ForeignKey('Studyidentity', models.DO_NOTHING, db_column='studynumber')
    detail = Previoustype.Field()

    class Meta:
        managed = False
        db_table = 'previouscomplication'
        unique_together = (('pcid', 'studynumber'),)


class Previousorganinvolvement(models.Model):
    poiid = models.AutoField(primary_key=True)
    studynumber = models.ForeignKey('Studyidentity', models.DO_NOTHING, db_column='studynumber')
    detail = Previoustype.Field()

    class Meta:
        managed = False
        db_table = 'previousorganinvolvement'
        unique_together = (('poiid', 'studynumber'),)


class Riskbehavior(models.Model):
    studynumber = models.ForeignKey('Studyidentity', models.DO_NOTHING, db_column='studynumber', primary_key=True)
    recorddate = models.DateField()
    rb_1 = models.FloatField(blank=True, null=True)
    rb_2 = models.FloatField(blank=True, null=True)
    rb_3 = models.FloatField(blank=True, null=True)
    rb_4 = models.FloatField(blank=True, null=True)
    rb_5 = models.FloatField(blank=True, null=True)
    rb_6 = models.FloatField(blank=True, null=True)
    rb_7 = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'riskbehavior'
        unique_together = (('studynumber', 'recorddate'),)


class Slicccriteria(models.Model):
    studynumber = models.ForeignKey('Studyidentity', models.DO_NOTHING, db_column='studynumber', primary_key=True)
    slicc1 = models.NullBooleanField()
    slicc2 = models.NullBooleanField()
    slicc3 = models.NullBooleanField()
    slicc4 = models.NullBooleanField()
    slicc5 = models.NullBooleanField()
    slicc6 = models.NullBooleanField()
    slicc7 = models.NullBooleanField()
    slicc8 = models.NullBooleanField()
    slicc9 = models.NullBooleanField()
    slicc10 = models.NullBooleanField()
    slicc11 = models.NullBooleanField()
    slicc12 = models.NullBooleanField()
    slicc13 = models.NullBooleanField()
    slicc14 = models.NullBooleanField()
    slicc15 = models.NullBooleanField()
    slicc16 = models.NullBooleanField()
    slicc17 = models.NullBooleanField()

    class Meta:
        managed = False
        db_table = 'slicccriteria'

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)

class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'

class Medicationnote(models.Model):
    recordid = models.AutoField(primary_key=True)
    studynumber = models.ForeignKey('Studyidentity', models.DO_NOTHING, db_column='studynumber')
    date = models.DateField(blank=True, null=True)
    medication = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'medicationnote'

class Studyidentity(models.Model):
    studynumber = models.CharField(primary_key=True, max_length=6)
    dateofdiagnosis = models.DateField(blank=True, null=True)
    dateofenrollment = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=7, blank=True, null=True)
    dateofbirth = models.DateField(blank=True, null=True)
    religion = models.CharField(max_length=20, blank=True, null=True)
    education = models.CharField(max_length=30, blank=True, null=True)
    maritalstatus = models.CharField(max_length=10, blank=True, null=True)
    region = models.CharField(max_length=10, blank=True, null=True)
    occupation = models.CharField(max_length=50, blank=True, null=True)
    income = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'studyidentity'

class Visiting(models.Model):
    visitingid = models.AutoField(primary_key=True)
    studynumber = models.ForeignKey(Studyidentity, models.DO_NOTHING, db_column='studynumber')
    visitdate = models.DateField()
    bp = models.CharField(max_length=10, blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    username = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='username', null=True, blank=True)
    nextvisit = models.DateField()
    visitnote = models.TextField(blank=True, null=True)
    visitfile = models.TextField(blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'visiting'
        unique_together = (('visitingid','studynumber', 'visitdate'),)