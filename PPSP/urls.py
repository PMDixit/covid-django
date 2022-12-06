"""PPSP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from covidmgmt.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/',Home,name='index'),
    path('about_us/',about_us,name='aboutus'),
    path('Find_Doctor/',Find_Doctor,name='finddoctor'),
    path('Medical_Services/',Medical_Services,name='medicalservices'),
    path('Ward_Details/',Ward_Details),
    path('registration_patient/',registration_patient),
    path('registration_patient_submit/',registration_patient_submit),
    path('allloginpage/',allloginpage),
    path('patient_login/',patient_login),
    path('patient_login1/',patient_login1),
    path('doctor_login/',doctor_login),
    path('doctor_login1/',doctor_login1),
    path('receptionist_login/',receptionist_login),
    path('receptionist_login1/',receptionist_login1),
    path('patient_interface/',patient_interface),
    path('ward_receptionalist_interface/',ward_receptionalist_interface),
    path('service_receptionalist_interface/',service_receptionalist_interface),
    path('doc_receptionalist_interface/',doc_receptionalist_interface),
    path('Doctor_interface/',Doctor_interface),
    path('StatusPatient/',StatusPatient),
]

