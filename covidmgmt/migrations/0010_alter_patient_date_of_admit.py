# Generated by Django 4.0 on 2022-01-14 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('covidmgmt', '0009_patient_date_of_admit_patient_date_of_discharge_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='Date_of_Admit',
            field=models.DateTimeField(),
        ),
    ]