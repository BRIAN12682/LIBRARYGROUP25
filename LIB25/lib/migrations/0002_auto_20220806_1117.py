# Generated by Django 3.1.8 on 2022-08-06 08:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lib', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='request',
            old_name='student',
            new_name='user',
        ),
    ]