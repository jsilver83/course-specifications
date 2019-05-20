from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from simple_history.models import HistoricalRecords


class Course(models.Model):
    class Locations:
        MAIN_CAMPUS = 'main_campus'
        DAMMAM_COMMUNITY_COLLEGE = 'dcc'
        OTHER = 'other'

        @classmethod
        def choices(cls):
            return (
                (cls.MAIN_CAMPUS, _('Main Campus')),
                (cls.DAMMAM_COMMUNITY_COLLEGE, _('Dammam Community College (DCC)')),
                (cls.OTHER, _('Other')),
            )

    mother_department = models.CharField(_('Mother Department'), max_length=500, null=True, blank=False)
    program_code = models.CharField(_('Program Code'), max_length=10, null=True, blank=False)
    number = models.CharField(_('Number'), max_length=10, null=True, blank=False)
    title = models.CharField(_('Title'), max_length=500, null=True, blank=False)
    catalog_description = models.TextField(_('Catalog Description'), null=True, blank=False,
                                           help_text=_('General description about the course and topics covered'))
    location = models.CharField(_('Location'), max_length=50, null=True, blank=False, choices=Locations.choices())
    lecture_credit_hours = models.PositiveSmallIntegerField(_('Lecture Credit Hours'), null=True, blank=False)
    lab_contact_hours = models.PositiveSmallIntegerField(_('Lab Contact Hours'), null=True, blank=True)
    total_credit_hours = models.PositiveSmallIntegerField(_('Total Credit Hours'), null=True, blank=False)
    weekly_office_hours = models.PositiveSmallIntegerField(_('Weekly Office Hours'), null=True, blank=True)

    prerequisite_courses = models.ManyToManyField('Course', blank=True, related_name='prerequisite_for')
    corequisite_courses = models.ManyToManyField('Course', blank=True, related_name='corequisite_for')

    mode_of_instruction_in_class = models.DecimalField(
        _('Mode Of Instruction (In-Class) %'),
        null=True,
        blank=False,
        max_digits=settings.MAX_DIGITS,
        decimal_places=settings.MAX_DECIMAL_POINT,
        validators=[
            MinValueValidator(0.1),
            MaxValueValidator(100),
        ],
    )
    mode_of_instruction_other = models.DecimalField(
        _('Mode Of Instruction (Other) %'),
        null=True,
        blank=False,
        max_digits=settings.MAX_DIGITS,
        decimal_places=settings.MAX_DECIMAL_POINT,
        validators=[
            MinValueValidator(0.1),
            MaxValueValidator(100),
        ],
    )
    mode_of_instruction_other_desc = models.CharField(_('Mode Of Instruction (Other) Description'),
                                                      max_length=100, null=True, blank=True)
    mode_of_instruction_comments = models.TextField(_('Mode Of Instruction Comments'), null=True, blank=False)

    self_study_lecture = models.DecimalField(
        _('Self-Study Lecture Hours'),
        null=True,
        blank=False,
        max_digits=settings.MAX_DIGITS,
        decimal_places=settings.MAX_DECIMAL_POINT
    )
    self_study_lab = models.DecimalField(
        _('Self-Study Laboratory Hours'),
        null=True,
        blank=False,
        max_digits=settings.MAX_DIGITS,
        decimal_places=settings.MAX_DECIMAL_POINT
    )
    self_study_tutorial = models.DecimalField(
        _('Self-Study Tutorial Hours'),
        null=True,
        blank=False,
        max_digits=settings.MAX_DIGITS,
        decimal_places=settings.MAX_DECIMAL_POINT
    )
    self_study_practical = models.DecimalField(
        _('Self-Study Practical Hours'),
        null=True,
        blank=False,
        max_digits=settings.MAX_DIGITS,
        decimal_places=settings.MAX_DECIMAL_POINT
    )
    self_study_other = models.DecimalField(
        _('Self-Study Other Hours'),
        null=True,
        blank=False,
        max_digits=settings.MAX_DIGITS,
        decimal_places=settings.MAX_DECIMAL_POINT
    )

    engineering_credit_hours = models.DecimalField(
        _('Engineering Credit Hours'),
        null=True,
        blank=False,
        max_digits=settings.MAX_DIGITS,
        decimal_places=settings.MAX_DECIMAL_POINT
    )
    math_science_credit_hours = models.DecimalField(
        _('Mathematics/Science Credit Hours'),
        null=True,
        blank=False,
        max_digits=settings.MAX_DIGITS,
        decimal_places=settings.MAX_DECIMAL_POINT
    )
    humanities_credit_hours = models.DecimalField(
        _('Humanities Credit Hours'),
        null=True,
        blank=False,
        max_digits=settings.MAX_DIGITS,
        decimal_places=settings.MAX_DECIMAL_POINT
    )
    social_sciences_credit_hours = models.DecimalField(
        _('Social Sciences Credit Hours'),
        null=True,
        blank=False,
        max_digits=settings.MAX_DIGITS,
        decimal_places=settings.MAX_DECIMAL_POINT
    )
    general_education_credit_hours = models.DecimalField(
        _('General Education Credit Hours'),
        null=True,
        blank=False,
        max_digits=settings.MAX_DIGITS,
        decimal_places=settings.MAX_DECIMAL_POINT
    )
    other_subject_areas_credit_hours = models.DecimalField(
        _('Other Subject Areas Credit Hours'),
        null=True,
        blank=False,
        max_digits=settings.MAX_DIGITS,
        decimal_places=settings.MAX_DECIMAL_POINT
    )

    required_textbooks_from_sierra = models.CharField(
        max_length=1000, verbose_name=_('required_textbooks'),
        help_text=_('List of required textbooks from Sierra system'), null=True, blank=False,
    )

    other_required_textbooks = models.TextField(
        _('Other Required Textbooks'), null=True, blank=True,
        help_text=_('List other required textbooks that are not available in Sierra system. You should mention the '
                    'book title, ISBN, edition and publisher')
    )

    essential_reference_materials = models.TextField(_('Essential Reference Materials'), null=True, blank=True,
                                                     help_text=_('journals, reports, etc...'))
    recommended_textbooks_reference_materials = models.TextField(_('Recommended Textbooks and Reference Materials'),
                                                                 null=True, blank=True,
                                                                 help_text=_('journals, reports, etc...'))
    electronic_materials = models.TextField(_('Electronic Materials'), null=True, blank=True,
                                            help_text=_('websites, facebook, twitter, etc...'))
    other_materials = models.TextField(
        _('Other Learning Materials'), null=True, blank=True,
        help_text=_('Computer-based programs/CD, professional standards or regulations and software')
    )

    strategies_of_student_feedback_and_evaluation = models.TextField(
        _('Strategies for obtaining Students Feedback and Evaluation'), null=True, blank=False,
        help_text=_('e.g. face-to-face meetings, student in-class evaluation, student survey, focus groups, etc...')
    )
    other_course_evaluation_methods = models.TextField(_('Other Course Evaluation Methods'), null=True, blank=True,
                                                       help_text=_('e.g. by faculty, program leaders, peer reviewer'))

    faculty_staff_availability = models.TextField(_('Faculty and Teaching Staff Availability'), null=True, blank=True)

    history = HistoricalRecords()

    @property
    def code(self):
        return "{} {}".format(self.program_code, self.number)

    def __str__(self):
        return self.code

    def release(self):
        """Creates a new release"""
        self.save()
        release = self.current_release()
        if release is None:
            new_version = 1
        else:
            new_version = release.version + 1
        new_release = CourseRelease.objects.create(version=new_version, course=self.history.latest())

        for objective in self.learning_objectives.all():
            new_release.learning_objectives.add(objective.history.latest())

        for prerequisite in self.prerequisite_courses.all():
            new_release.prerequisite_courses.add(prerequisite.history.latest())

        for corequisite in self.corequisite_courses.all():
            new_release.corequisite_courses.add(corequisite.history.latest())

        for clo in self.learning_outcomes.all():
            new_release.learning_outcomes.add(clo.history.latest())

        for topic in self.topics.all():
            new_release.topics.add(topic.history.latest())

        for assessment_task in self.assessment_tasks.all():
            new_release.assessment_tasks.add(assessment_task.history.latest())

        for facility_required in self.facilities_required.all():
            new_release.facilities_required.add(facility_required.history.latest())

    def current_release(self):
        """Gets the current release"""
        try:
            release = CourseRelease.objects.filter(course__id=self.id).latest('version')
        except CourseRelease.DoesNotExist:
            release = None
        return release


class LearningObjective(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=False, verbose_name=_('Course'),
                               related_name='learning_objectives')
    learning_objective = models.CharField(_('Learning Objective'), max_length=2000, null=False, blank=False)

    history = HistoricalRecords()

    def __str__(self):
        return self.learning_objective


class CourseLearningOutcome(models.Model):
    class Categories:
        KNOWLEDGE = 'knowledge'
        SKILLS = 'skills'
        COMPETENCE = 'competence'

        @classmethod
        def choices(cls):
            return (
                (cls.KNOWLEDGE, _('Knowledge')),
                (cls.SKILLS, _('Skills')),
                (cls.COMPETENCE, _('Competence')),
            )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=False, verbose_name=_('Course'),
                               related_name='learning_outcomes')
    clo_category = models.CharField(_('Category'), max_length=50, null=True, blank=False, choices=Categories.choices())
    learning_outcome = models.CharField(_('Learning Outcome'), max_length=2000, null=True, blank=False)
    teaching_strategy = models.CharField(_('Teaching Strategy'), max_length=2000, null=True, blank=False)
    assessment_method = models.CharField(_('Assessment Method'), max_length=2000, null=True, blank=False)

    history = HistoricalRecords()

    def __str__(self):
        return '{} - {}'.format(self.get_clo_category_display(), self.learning_outcome)


class Topic(models.Model):
    class Types:
        LECTURE = 'lecture'
        LAB = 'lab'
        TUTORIAL = 'tutorial'
        PRACTICAL = 'practical'
        OTHER = 'other'

        @classmethod
        def choices(cls):
            return (
                (cls.LECTURE, _('Lecture')),
                (cls.LAB, _('Laboratory')),
                (cls.TUTORIAL, _('Tutorial')),
                (cls.PRACTICAL, _('Practical')),
                (cls.OTHER, _('Other')),
            )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=False, verbose_name=_('Course'),
                               related_name='topics')
    type = models.CharField(_('Type'), max_length=50, null=True, blank=False, choices=Types.choices())
    topic = models.CharField(_('Topic'), max_length=2000, null=True, blank=False)
    contact_hours = models.DecimalField(
        _('Contact Hours'),
        null=True,
        blank=False,
        max_digits=settings.MAX_DIGITS,
        decimal_places=settings.MAX_DECIMAL_POINT
    )
    related_course_learning_outcomes = models.ManyToManyField('CourseLearningOutcome', blank=True,
                                                              related_name='covered_by_topics')

    history = HistoricalRecords()

    def __str__(self):
        return '{} - {}'.format(self.get_type_display(), self.topic)


class AssessmentTask(models.Model):
    class Types:
        LECTURE = 'lecture'
        LAB = 'lab'

        @classmethod
        def choices(cls):
            return (
                (cls.LECTURE, _('Lecture')),
                (cls.LAB, _('Laboratory')),
            )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=False, verbose_name=_('Course'),
                               related_name='assessment_tasks')
    type = models.CharField(_('Type'), max_length=50, null=True, blank=False, choices=Types.choices())
    assessment_task = models.CharField(_('Assessment Task'), max_length=2000, null=True, blank=False,
                                       help_text=_('e.g essay, test, group project, examination, speech, etc...'))
    week_due = models.PositiveSmallIntegerField(_('Week Due'), null=True, blank=True)
    weight_percentage = models.DecimalField(
        _('Weight Percentage'),
        null=True,
        blank=False,
        max_digits=settings.MAX_DIGITS,
        decimal_places=settings.MAX_DECIMAL_POINT,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(0.1)
        ]
    )

    history = HistoricalRecords()

    def __str__(self):
        return '{} - {}'.format(self.get_type_display(), self.assessment_task)


class FacilitiesRequired(models.Model):
    class Types:
        ACCOMMODATION = 'accommodation'
        TECHNOLOGY_RESOURCES = 'technology_resources'
        OTHER = 'other'

        @classmethod
        def choices(cls):
            return (
                (cls.ACCOMMODATION, _('Accommodation')),
                (cls.TECHNOLOGY_RESOURCES, _('Technology Resources')),
                (cls.OTHER, _('Other')),
            )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=False, verbose_name=_('Course'),
                               related_name='facilities_required')
    type = models.CharField(_('Type'), max_length=50, null=True, blank=False, choices=Types.choices())
    facility_required = models.CharField(_('Facility Required'), max_length=2000, null=True, blank=False,
                                         help_text=_('e.g. classrooms and laboratories'))

    history = HistoricalRecords()

    def __str__(self):
        return '{} - {}'.format(self.get_type_display(), self.facility_required)


class CourseRelease(models.Model):
    version = models.PositiveIntegerField(_('version'), null=False, default=1)
    course = models.ForeignKey('HistoricalCourse', on_delete=models.PROTECT,
                               null=False, blank=False, verbose_name=_('course'),
                               related_name='releases')
    prerequisite_courses = models.ManyToManyField('HistoricalCourse', related_name='prerequisite_for')
    corequisite_courses = models.ManyToManyField('HistoricalCourse', related_name='corequisite_for')
    learning_objectives = models.ManyToManyField('HistoricalLearningObjective', related_name='releases')
    learning_outcomes = models.ManyToManyField('HistoricalCourseLearningOutcome', related_name='releases')
    topics = models.ManyToManyField('HistoricalTopic', related_name='releases')
    assessment_tasks = models.ManyToManyField('HistoricalAssessmentTask', related_name='releases')
    facilities_required = models.ManyToManyField('HistoricalFacilitiesRequired', related_name='releases')

    class Meta:
        unique_together = ('version', 'course')

    def __str__(self):
        return '{} - {}'.format(self.version, self.course)

# May need the explicit 'through' model below to better control on_delete behavior
# class CourseReleaseLearningObjective(models.Model):
#     """A many-to-many relationship table linking historical learning objectives to course releases"""
#     course_release = models.ForeignKey(CourseRelease, on_delete=models.CASCADE,
#                                        null=False, related_name='learning_objectives')
#     learning_objective = models.ForeignKey(HistoricalLearningObjective, on_delete=models.PROTECT,
#                                            null=False, related_name='releases')