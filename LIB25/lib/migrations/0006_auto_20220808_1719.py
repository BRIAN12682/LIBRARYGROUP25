# Generated by Django 3.1.8 on 2022-08-08 14:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lib', '0005_auto_20220808_1714'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='lib.books'),
        ),
    ]