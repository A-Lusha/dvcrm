# Generated by Django 4.0 on 2022-03-11 21:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lead', '0002_rename_contact_person_lead_contact_first_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lead',
            old_name='business_name',
            new_name='company_name',
        ),
    ]
