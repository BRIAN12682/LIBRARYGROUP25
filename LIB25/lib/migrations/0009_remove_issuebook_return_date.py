# Generated by Django 3.1.8 on 2022-08-25 07:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lib', '0008_auto_20220825_1056'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='issuebook',
            name='return_date',
        ),
    ]
