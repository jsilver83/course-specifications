from decimal import Decimal

from django import forms
from django.forms import modelformset_factory, BaseModelFormSet
from django.utils.translation import ugettext_lazy as _

from .models import *


class CourseIdentificationForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['program_code', 'number', 'title', 'location',
                  'lecture_credit_hours', 'lab_contact_hours', 'total_credit_hours', 'weekly_office_hours',
                  'prerequisite_courses', 'corequisite_courses', 'mode_of_instruction_in_class',
                  'mode_of_instruction_other', 'mode_of_instruction_other_desc', 'mode_of_instruction_comments']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

        # self.fields['number'].widget.attrs.update({'placeholder': _('000')})
        self.fields['mode_of_instruction_in_class'].widget.attrs.update({'placeholder': _('Percentage (%)')})
        self.fields['mode_of_instruction_other'].widget.attrs.update({'placeholder': _('Percentage (%)')})
        self.fields['mode_of_instruction_other_desc'].widget.attrs.update({'placeholder': _('Other')})
        self.fields['lecture_credit_hours'].widget.attrs.update({'placeholder': _('Credit Hrs')})
        self.fields['lab_contact_hours'].widget.attrs.update({'placeholder': _('Contact Hrs')})
        self.fields['total_credit_hours'].widget.attrs.update({'placeholder': _('Credit Hrs')})

        self.fields['mode_of_instruction_comments'].label = _('Comments')

        self.fields['lecture_credit_hours'].label = _('Lecture')
        self.fields['lab_contact_hours'].label = _('Lab')
        self.fields['total_credit_hours'].label = _('Total')
        self.fields['mode_of_instruction_in_class'].label = _('In class (face to face)')

        courses = Course.objects.exclude(pk=self.instance.pk)
        self.fields['prerequisite_courses'].queryset = courses
        self.fields['corequisite_courses'].queryset = courses

    def clean(self):
        cleaned_data = super().clean()

        mode_of_instruction_in_class = cleaned_data.get('mode_of_instruction_in_class')
        mode_of_instruction_other = cleaned_data.get('mode_of_instruction_other')

        if mode_of_instruction_other and mode_of_instruction_in_class + mode_of_instruction_other > 100:
            raise forms.ValidationError(
                _('Mode of Instruction summation of In-Class and Other should NOT exceed 100'),
            )

        return cleaned_data


class CourseDescriptionForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['catalog_description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['catalog_description'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': _('General description about the course & topics')
        })


class LearningObjectiveForm(forms.ModelForm):
    class Meta:
        model = LearningObjective
        fields = ['learning_objective']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['learning_objective'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': _('Enter objective')
        })


LearningObjectiveFormSet = modelformset_factory(model=LearningObjective, form=LearningObjectiveForm,
                                                extra=3, can_delete=True, min_num=1, validate_min=True)


class CourseLearningOutcomeForm(forms.ModelForm):
    class Meta:
        model = CourseLearningOutcome
        fields = ['clo_category', 'learning_outcome', 'teaching_strategy', 'assessment_method', ]


CourseLearningOutcomeFormSet = modelformset_factory(model=CourseLearningOutcome, form=CourseLearningOutcomeForm,
                                                    extra=3, can_delete=True, min_num=1, validate_min=True)


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['topic', 'contact_hours', 'related_course_learning_outcomes', ]

    def __init__(self, course, *args, **kwargs):
        self.course = course
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

        self.fields['topic'].widget.attrs.update({'placeholder': _('Enter topic')})
        self.fields['contact_hours'].widget.attrs.update({'placeholder': _('e.g. 3 hrs')})
        self.fields['related_course_learning_outcomes'].widget.attrs.update({'class': 'select2 form-control',
                                                                             'style': 'width:100%'})

        self.fields['related_course_learning_outcomes'].queryset = CourseLearningOutcome.objects.filter(
            course=self.course
        )


class LectureTopicBaseFormSet(BaseModelFormSet):

    def clean(self):
        if any(self.errors):
            # Don't bother validating the formset unless each form is valid on its own
            return

        total = Decimal('0.00')
        for form in self.forms:
            if self.can_delete and self._should_delete_form(form):
                continue
            total += form.cleaned_data.get('contact_hours', Decimal('0.00'))

        course = self.get_form_kwargs(0).get('course')

        if total != course.get_min_lecture_contact_hours_for_topics():
            raise forms.ValidationError(_('Total contact hours for lecture should be equal to {}'.format(
                course.get_min_lecture_contact_hours_for_topics())))


class LabTopicBaseFormSet(BaseModelFormSet):

    def clean(self):
        if any(self.errors):
            # Don't bother validating the formset unless each form is valid on its own
            return

        total = Decimal('0.00')
        for form in self.forms:
            if self.can_delete and self._should_delete_form(form):
                continue
            total += form.cleaned_data.get('contact_hours', Decimal('0.00'))

        course = self.get_form_kwargs(0).get('course')

        if total > course.get_max_lab_contact_hours_for_topics() or total < course.get_min_lab_contact_hours_for_topics():
            raise forms.ValidationError(_('Total contact hours for lab should be between {} and {}'.format(
                course.get_min_lab_contact_hours_for_topics(),
                course.get_max_lab_contact_hours_for_topics(),
            )))


LectureTopicFormSet = modelformset_factory(model=Topic, form=TopicForm, formset=LectureTopicBaseFormSet,
                                           extra=3, can_delete=True, min_num=1, validate_min=True)

LabTopicFormSet = modelformset_factory(model=Topic, form=TopicForm, formset=LabTopicBaseFormSet,
                                       extra=3, can_delete=True, min_num=1, validate_min=True)


class CourseContentForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['self_study_lecture', 'self_study_lab', 'self_study_tutorial', 'self_study_practical',
                  'self_study_other', 'engineering_credit_hours', 'math_science_credit_hours',
                  'humanities_credit_hours', 'social_sciences_credit_hours', 'general_education_credit_hours',
                  'other_subject_areas_credit_hours', 'tutorial_contact_hours', 'practical_contact_hours',
                  'other_contact_hours', 'other_contact_hours_description', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            if field not in ['other_contact_hours_description']:
                self.fields[field].widget.attrs.update({'placeholder': _('e.g. 3 hrs')})

            if field not in ['tutorial_contact_hours', 'practical_contact_hours', 'other_contact_hours',
                             'other_contact_hours_description']:
                self.fields[field].label = self.fields[field].label.replace('Hours', '').replace(
                    'Self-Study', '').replace('Credit', '')

        self.fields['other_contact_hours_description'].label = _('Description')
        self.fields['other_contact_hours'].label = _('Contact Hours')

    def clean(self):
        cleaned_data = super().clean()
        if not any([cleaned_data.get('engineering_credit_hours'), cleaned_data.get('math_science_credit_hours'),
                    cleaned_data.get('humanities_credit_hours'), cleaned_data.get('social_sciences_credit_hours'),
                    cleaned_data.get('general_education_credit_hours'),
                    cleaned_data.get('other_subject_areas_credit_hours'), ]):
            raise forms.ValidationError(_('You need to specify credit hours in one classification at least'))

        return cleaned_data


class AssessmentTaskForm(forms.ModelForm):
    class Meta:
        model = AssessmentTask
        fields = ['type', 'assessment_task', 'week_due', 'weight_percentage', ]
        widgets = {
            'type': forms.HiddenInput,
        }

    def __init__(self, task_type, *args, **kwargs):
        self.task_type = task_type
        super().__init__(*args, **kwargs)

        self.initial['type'] = self.task_type

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

        self.fields['assessment_task'].widget.attrs.update({'placeholder':
                                                                _('e.g. essay, test, group project, speech, etc.')})
        self.fields['week_due'].widget.attrs.update({'placeholder': _('e.g. 3')})
        self.fields['weight_percentage'].widget.attrs.update({'placeholder': _('e.g. 20'), 'step': '0.5'})


AssessmentTaskFormSet = modelformset_factory(model=AssessmentTask, form=AssessmentTaskForm,
                                             extra=3, can_delete=True, min_num=1, validate_min=True)


class LearningResourcesForm(forms.ModelForm):
    # TODO: fetch real textbooks from sierra
    CHOICES = (
        ('ISBN01', 'Test Textbook 1'),
        ('ISBN02', 'Test Textbook 2'),
        ('ISBN03', 'Test Textbook 3'),
        ('ISBN04', 'Test Textbook 4'),
        ('ISBN05', 'Test Textbook 5'),
    )

    required_textbooks_from_sierra = forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'class': 'select2'}),
                                                               choices=CHOICES)

    class Meta:
        model = Course
        fields = ['required_textbooks_from_sierra', 'other_required_textbooks', 'essential_reference_materials',
                  'recommended_textbooks_reference_materials', 'electronic_materials', 'other_materials', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # TODO: fix to show selected textbooks properly
        if self.instance.required_textbooks_from_sierra:
            self.fields['required_textbooks_from_sierra'].help_text = _('Currently selected: {}'.format(
                self.instance.required_textbooks_from_sierra)
            )
