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
            cursor.execute('UPDATE covidmgmt_patient SET ward_id=null where p_id='+patid)
            return wardalloc(request,cursor,id,bed=False)
        
        #getting no of beds in selected ward_id
        obj=Ward.objects.get(ward_id=wardid)
        count=obj.no_of_beds

        #getting no of beds alloted for only active cases
        alloted=Patient.objects.filter(ward=wardid,status='Active').count()

        #cheaking if beds are avilable for selcted wardid
        if(alloted<count):
            cursor.execute('UPDATE covidmgmt_patient SET ward_id='+wardid+' where p_id='+patid)
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
            cursor.execute('DELETE FROM covidmgmt_avails WHERE p_id='+patid)
            return servicealloc(request,cursor,id)
            
        else:
            try:
                cursor.execute('INSERT INTO covidmgmt_avails (p_id,service_id) VALUES('+ patid +','+ serid +')')
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
            cursor.execute('DELETE FROM covidmgmt_treats WHERE p_id='+patid)
            return wardalloc(request,cursor,id,bed=False)
            
        else:
            #print(patid,wardid)
            #cursor.execute('DELETE FROM covidmgmt_treats WHERE p_id='+patid) #deleting the existing
            try:
                cursor.execute('INSERT INTO covidmgmt_treats (p_id,d_id) VALUES('+ patid +','+ docid +')')
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
        cursor.execute('DELETE FROM covidmgmt_prescribed_to WHERE p_id='+patid)
        return medalloc(request,cursor,id)
            
    else:
        try:
            cursor.execute('INSERT INTO covidmgmt_prescribed_to (p_id,m_id) VALUES('+ patid +','+ medid +')')
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


    #getting ward and service assigned for a patient
    cursor.execute('''SELECT mt.pid,mt.fname,mt.lname,ch1.ward_type as ward,mt.phno,mt.discript,GROUP_CONCAT(ch2.name),mt.stat,mt.dateadmit as doctors FROM
                    (SELECT p.p_id as pid,p.first_name as fname,p.last_name as lname,p.ward_id as wid,p.phone_no as phno,p.discription as discript,t.d_id as did, p.status as stat,p.Date_of_Admit as dateadmit
                    FROM covidmgmt_patient as p LEFT OUTER JOIN covidmgmt_treats as t
                    on t.p_id=p.p_id) as mt LEFT OUTER JOIN covidmgmt_ward as ch1 ON mt.wid= ch1.ward_id  LEFT OUTER JOIN covidmgmt_doctor as ch2 ON ch2.d_id=mt.did
                    GROUP BY mt.pid
                    ORDER BY mt.stat;''')
    results=cursor.fetchall()

    #getting ward id and ward name
    cursor.execute("SELECT ward_id,ward_type FROM covidmgmt_ward")
    ward=cursor.fetchall()
    #getting doctor id and doctor name
    cursor.execute("SELECT d_id,name FROM covidmgmt_doctor")
    doctor=cursor.fetchall()
            
    return render(request,"10_ward_receptionalist_interface.html",{"reception":results,"ward":ward,"doctor":doctor,"bed":bed,"name":respname})

def servicealloc(request,cursor,id):
    #getting logged in recptionalist name
    resp=Recptionalist.objects.get(r_id=id)
    respname=resp.name

    #getting ward and service assigned for a patient
    cursor.execute('''SELECT mt.pid,mt.fname,mt.lname,GROUP_CONCAT(ct.ser_name) as servicnames,mt.phno,mt.descrip,mt.address,mt.stat,mt.dateadmit FROM (SELECT p.p_id as pid,p.first_name as fname,p.last_name as lname,a.service_id as serid,p.phone_no as phno,p.discription as descrip,p.address as address,p.status as stat,p.Date_of_Admit as dateadmit
                    FROM covidmgmt_patient as p LEFT OUTER JOIN covidmgmt_avails as a ON p.p_id = a.p_id ) as mt LEFT OUTER JOIN covidmgmt_service ct ON mt.serid=ct.ser_id
                    GROUP by mt.pid
                    ORDER BY mt.stat;''')
    results=cursor.fetchall()
    #getting all the services
    cursor.execute("SELECT ser_id,ser_name FROM covidmgmt_service")
    service=cursor.fetchall()
            
    return render(request,"10_service_receptionalist_interface.html",{"reception":results,"service":service,"name":respname})

def medalloc(request,cursor,id):
    doctor=Doctor.objects.get(d_id=id)
    name=doctor.name
    cursor.execute('''SELECT mt.pid,mt.fname,mt.lname,mt.discript,mt.phno,GROUP_CONCAT(ch.med_name) as med,mt.stat 
                    FROM (SELECT p.p_id as pid,p.first_name as fname,p.last_name as lname,w.m_id as mid,p.phone_no as phno,p.discription as discript,p.status as stat
                    FROM covidmgmt_patient as p LEFT OUTER JOIN covidmgmt_prescribed_to as w ON p.p_id = w.p_id) as mt LEFT OUTER JOIN covidmgmt_medicine as ch ON ch.m_id=mt.mid JOIN covidmgmt_treats t ON 			  mt.pid=t.p_id
                    WHERE t.d_id='''+id+'''
                    GROUP BY mt.pid
                    ORDER BY mt.stat;
                    ''')
    result=cursor.fetchall()

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