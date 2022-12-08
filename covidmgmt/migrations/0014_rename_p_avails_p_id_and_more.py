# Generated by Django 4.1.3 on 2022-12-08 12:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('covidmgmt', '0013_alter_avails_p_alter_avails_service_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='avails',
            old_name='p',
            new_name='p_id',
        ),
        migrations.RenameField(
            model_name='avails',
            old_name='service',
            new_name='service_id',
        ),
        migrations.RenameField(
            model_name='prescribed_to',
            old_name='m',
            new_name='m_id',
        ),
        migrations.RenameField(
            model_name='prescribed_to',
            old_name='p',
            new_name='p_id',
        ),
        migrations.RenameField(
            model_name='treats',
            old_name='d',
            new_name='d_id',
        ),
        migrations.RenameField(
            model_name='treats',
            old_name='p',
            new_name='p_id',
        ),
        migrations.AlterUniqueTogether(
            name='avails',
            unique_together={('p_id', 'service_id')},
        ),
        migrations.AlterUniqueTogether(
            name='prescribed_to',
            unique_together={('m_id', 'p_id')},
        ),
        migrations.AlterUniqueTogether(
            name='treats',
            unique_together={('d_id', 'p_id')},
        ),
    ]
