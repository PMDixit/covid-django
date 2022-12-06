from django.contrib import admin
from covidmgmt.models import *

admin.site.site_header='PSPP COVID MANAGEMENT ADMIN'

# Register your models here.
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('d_id','name','phone_no')
    ordering = ('name',)
    search_fields = ('name', 'phone_no','d_id')
    list_filter=('gender',)
admin.site.register(Doctor,DoctorAdmin)


class PatientAdmin(admin.ModelAdmin):
    list_display = ('p_id','first_name','last_name','phone_no','Date_of_Admit','status')
    ordering = ('first_name','last_name')
    search_fields = ('first_name', 'phone_no')
    list_filter=('Date_of_Admit','Date_of_Discharge','gender','status','ward')
admin.site.register(Patient,PatientAdmin)

class RecAdmin(admin.ModelAdmin):
    list_display = ('r_id','name','password')
    ordering = ('name',)
    search_fields = ('name',)

admin.site.register(Recptionalist,RecAdmin)

class MedAdmin(admin.ModelAdmin):
    list_display = ('m_id','med_name')
    ordering = ('m_id',)
    search_fields = ('m_id','med_name')
admin.site.register(Medicine,MedAdmin)

class WardAdmin(admin.ModelAdmin):
    list_display = ('ward_id','ward_type','no_of_beds','price')
    ordering = ('ward_id',)
    search_fields = ('ward_id','ward_type','no_of_beds','price')
admin.site.register(Ward,WardAdmin)

class SerAdmin(admin.ModelAdmin):
    list_display = ('ser_id','ser_name','price')
    ordering = ('ser_id',)
    search_fields = ('ser_name','ser_id','price')
admin.site.register(Service,SerAdmin)

class AvailAdmin(admin.ModelAdmin):
    list_display = ('p','service')
    ordering = ('p',)
    search_fields = ('p','service')
admin.site.register(Avails,AvailAdmin)

class PrescAdmin(admin.ModelAdmin):
    list_display = ('m','p')
    ordering = ('m',)
    search_fields = ('m','p')
admin.site.register(Prescribed_to,PrescAdmin)

class TreatAdmin(admin.ModelAdmin):
    list_display = ('d','p')
    ordering = ('d',)
    search_fields = ('d','p')
admin.site.register(Treats,TreatAdmin)