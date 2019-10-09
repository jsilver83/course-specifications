from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from simple_history.models import HistoricalRecords

from course_specifications.utils import get_department_name, get_full_name, CamundaAPI

User = settings.AUTH_USER_MODEL


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

    # region model-fields

    # region desc
    mother_department = models.CharField(_('Mother Department'), max_length=500, null=True, blank=False)
    program_code = models.CharField(_('Program Code'), max_length=10, null=True, blank=False,
                                    help_text=_('3 or 4 upper-case letters only'),
                                    validators=[
                                        RegexValidator(r'^[A-Z]{3,4}$'),
                                    ])
    number = models.CharField(_('Number'), max_length=10, null=True, blank=False)
    title = models.CharField(_('Title'), max_length=500, null=True, blank=False)
    catalog_description = models.TextField(_('Catalog Description'), null=True, blank=False,
                                           help_text=_('General description about the course and topics covered'))
    location = models.CharField(_('Location'), max_length=50, null=True, blank=False, choices=Locations.choices())
    lecture_credit_hours = models.PositiveSmallIntegerField(_('Lecture Credit Hours'), null=True, blank=False,
                                                            validators=[
                                                                MinValueValidator(0),
                                                                MaxValueValidator(12),
                                                            ], )
    lab_contact_hours = models.PositiveSmallIntegerField(_('Lab Contact Hours'), null=True, blank=True,
                                                         validators=[
                                                             MinValueValidator(0),
                                                             MaxValueValidator(12),
                                                         ], )
    total_credit_hours = models.PositiveSmallIntegerField(_('Total Credit Hours'), null=True, blank=False,
                                                          validators=[
                                                              MinValueValidator(0),
                                                              MaxValueValidator(12),
                                                          ], )
    weekly_office_hours = models.PositiveSmallIntegerField(_('Weekly Office Hours'), null=True, blank=True,
                                                           validators=[
                                                               MinValueValidator(3),
                                                           ])

    prerequisite_courses = models.ManyToManyField('Course', blank=True, related_name='prerequisite_for')
    corequisite_courses = models.ManyToManyField('Course', blank=True, related_name='corequisite_for')
    # endregion desc

    # region mode_of_instruction
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
        blank=True,
        max_digits=settings.MAX_DIGITS,
        decimal_places=settings.MAX_DECIMAL_POINT,
        validators=[
            MinValueValidator(0.1),
            MaxValueValidator(100),
        ],
    )
    mode_of_instruction_other_desc = models.CharField(_('Mode Of Instruction (Other) Description'),
                                                      max_length=100, null=True, blank=True)
    mode_of_instruction_comments = models.TextField(_('Mode Of Instruction Comments'), null=True, blank=True)
    # endregion mode_of_instruction

    # region contact-hrs
    tutorial_contact_hours = models.DecimalField(
        _('Tutorial Contact Hours'),
        null=True,
        blank=True,
        max_digits=settings.MAX_DIGITS,
        decimal_places=settings.MAX_DECIMAL_POINT
    )
    practical_contact_hours = models.DecimalField(
        _('Practical Contact Hours'),
        null=True,
        blank=True,
        max_digits=settings.MAX_DIGITS,
        decimal_places=settings.MAX_DECIMAL_POINT
    )
    other_contact_hours = models.DecimalField(
        _('Other Contact Hours'),
        null=True,
        blank=True,
        max_digits=settings.MAX_DIGITS,
        decimal_places=settings.MAX_DECIMAL_POINT
    )
    other_contact_hours_description = models.CharField(_('Other Contact Hours Description'), null=True, blank=True,
                                                       max_length=200)
    # endregion contact-hrs

    # region self-study
    self_study_lecture = models.DecimalField(
        _('Self-Study Lecture Hours'),
        null=True,
        blank=True,
        max_digits=settings.MAX_DIGITS,
        decimal_places=settings.MAX_DECIMAL_POINT
    )
    self_study_lab = models.DecimalField(
        _('Self-Study Laboratory Hours'),
        null=True,
        blank=True,
        max_digits=settings.MAX_DIGITS,
        decimal_places=settings.MAX_DECIMAL_POINT
    )
    self_study_tutorial = models.DecimalField(
        _('Self-Study Tutorial Hours'),
        null=True,
        blank=True,
        max_digits=settings.MAX_DIGITS,
        decimal_places=settings.MAX_DECIMAL_POINT
    )
    self_study_practical = models.DecimalField(
        _('Self-Study Practical Hours'),
        null=True,
        blank=True,
        max_digits=settings.MAX_DIGITS,
        decimal_places=settings.MAX_DECIMAL_POINT
    )
    self_study_other = models.DecimalField(
        _('Self-Study Other Hours'),
        null=True,
        blank=True,
        max_digits=settings.MAX_DIGITS,
        decimal_places=settings.MAX_DECIMAL_POINT
    )
    # endregion self-study

    # region subject-area
    engineering_credit_hours = models.DecimalField(
        _('Engineering / Computer Science Credit Hours'),
        null=True,
        blank=True,
        max_digits=settings.MAX_DIGITS,
        decimal_places=settings.MAX_DECIMAL_POINT
    )
    math_science_credit_hours = models.DecimalField(
        _('Mathematics/Science Credit Hours'),
        null=True,
        blank=True,
        max_digits=settings.MAX_DIGITS,
        decimal_places=settings.MAX_DECIMAL_POINT
    )
    humanities_credit_hours = models.DecimalField(
        _('Humanities Credit Hours'),
        null=True,
        blank=True,
        max_digits=settings.MAX_DIGITS,
        decimal_places=settings.MAX_DECIMAL_POINT
    )
    social_sciences_credit_hours = models.DecimalField(
        _('Social Sciences Credit Hours'),
        null=True,
        blank=True,
        max_digits=settings.MAX_DIGITS,
        decimal_places=settings.MAX_DECIMAL_POINT
    )
    general_education_credit_hours = models.DecimalField(
        _('General Education Credit Hours'),
        null=True,
        blank=True,
        max_digits=settings.MAX_DIGITS,
        decimal_places=settings.MAX_DECIMAL_POINT
    )
    other_subject_areas_credit_hours = models.DecimalField(
        _('Other Subject Areas Credit Hours'),
        null=True,
        blank=True,
        max_digits=settings.MAX_DIGITS,
        decimal_places=settings.MAX_DECIMAL_POINT
    )
    # endregion subject-area

    # region material
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
    # endregion material

    # region misc
    strategies_of_student_feedback_and_evaluation = models.TextField(
        _('Strategies for obtaining Students Feedback and Evaluation'), null=True, blank=False,
        help_text=_('e.g. face-to-face meetings, student in-class evaluation, student survey, focus groups, etc...')
    )
    other_course_evaluation_methods = models.TextField(_('Other Course Evaluation Methods'), null=True, blank=True,
                                                       help_text=_('e.g. by faculty, program leaders, peer reviewer'))

    faculty_staff_availability = models.TextField(_('Faculty and Teaching Staff Availability'), null=True, blank=True,
                                                  help_text=_('Arrangements for availability of faculty and teaching '
                                                              'staff for individual student consultations and academic '
                                                              'advice'))
    # endregion misc

    # TODO: add grad_flag
    # endregion

    history = HistoricalRecords()

    class Meta:
        unique_together = ('program_code', 'number')

    @property
    def code(self):
        return "{} {}".format(self.program_code, self.number)

    def __str__(self):
        return self.code

    def release(self):
        """Creates a new release that will be reviewed"""
        self.save()
        release = self.current_release()
        if release is None:
            new_version = 0
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

    def all_releases(self):
        return CourseRelease.objects.filter(course__id=self.id)

    def current_release(self):
        """Gets the current APPROVED release"""
        try:
            release = CourseRelease.objects.filter(course__id=self.id, approved=True).latest()
        except CourseRelease.DoesNotExist:
            release = None
        return release

    def current_version(self):
        if self.current_release():
            v = self.current_release().version
        else:
            v = 0

        return 'V{}'.format(v)

    def latest_release(self):
        """Gets the latest release whether it is approved or not"""
        try:
            release = CourseRelease.objects.filter(course__id=self.id).latest()
        except CourseRelease.DoesNotExist:
            release = None
        return release

    def last_edit(self):
        try:
            return self.history.first().history_date
        except:
            pass

    def get_min_lecture_contact_hours_for_topics(self):
        try:
            return self.lecture_credit_hours * 15
        except TypeError:
            pass

    def get_max_lecture_contact_hours_for_topics(self):
        try:
            return self.lecture_credit_hours * 15
        except TypeError:
            pass

    def get_min_lab_contact_hours_for_topics(self):
        try:
            return (self.lab_contact_hours * 15) / 2
        except TypeError:
            pass

    def get_max_lab_contact_hours_for_topics(self):
        try:
            return self.lab_contact_hours * 15
        except TypeError:
            pass

    def total_lecture_topic_contact_hours(self):
        return self.topics.filter(type=Topic.Types.LECTURE).aggregate(Sum('contact_hours')).get('contact_hours__sum')

    def total_lab_topic_contact_hours(self):
        return self.topics.filter(type=Topic.Types.LAB).aggregate(Sum('contact_hours')).get('contact_hours__sum')

    def total_lecture_assessment_tasks_weight(self):
        return self.assessment_tasks.filter(
            type=AssessmentTask.Types.LECTURE
        ).aggregate(Sum('weight_percentage')).get('weight_percentage__sum')

    def total_lab_assessment_tasks_weight(self):
        return self.assessment_tasks.filter(
            type=AssessmentTask.Types.LAB
        ).aggregate(Sum('weight_percentage')).get('weight_percentage__sum')

    def get_total_self_study_hours(self):
        self_studies = [self.self_study_lecture, self.self_study_lab, self.self_study_other,
                        self.self_study_practical, self.self_study_tutorial]

        return sum(filter(None, self_studies))

    def can_navigate_to_step1(self):
        return self.title

    def can_navigate_to_step2(self):
        return self.catalog_description

    def can_navigate_to_step3(self):
        return (self.engineering_credit_hours or self.math_science_credit_hours or self.humanities_credit_hours
                or self.social_sciences_credit_hours or self.general_education_credit_hours
                or self.other_subject_areas_credit_hours)

    def can_navigate_to_step4(self):
        return self.assessment_tasks.all().count()

    def can_navigate_to_step5(self):
        return self.required_textbooks_from_sierra

    def can_navigate_to_step6(self):
        return self.strategies_of_student_feedback_and_evaluation

    def can_navigate_to_step7(self):
        return self.facilities_required.all().count()

    def get_department_name(self):
        return get_department_name(self.mother_department)

    # TODO: use Hassan's API from Adwar
    def is_a_maintainer(self, user):
        return True

    def can_be_re_released(self):
        """A course can NOT be edited if the latest release is still being reviewed; i.e. approved is None"""
        return not CourseRelease.objects.filter(course__id=self.id, approved__isnull=True).exists()

    def can_be_edited(self, user):
        return self.can_be_re_released() and self.is_a_maintainer(user)


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
    week_due = models.PositiveSmallIntegerField(_('Week Due'), null=True, blank=False,
                                                validators=[
                                                    MinValueValidator(1),
                                                    MaxValueValidator(17),
                                                ], )
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

    class Meta:
        ordering = ('course', 'type', 'week_due')

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
    _workflow_status = models.CharField(_('Workflow Status (Cached)'), max_length=200, null=True, blank=True)
    _workflow_assignee = models.CharField(_('Workflow Assignee (Cached)'), max_length=200, null=True, blank=True)
    workflow_instance_id = models.CharField(_('Workflow Instance ID'), max_length=200, null=True, blank=True)
    approved = models.NullBooleanField(_('Approved'), null=True, blank=True)
    approved_on = models.DateTimeField(_('Approved On'), null=True, blank=True)
    approved_by = models.ForeignKey(User, on_delete=models.PROTECT,
                                    null=True, blank=True, verbose_name=_('Approved By'),
                                    related_name='approved_courses', )

    # TODO: meaningful names plz
    # flag_1 = models.NullBooleanField(_('Course Identification Flag'), null=True, blank=True)
    # flag_2 = models.NullBooleanField(_('Course Identification Flag'), null=True, blank=True)
    # flag_3 = models.NullBooleanField(_('Course Identification Flag'), null=True, blank=True)
    # flag_4 = models.NullBooleanField(_('Course Identification Flag'), null=True, blank=True)
    # flag_5 = models.NullBooleanField(_('Course Identification Flag'), null=True, blank=True)
    # flag_6 = models.NullBooleanField(_('Course Identification Flag'), null=True, blank=True)
    # flag_7 = models.NullBooleanField(_('Course Identification Flag'), null=True, blank=True)

    class Meta:
        unique_together = ('version', 'course')
        get_latest_by = ['course__history_date', 'version']

    def __str__(self):
        return '{} - {}'.format(self.version, self.course)

    def approve(self, user, approval_state):
        self.approved = approval_state
        self.approved_by = user
        self.approved_on = timezone.now()
        self.save()

    @property
    def camunda_task(self):
        # fetch active task info from camunda api
        # and save them into _workflow_status and _workflow_assignee
        task_options = None

        try:
            camunda_api = CamundaAPI(self.workflow_instance_id)
            active_task = camunda_api.get_active_task()
            if active_task:
                self._workflow_status = active_task['name']
                self._workflow_assignee = active_task['assignee']
                self.save()

                task_options = camunda_api.get_task_options(active_task)
        except:
            pass

        task_summery = {
            'name': self._workflow_status,
            'assignee': self._workflow_assignee,
            'options':task_options or {}
        }


        return task_summery

    @property
    def is_completed(self):
        camunda_api = CamundaAPI(self.workflow_instance_id)
        return camunda_api.is_process_completed()

    def complete_task(self, decision):
        camunda_api = CamundaAPI(self.workflow_instance_id)

        return camunda_api.complete_current_task(decision)

    @property
    def course_release_status(self):
        camunda_api = CamundaAPI(self.workflow_instance_id)
        active_task = camunda_api.get_active_task()
        if active_task:
            self._workflow_status = active_task['name']
            self._workflow_assignee = active_task['assignee']
            self.save()
            return {
                'name': self._workflow_status,
                'assignee': self._workflow_assignee,
            }

    # TODO get AAC_task_assignee, is graduate course, and (collage id it may be changed in camunda code)
    def start_camunda_process(self):
        process_instance = CamundaAPI.start_process(
            self.course.code,
            self.id,
            'AAC_task_assignee',
            False,
            self.course.mother_department,
            'collage_id'
        )

        self.workflow_instance_id = process_instance['id']
        self.save()

# May need the explicit 'through' model below to better control on_delete behavior
# class CourseReleaseLearningObjective(models.Model):
#     """A many-to-many relationship table linking historical learning objectives to course releases"""
#     course_release = models.ForeignKey(CourseRelease, on_delete=models.CASCADE,
#                                        null=False, related_name='learning_objectives')
#     learning_objective = models.ForeignKey(HistoricalLearningObjective, on_delete=models.PROTECT,
#                                            null=False, related_name='releases')


class ApprovalComment(models.Model):
    class Sections:
        # TODO: add rest of the sections
        COURSE_IDENTIFICATION = 'COURSE_IDENTIFICATION'
        REQUISITES = 'REQUISITES'
        MODE_OF_INSTRUCTION = 'MODE_OF_INSTRUCTION'
        OFFICE_HOURS = 'OFFICE_HOURS'
        DESCRIPTION = 'DESCRIPTION'
        OBJECTIVES = 'OBJECTIVES'
        CLO = 'CLO'
        TOPICS = 'TOPICS'
        SELF_LEARNING = 'SELF_LEARNING'
        SUBJECT_AREA_HRS = 'SUBJECT_AREA_HRS'
        ASSESSMENT_TASKS = 'ASSESSMENT_TASKS'
        LEARNING_RESOURCES = 'LEARNING_RESOURCES'
        COURSE_EVALUATION = 'COURSE_EVALUATION'

        @classmethod
        def choices(cls):
            return (
                (cls.SECTION_1, _('Section# 1'))
            )

    course_release = models.ForeignKey('CourseRelease', on_delete=models.CASCADE,
                                       null=False, blank=False, verbose_name=_('course_release'),
                                       related_name='approval_comments')
    section = models.CharField(max_length=200)
    comment = models.CharField(max_length=1000)
    commented_by = models.ForeignKey(User, on_delete=models.PROTECT,
                                     null=True, blank=True, verbose_name=_('Commenter'),
                                     related_name='approval_comments', )
    comment_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        get_latest_by = ['comment_date', ]

    def __str__(self):
        return self.comment

    def commenter_role(self):
        # TODO: get role from Camunda [Shaheed]
        return ''

    def create_viewership(self, user):
        # TODO: implement
        pass

    def is_new_for_user(self, user):
        # TODO: implement
        pass

    def commenter_full_name(self):
        return get_full_name(self.commented_by)


class CommentViewership(models.Model):
    comment = models.ForeignKey('ApprovalComment', on_delete=models.CASCADE,
                                null=True, blank=False, verbose_name=_('Comment'),
                                related_name='comment_views', )
    viewer = models.ForeignKey(User, on_delete=models.CASCADE,
                               null=True, blank=False, verbose_name=_('Viewer'),
                               related_name='viewed_comments', )
    is_new = models.BooleanField(
        _('Is New?'),
        default=True,
        help_text=_('If checked, it means this comment is new to this user. The comment will be considered old, '
                    'if the user moved on in the process to the next step')
    )
    viewed_on = models.DateTimeField(_('Viewed On'), auto_now=True)
