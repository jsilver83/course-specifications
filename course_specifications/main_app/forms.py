from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Course


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

        self.fields['number'].widget.attrs.update({'placeholder': _('000')})
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

        # for field in self.fields:
        #     self.fields[field].widget.attrs.update({'class': 'form-control'})

        self.fields['catalog_description'].widget.attrs.update({
             'class': 'form-control',
             'placeholder': _('General description about the course & topics')
        })
