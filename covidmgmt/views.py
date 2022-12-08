from ast import expr_context
from pydoc import doc
#from signal import pthread_kill
from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.db import connection
import time
import hashlib

# Create your views here.
def Home(request):
    #"SELECT COUNT(*) FROM covidmgmt_patient;"
    total=Patient.objects.count()
    #"SELECT COUNT(*) FROM covidmgmt_patient WHERE status='Active';"
    active=Patient.objects.filter(status='Active').count()
    #"SELECT COUNT(*) FROM covidmgmt_patient WHERE status='Inactive';"
    cured=Patient.objects.filter(status='Inactive').count()
    return render(request,"1_index.html",{"total":total,"active":active,"cured":cured})

def about_us(request):
    return render(request,"2_about_us.html")

def Find_Doctor(request):
    doctors=Doctor.objects.all()
    return render(request,"3_Find_Doctor.html",{"doc":doctors})

def Medical_Services(request):
    services=Service.objects.all()
    return render(request,"4_Medical_Services.html",{"services":services})

def Ward_Details(request):
    ward=Ward.objects.all()
    return render(request,"4_5_Ward_details.html",{"ward":ward})

def registration_patient(request):
    return render(request,"5_registration_patient.html")

def registration_patient_submit(request):
    fname=request.GET.get('fname')
    lname=request.GET.get('lname')
    address=request.GET.get('address')
    phoneno=request.GET.get('phoneno')
    gender=request.GET.get('gender')
    discript=request.GET.get('discript')
    passwd=request.GET.get('passwd')
    passwd=hashlib.md5(passwd.encode('utf-8')).hexdigest()
    date=time.strftime("%Y-%m-%d %H:%M:%S")
    obj=Patient(first_name=fname,last_name=lname,gender=gender,phone_no=phoneno,address=address,discription=discript,Date_of_Admit=date,password=passwd)
    obj.save()
    id=obj.p_id
    str1="Successfully regeistered!!! \n your alloted ID: "+str(id)+"\n keep this for future logins"
    return HttpResponse(str1)

def allloginpage(request):
    return render(request,"5_5_allloginpage.html")

def patient_login(request):
    return render(request,"6_patient_login.html")

def patient_login1(request):
    id=request.POST.get('uname')
    pswd=request.POST.get('psw')
    if id.isdigit():
        pswd=hashlib.md5(pswd.encode('utf-8')).hexdigest()
        doc=Patient.objects.filter(p_id=id,password=pswd)
        if(doc):
            cursor=connection.cursor()
            response=patientresult(request,cursor,id)
            response.set_cookie('patid',id)
            return response
        else:
            return render(request,"6_patient_login.html",{"incorect":True})
    return render(request,"6_patient_login.html",{"incorect":True})

def doctor_login(request):
        return render(request,"7_doctor_login.html",{"incorect":False})

def doctor_login1(request):
    id=request.POST.get('uname')
    pswd=request.POST.get('psw')
    if id.isdigit():
        doc=Doctor.objects.filter(d_id=id,password=pswd)
        if(doc):
            cursor=connection.cursor()
            response=medalloc(request,cursor,id)
            response.set_cookie('docid',id)
            return response
        else:
            return render(request,"7_doctor_login.html",{"incorect":True})
    return render(request,"7_doctor_login.html",{"incorect":True})

def receptionist_login(request):
    return render(request,"8_receptionist_login.html")

def receptionist_login1(request):
    id=request.POST.get('uname')
    pswd=request.POST.get('psw')
    if id.isdigit():
        doc=Recptionalist.objects.filter(r_id=id,password=pswd)
        if(doc):
            response=render(request,"receptionist_options.html")
            response.set_cookie('recid',id)
            return response
        else:
            return render(request,"8_receptionist_login.html",{"incorect":True})
    return render(request,"8_receptionist_login.html",{"incorect":True})

def patient_interface(request):
    return render(request,"9_patient_interface.html")

def ward_receptionalist_interface(request):
    cursor=connection.cursor()
    id=request.COOKIES.get('recid')
    if is_ajax(request):
        patid=request.GET.get("patientid")
        wardid=request.GET.get("wardid")

        #If none option is choosed ward_id for the patient selcted will set to null
        if wardid=="None":
            #cursor.execute('UPDATE covidmgmt_patient SET ward_id=null where p_id='+patid)
            obj=Patient.objects.get(p_id=patid)
            obj.ward=None
            obj.save()
            return wardalloc(request,cursor,id,bed=False)
        
        #getting no of beds in selected ward_id
        obj=Ward.objects.get(ward_id=wardid)
        count=obj.no_of_beds

        #getting no of beds alloted for only active cases
        alloted=Patient.objects.filter(ward=wardid,status='Active').count()

        #cheaking if beds are avilable for selcted wardid
        if(alloted<count):
            #cursor.execute('UPDATE covidmgmt_patient SET ward_id='+wardid+' where p_id='+patid)
            obj=Patient.objects.get(p_id=patid)
            obj.ward=wardid
            obj.save()
            return wardalloc(request,cursor,id,bed=False)
        else:
            print("Not allowed")
            return wardalloc(request,cursor,id,bed=True)
    else:
        return wardalloc(request,cursor,id,bed=False)
   
def service_receptionalist_interface(request):
    cursor=connection.cursor()
    id=request.COOKIES.get('recid')
    if is_ajax(request):
        patid=request.GET.get("patientid")
        serid=request.GET.get("serid")
        if serid=="None":
            Avails.objects.filter(p_id=patid).delete()
            return servicealloc(request,cursor,id)
            
        else:
            try:
                avail=Avails(p_id=patid,service_id=serid)
                avail.save()
                return servicealloc(request,cursor,id)
            except:
                print("Duplicates are Not allowed")
                return servicealloc(request,cursor,id)
    else:
        return servicealloc(request,cursor,id)

def doc_receptionalist_interface(request):
    cursor=connection.cursor()
    id=request.COOKIES.get('recid')
    if is_ajax(request):
        patid=request.GET.get("patientid")
        docid=request.GET.get("docid")
        if docid=="None":
            Treats.objects.filter(p_id=patid).delete()
            return wardalloc(request,cursor,id,bed=False)
            
        else:
            try:
                Treats(p_id=patid,d_id=docid).save()
                return wardalloc(request,cursor,id,bed=False)
            except:
                print("Duplicates Not Allowed")
                return wardalloc(request,cursor,id,bed=False)
    else:
        return wardalloc(request,cursor,id,bed=False)

def Doctor_interface(request):
    cursor=connection.cursor()
    patid=request.GET.get("patientid")
    medid=request.GET.get("medid")
    id=request.COOKIES.get('docid')
    if medid=="None":
        Prescribed_to.objects.filter(p_id=patid).delete()
        return medalloc(request,cursor,id)
            
    else:
        try:
            Prescribed_to(p_id=patid,m_id=medid).save()
            return medalloc(request,cursor,id)
        except:
            print("duplicates are not allowed")
            return medalloc(request,cursor,id)
    
def StatusPatient(request):
    patid=request.GET.get("patientid")
    status=request.GET.get("status")
    id=request.COOKIES.get('docid')
    cursor=connection.cursor()
    if(status=="Inactive"):
        date=time.strftime("%Y-%m-%d %H:%M:%S")
        obj=Patient.objects.get(p_id=patid)
        obj.status=status
        obj.Date_of_Discharge=date
        obj.save()
    if(status=="Active"):
        print(status)
        date=time.strftime("%Y-%m-%d %H:%M:%S")
        obj=Patient.objects.get(p_id=patid)
        obj.ward=None
        obj.status=status
        obj.Date_of_Discharge=None 
        obj.Date_of_Admit=date
        obj.save()
    return medalloc(request,cursor,id)

#ajax cheaking function
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


#fetching functions
def wardalloc(request,cursor,id,bed):
    #getting logged in recptionalist name
    resp=Recptionalist.objects.get(r_id=id)
    respname=resp.name
    
    results=[[i.p_id,i.first_name,i.last_name,i.ward,i.phone_no,i.discription,None,i.status,i.Date_of_Admit] for i in Patient.objects.all()]
    for i in results:
        try:
            i[3]=Ward.objects.get(ward_id=i[3]).ward_type
        except:
            pass
        doc_id_list=[k.d_id for k in tuple(Treats.objects.filter(p_id=i[0]))]
        i[6]=",".join([k.name for k in [Doctor.objects.filter(d_id=z)[0] for z in doc_id_list]])
        i=tuple(i)

    ward=[(i.ward_id,i.ward_type) for i in Ward.objects.all()]
    doctor=[(i.d_id,i.name) for i in Doctor.objects.all()]
            
    return render(request,"10_ward_receptionalist_interface.html",{"reception":results,"ward":ward,"doctor":doctor,"bed":bed,"name":respname})

def servicealloc(request,cursor,id):
    #getting logged in recptionalist name
    resp=Recptionalist.objects.get(r_id=id)
    respname=resp.name

    results=[[i.p_id,i.first_name,i.last_name,None,i.phone_no,i.discription,i.address,i.status,i.Date_of_Admit] for i in Patient.objects.all()]
    service=[(i.ser_id,i.ser_name) for i in Service.objects.all()]

    for i in results:
        ser_id_list=[k.service_id for k in Avails.objects.filter(p_id=i[0])]
        i[3]=",".join([z.ser_name for z in (Service.objects.filter(ser_id=k)[0] for k in ser_id_list)])
        i=tuple(i)

            
    return render(request,"10_service_receptionalist_interface.html",{"reception":results,"service":service,"name":respname})

def medalloc(request,cursor,id):
    doctor=Doctor.objects.get(d_id=id)
    name=doctor.name
    patient_ids=[i.p_id for i in Treats.objects.filter(d_id=id)]
    result=[]
    for i in patient_ids:
        obj=Patient.objects.get(p_id=i)
        med_id_list=[k.m_id for k in Prescribed_to.objects.filter(p_id=i)]
        med_names=",".join([z.med_name for z in (Medicine.objects.filter(m_id=k)[0] for k in med_id_list)])
        result.append((obj.p_id,obj.first_name,obj.last_name,obj.discription,obj.phone_no,med_names,obj.status))

    medicines=Medicine.objects.all()
    return render(request,"11_Doctor_interface.html",{"result":result,"medicines":medicines,"name":name})

def patientresult(request,cursor,id):
    patient_ob=Patient.objects.filter(p_id=id)[0]
    name=patient_ob.first_name+" "+patient_ob.last_name
    try:
        ward_id1=patient_ob.ward
        ward_type=Ward.objects.filter(ward_id=ward_id1)[0].ward_type
        ward_price=Ward.objects.filter(ward_id=ward_id1)[0].price
    except:
        ward_type=None
        ward_price=0

    doc_id_list=[i.d_id for i in tuple(Treats.objects.filter(p_id=id))]
    doc_name=",".join([i.name for i in [Doctor.objects.filter(d_id=k)[0] for k in doc_id_list]])
    doc_phone=",".join([str(i.phone_no) for i in [Doctor.objects.filter(d_id=k)[0] for k in doc_id_list]])

    ser_id_list=[i.service_id for i in Avails.objects.filter(p_id=id)]
    ser_name=",".join([i.ser_name for i in (Service.objects.filter(ser_id=k)[0] for k in ser_id_list)])
    ser_price_list=[i.price for i in (Service.objects.filter(ser_id=k)[0] for k in ser_id_list)]

    med_id_list=[i.m_id for i in Prescribed_to.objects.filter(p_id=id)]
    med_name=",".join([i.med_name for i in (Medicine.objects.filter(m_id=k)[0] for k in med_id_list)])
    
    totalprice=0
    totalprice=ward_price+sum(ser_price_list)
    result=[(id,patient_ob.first_name,patient_ob.last_name,doc_name,doc_phone,ward_type,ser_name,med_name,patient_ob.status,ward_price,sum(ser_price_list))]

    return render(request,"9_patient_interface.html",{"result":result,"sum":totalprice,"name":name})