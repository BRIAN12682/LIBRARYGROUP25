# Generated by Django 4.0.6 on 2022-08-09 03:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lib', '0006_auto_20220808_1719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='area',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='books',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='chatmessages',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='finedstudents',
            name='Issued_book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Issued_book+', to='lib.issuebook'),
        ),
        migrations.AlterField(
            model_name='finedstudents',
            name='Issuing_date',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Issuing_date+', to='lib.issuebook'),
        ),
        migrations.AlterField(
            model_name='finedstudents',
            name='book_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='book_to+', to='lib.issuebook'),
        ),
        migrations.AlterField(
            model_name='finedstudents',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='issuebook',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='request',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='students',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='subarea',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.DeleteModel(
            name='IssuedBook',
        ),
    ]