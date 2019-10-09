# Generated by Django 2.1 on 2019-10-09 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0015_auto_20191009_1116'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='courserelease',
            options={'get_latest_by': ['course__history_date', 'version'], 'ordering': ['-course__history_date', 'version']},
        ),
        migrations.AddField(
            model_name='course',
            name='graduate_course_flag',
            field=models.BooleanField(default=False, verbose_name='Is Graduate Course?'),
        ),
        migrations.AddField(
            model_name='historicalcourse',
            name='graduate_course_flag',
            field=models.BooleanField(default=False, verbose_name='Is Graduate Course?'),
        ),
    ]
