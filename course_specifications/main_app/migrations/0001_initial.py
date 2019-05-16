# Generated by Django 2.1 on 2019-05-16 11:14

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AssessmentTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('lecture', 'Lecture'), ('lab', 'Laboratory')], max_length=50, null=True, verbose_name='Type')),
                ('assessment_task', models.CharField(help_text='e.g essay, test, group project, examination, speech, etc...', max_length=2000, null=True, verbose_name='Assessment Task')),
                ('week_due', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Week Due')),
                ('weight_percentage', models.DecimalField(decimal_places=4, max_digits=10, null=True, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0.1)], verbose_name='Weight Percentage')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mother_department', models.CharField(max_length=500, null=True, verbose_name='Mother Department')),
                ('program_code', models.CharField(max_length=10, null=True, verbose_name='Program Code')),
                ('number', models.CharField(max_length=10, null=True, verbose_name='Number')),
                ('title', models.CharField(max_length=500, null=True, verbose_name='Title')),
                ('catalog_description', models.TextField(help_text='General description about the course and topics covered', null=True, verbose_name='Catalog Description')),
                ('location', models.CharField(choices=[('main_campus', 'Main Campus'), ('dcc', 'Dammam Community College (DCC)'), ('other', 'Other')], max_length=50, null=True, verbose_name='Location')),
                ('lecture_credit_hours', models.PositiveSmallIntegerField(null=True, verbose_name='Lecture Credit Hours')),
                ('lab_contact_hours', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Lab Contact Hours')),
                ('total_credit_hours', models.PositiveSmallIntegerField(null=True, verbose_name='Total Credit Hours')),
                ('weekly_office_hours', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Weekly Office Hours')),
                ('mode_of_instruction_in_class', models.DecimalField(decimal_places=4, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0.1), django.core.validators.MaxValueValidator(100)], verbose_name='Mode Of Instruction (In-Class) %')),
                ('mode_of_instruction_other', models.DecimalField(decimal_places=4, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0.1), django.core.validators.MaxValueValidator(100)], verbose_name='Mode Of Instruction (Other) %')),
                ('mode_of_instruction_other_desc', models.CharField(blank=True, max_length=100, null=True, verbose_name='Mode Of Instruction (Other) Description')),
                ('mode_of_instruction_comments', models.TextField(null=True, verbose_name='Mode Of Instruction Comments')),
                ('self_study_lecture', models.DecimalField(decimal_places=4, max_digits=10, null=True, verbose_name='Self-Study Lecture Hours')),
                ('self_study_lab', models.DecimalField(decimal_places=4, max_digits=10, null=True, verbose_name='Self-Study Laboratory Hours')),
                ('self_study_tutorial', models.DecimalField(decimal_places=4, max_digits=10, null=True, verbose_name='Self-Study Tutorial Hours')),
                ('self_study_practical', models.DecimalField(decimal_places=4, max_digits=10, null=True, verbose_name='Self-Study Practical Hours')),
                ('self_study_other', models.DecimalField(decimal_places=4, max_digits=10, null=True, verbose_name='Self-Study Other Hours')),
                ('engineering_credit_hours', models.DecimalField(decimal_places=4, max_digits=10, null=True, verbose_name='Engineering Credit Hours')),
                ('math_science_credit_hours', models.DecimalField(decimal_places=4, max_digits=10, null=True, verbose_name='Mathematics/Science Credit Hours')),
                ('humanities_credit_hours', models.DecimalField(decimal_places=4, max_digits=10, null=True, verbose_name='Humanities Credit Hours')),
                ('social_sciences_credit_hours', models.DecimalField(decimal_places=4, max_digits=10, null=True, verbose_name='Social Sciences Credit Hours')),
                ('general_education_credit_hours', models.DecimalField(decimal_places=4, max_digits=10, null=True, verbose_name='General Education Credit Hours')),
                ('other_subject_areas_credit_hours', models.DecimalField(decimal_places=4, max_digits=10, null=True, verbose_name='Other Subject Areas Credit Hours')),
                ('required_textbooks_from_sierra', models.CharField(help_text='List of required textbooks from Sierra system', max_length=1000, null=True, verbose_name='required_textbooks')),
                ('other_required_textbooks', models.TextField(blank=True, help_text='List other required textbooks that are not available in Sierra system. You should mention the book title, ISBN, edition and publisher', null=True, verbose_name='Other Required Textbooks')),
                ('essential_reference_materials', models.TextField(blank=True, help_text='journals, reports, etc...', null=True, verbose_name='Essential Reference Materials')),
                ('recommended_textbooks_reference_materials', models.TextField(blank=True, help_text='journals, reports, etc...', null=True, verbose_name='Recommended Textbooks and Reference Materials')),
                ('electronic_materials', models.TextField(blank=True, help_text='websites, facebook, twitter, etc...', null=True, verbose_name='Electronic Materials')),
                ('other_materials', models.TextField(blank=True, help_text='Computer-based programs/CD, professional standards or regulations and software', null=True, verbose_name='Other Learning Materials')),
                ('strategies_of_student_feedback_and_evaluation', models.TextField(help_text='e.g. face-to-face meetings, student in-class evaluation, student survey, focus groups, etc...', null=True, verbose_name='Strategies for obtaining Students Feedback and Evaluation')),
                ('other_course_evaluation_methods', models.TextField(blank=True, help_text='e.g. by faculty, program leaders, peer reviewer', null=True, verbose_name='Other Course Evaluation Methods')),
                ('faculty_staff_availability', models.TextField(blank=True, null=True, verbose_name='Faculty and Teaching Staff Availability')),
                ('corequisite_courses', models.ManyToManyField(blank=True, related_name='corequisite_for', to='main_app.Course')),
                ('prerequisite_courses', models.ManyToManyField(blank=True, related_name='prerequisite_for', to='main_app.Course')),
            ],
        ),
        migrations.CreateModel(
            name='CourseLearningOutcome',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clo_category', models.CharField(choices=[('knowledge', 'Knowledge'), ('skills', 'Skills'), ('competence', 'Competence')], max_length=50, null=True, verbose_name='Category')),
                ('learning_outcome', models.CharField(max_length=2000, null=True, verbose_name='Learning Outcome')),
                ('teaching_strategy', models.CharField(max_length=2000, null=True, verbose_name='Teaching Strategy')),
                ('assessment_method', models.CharField(max_length=2000, null=True, verbose_name='Assessment Method')),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='learning_outcomes', to='main_app.Course', verbose_name='Course')),
            ],
        ),
        migrations.CreateModel(
            name='CourseRelease',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.PositiveIntegerField(default=1, verbose_name='version')),
            ],
        ),
        migrations.CreateModel(
            name='FacilitiesRequired',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('accommodation', 'Accommodation'), ('technology_resources', 'Technology Resources'), ('other', 'Other')], max_length=50, null=True, verbose_name='Type')),
                ('facility_required', models.CharField(help_text='e.g. classrooms and laboratories', max_length=2000, null=True, verbose_name='Facility Required')),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='facilities_required', to='main_app.Course', verbose_name='Course')),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalAssessmentTask',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('type', models.CharField(choices=[('lecture', 'Lecture'), ('lab', 'Laboratory')], max_length=50, null=True, verbose_name='Type')),
                ('assessment_task', models.CharField(help_text='e.g essay, test, group project, examination, speech, etc...', max_length=2000, null=True, verbose_name='Assessment Task')),
                ('week_due', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Week Due')),
                ('weight_percentage', models.DecimalField(decimal_places=4, max_digits=10, null=True, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0.1)], verbose_name='Weight Percentage')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('course', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='main_app.Course', verbose_name='Course')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'get_latest_by': 'history_date',
                'ordering': ('-history_date', '-history_id'),
                'verbose_name': 'historical assessment task',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalCourse',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('mother_department', models.CharField(max_length=500, null=True, verbose_name='Mother Department')),
                ('program_code', models.CharField(max_length=10, null=True, verbose_name='Program Code')),
                ('number', models.CharField(max_length=10, null=True, verbose_name='Number')),
                ('title', models.CharField(max_length=500, null=True, verbose_name='Title')),
                ('catalog_description', models.TextField(help_text='General description about the course and topics covered', null=True, verbose_name='Catalog Description')),
                ('location', models.CharField(choices=[('main_campus', 'Main Campus'), ('dcc', 'Dammam Community College (DCC)'), ('other', 'Other')], max_length=50, null=True, verbose_name='Location')),
                ('lecture_credit_hours', models.PositiveSmallIntegerField(null=True, verbose_name='Lecture Credit Hours')),
                ('lab_contact_hours', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Lab Contact Hours')),
                ('total_credit_hours', models.PositiveSmallIntegerField(null=True, verbose_name='Total Credit Hours')),
                ('weekly_office_hours', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Weekly Office Hours')),
                ('mode_of_instruction_in_class', models.DecimalField(decimal_places=4, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0.1), django.core.validators.MaxValueValidator(100)], verbose_name='Mode Of Instruction (In-Class) %')),
                ('mode_of_instruction_other', models.DecimalField(decimal_places=4, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0.1), django.core.validators.MaxValueValidator(100)], verbose_name='Mode Of Instruction (Other) %')),
                ('mode_of_instruction_other_desc', models.CharField(blank=True, max_length=100, null=True, verbose_name='Mode Of Instruction (Other) Description')),
                ('mode_of_instruction_comments', models.TextField(null=True, verbose_name='Mode Of Instruction Comments')),
                ('self_study_lecture', models.DecimalField(decimal_places=4, max_digits=10, null=True, verbose_name='Self-Study Lecture Hours')),
                ('self_study_lab', models.DecimalField(decimal_places=4, max_digits=10, null=True, verbose_name='Self-Study Laboratory Hours')),
                ('self_study_tutorial', models.DecimalField(decimal_places=4, max_digits=10, null=True, verbose_name='Self-Study Tutorial Hours')),
                ('self_study_practical', models.DecimalField(decimal_places=4, max_digits=10, null=True, verbose_name='Self-Study Practical Hours')),
                ('self_study_other', models.DecimalField(decimal_places=4, max_digits=10, null=True, verbose_name='Self-Study Other Hours')),
                ('engineering_credit_hours', models.DecimalField(decimal_places=4, max_digits=10, null=True, verbose_name='Engineering Credit Hours')),
                ('math_science_credit_hours', models.DecimalField(decimal_places=4, max_digits=10, null=True, verbose_name='Mathematics/Science Credit Hours')),
                ('humanities_credit_hours', models.DecimalField(decimal_places=4, max_digits=10, null=True, verbose_name='Humanities Credit Hours')),
                ('social_sciences_credit_hours', models.DecimalField(decimal_places=4, max_digits=10, null=True, verbose_name='Social Sciences Credit Hours')),
                ('general_education_credit_hours', models.DecimalField(decimal_places=4, max_digits=10, null=True, verbose_name='General Education Credit Hours')),
                ('other_subject_areas_credit_hours', models.DecimalField(decimal_places=4, max_digits=10, null=True, verbose_name='Other Subject Areas Credit Hours')),
                ('required_textbooks_from_sierra', models.CharField(help_text='List of required textbooks from Sierra system', max_length=1000, null=True, verbose_name='required_textbooks')),
                ('other_required_textbooks', models.TextField(blank=True, help_text='List other required textbooks that are not available in Sierra system. You should mention the book title, ISBN, edition and publisher', null=True, verbose_name='Other Required Textbooks')),
                ('essential_reference_materials', models.TextField(blank=True, help_text='journals, reports, etc...', null=True, verbose_name='Essential Reference Materials')),
                ('recommended_textbooks_reference_materials', models.TextField(blank=True, help_text='journals, reports, etc...', null=True, verbose_name='Recommended Textbooks and Reference Materials')),
                ('electronic_materials', models.TextField(blank=True, help_text='websites, facebook, twitter, etc...', null=True, verbose_name='Electronic Materials')),
                ('other_materials', models.TextField(blank=True, help_text='Computer-based programs/CD, professional standards or regulations and software', null=True, verbose_name='Other Learning Materials')),
                ('strategies_of_student_feedback_and_evaluation', models.TextField(help_text='e.g. face-to-face meetings, student in-class evaluation, student survey, focus groups, etc...', null=True, verbose_name='Strategies for obtaining Students Feedback and Evaluation')),
                ('other_course_evaluation_methods', models.TextField(blank=True, help_text='e.g. by faculty, program leaders, peer reviewer', null=True, verbose_name='Other Course Evaluation Methods')),
                ('faculty_staff_availability', models.TextField(blank=True, null=True, verbose_name='Faculty and Teaching Staff Availability')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'get_latest_by': 'history_date',
                'ordering': ('-history_date', '-history_id'),
                'verbose_name': 'historical course',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalCourseLearningOutcome',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('clo_category', models.CharField(choices=[('knowledge', 'Knowledge'), ('skills', 'Skills'), ('competence', 'Competence')], max_length=50, null=True, verbose_name='Category')),
                ('learning_outcome', models.CharField(max_length=2000, null=True, verbose_name='Learning Outcome')),
                ('teaching_strategy', models.CharField(max_length=2000, null=True, verbose_name='Teaching Strategy')),
                ('assessment_method', models.CharField(max_length=2000, null=True, verbose_name='Assessment Method')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('course', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='main_app.Course', verbose_name='Course')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'get_latest_by': 'history_date',
                'ordering': ('-history_date', '-history_id'),
                'verbose_name': 'historical course learning outcome',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalFacilitiesRequired',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('type', models.CharField(choices=[('accommodation', 'Accommodation'), ('technology_resources', 'Technology Resources'), ('other', 'Other')], max_length=50, null=True, verbose_name='Type')),
                ('facility_required', models.CharField(help_text='e.g. classrooms and laboratories', max_length=2000, null=True, verbose_name='Facility Required')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('course', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='main_app.Course', verbose_name='Course')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'get_latest_by': 'history_date',
                'ordering': ('-history_date', '-history_id'),
                'verbose_name': 'historical facilities required',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalLearningObjective',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('learning_objective', models.CharField(max_length=2000, verbose_name='Learning Objective')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('course', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='main_app.Course', verbose_name='Course')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'get_latest_by': 'history_date',
                'ordering': ('-history_date', '-history_id'),
                'verbose_name': 'historical learning objective',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalTopic',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('type', models.CharField(choices=[('lecture', 'Lecture'), ('lab', 'Laboratory'), ('tutorial', 'Tutorial'), ('practical', 'Practical'), ('other', 'Other')], max_length=50, null=True, verbose_name='Type')),
                ('topic', models.CharField(max_length=2000, null=True, verbose_name='Topic')),
                ('contact_hours', models.DecimalField(decimal_places=4, max_digits=10, null=True, verbose_name='Contact Hours')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('course', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='main_app.Course', verbose_name='Course')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'get_latest_by': 'history_date',
                'ordering': ('-history_date', '-history_id'),
                'verbose_name': 'historical topic',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='LearningObjective',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('learning_objective', models.CharField(max_length=2000, verbose_name='Learning Objective')),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='learning_objectives', to='main_app.Course', verbose_name='Course')),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('lecture', 'Lecture'), ('lab', 'Laboratory'), ('tutorial', 'Tutorial'), ('practical', 'Practical'), ('other', 'Other')], max_length=50, null=True, verbose_name='Type')),
                ('topic', models.CharField(max_length=2000, null=True, verbose_name='Topic')),
                ('contact_hours', models.DecimalField(decimal_places=4, max_digits=10, null=True, verbose_name='Contact Hours')),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='topics', to='main_app.Course', verbose_name='Course')),
                ('related_course_learning_outcomes', models.ManyToManyField(blank=True, related_name='covered_by_topics', to='main_app.CourseLearningOutcome')),
            ],
        ),
        migrations.AddField(
            model_name='courserelease',
            name='assessment_tasks',
            field=models.ManyToManyField(related_name='releases', to='main_app.HistoricalAssessmentTask'),
        ),
        migrations.AddField(
            model_name='courserelease',
            name='corequisite_courses',
            field=models.ManyToManyField(related_name='corequisite_for', to='main_app.HistoricalCourse'),
        ),
        migrations.AddField(
            model_name='courserelease',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='releases', to='main_app.HistoricalCourse', verbose_name='course'),
        ),
        migrations.AddField(
            model_name='courserelease',
            name='facilities_required',
            field=models.ManyToManyField(related_name='releases', to='main_app.HistoricalFacilitiesRequired'),
        ),
        migrations.AddField(
            model_name='courserelease',
            name='learning_objectives',
            field=models.ManyToManyField(related_name='releases', to='main_app.HistoricalLearningObjective'),
        ),
        migrations.AddField(
            model_name='courserelease',
            name='learning_outcomes',
            field=models.ManyToManyField(related_name='releases', to='main_app.HistoricalCourseLearningOutcome'),
        ),
        migrations.AddField(
            model_name='courserelease',
            name='prerequisite_courses',
            field=models.ManyToManyField(related_name='prerequisite_for', to='main_app.HistoricalCourse'),
        ),
        migrations.AddField(
            model_name='courserelease',
            name='topics',
            field=models.ManyToManyField(related_name='releases', to='main_app.HistoricalTopic'),
        ),
        migrations.AddField(
            model_name='assessmenttask',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assessment_tasks', to='main_app.Course', verbose_name='Course'),
        ),
        migrations.AlterUniqueTogether(
            name='courserelease',
            unique_together={('version', 'course')},
        ),
    ]
