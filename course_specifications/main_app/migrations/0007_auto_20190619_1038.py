# Generated by Django 2.1 on 2019-06-19 07:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_auto_20190617_1116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='faculty_staff_availability',
            field=models.TextField(blank=True, help_text='Arrangements for availability of faculty and teaching staff for individual student consultations and academic advice', null=True, verbose_name='Faculty and Teaching Staff Availability'),
        ),
        migrations.AlterField(
            model_name='course',
            name='lab_contact_hours',
            field=models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)], verbose_name='Lab Contact Hours'),
        ),
        migrations.AlterField(
            model_name='course',
            name='lecture_credit_hours',
            field=models.PositiveSmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)], verbose_name='Lecture Credit Hours'),
        ),
        migrations.AlterField(
            model_name='course',
            name='total_credit_hours',
            field=models.PositiveSmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)], verbose_name='Total Credit Hours'),
        ),
        migrations.AlterField(
            model_name='historicalcourse',
            name='faculty_staff_availability',
            field=models.TextField(blank=True, help_text='Arrangements for availability of faculty and teaching staff for individual student consultations and academic advice', null=True, verbose_name='Faculty and Teaching Staff Availability'),
        ),
        migrations.AlterField(
            model_name='historicalcourse',
            name='lab_contact_hours',
            field=models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)], verbose_name='Lab Contact Hours'),
        ),
        migrations.AlterField(
            model_name='historicalcourse',
            name='lecture_credit_hours',
            field=models.PositiveSmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)], verbose_name='Lecture Credit Hours'),
        ),
        migrations.AlterField(
            model_name='historicalcourse',
            name='total_credit_hours',
            field=models.PositiveSmallIntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)], verbose_name='Total Credit Hours'),
        ),
    ]
