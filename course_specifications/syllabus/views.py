from weasyprint import HTML
from docxtpl import DocxTemplate

from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView
from django.contrib.staticfiles import finders
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.contrib import messages
from django.urls import reverse
from course_specifications.utils import get_department_name
from main_app.models import Course, Topic
from syllabus.utils import get_weekly_topics_list, get_textbooks_list


class GenerateSyllabusBaseView(DetailView):
    model = Course
    number_of_weeks = 15

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course_current_release = self.get_object()
        context['department_name'] = get_department_name(course_current_release.course.history_object.mother_department)
        context['lecture_assessment_tasks'] = course_current_release.assessment_tasks.order_by('week_due').filter(
            type='lecture')
        context['lab_assessment_tasks'] = course_current_release.assessment_tasks.order_by('week_due').filter(
            type='lab')
        context['prerequisite_courses'] = course_current_release.prerequisite_courses.order_by('id').all()
        context['corequisite_courses'] = course_current_release.corequisite_courses.order_by('id').all()
        context['learning_objectives'] = course_current_release.learning_objectives.order_by('id').all()
        context['learning_outcomes'] = course_current_release.learning_outcomes.order_by('id').all()
        if course_current_release.course.history_object.required_textbooks_from_sierra:
            context['required_textbooks'] = get_textbooks_list(
                course_current_release.course.history_object.required_textbooks_from_sierra)
        if course_current_release.course.history_object.other_required_textbooks:
            context['other_required_textbooks'] = str(course_current_release.course.history_object
                                                      .other_required_textbooks).splitlines()
        else:
            context['other_required_textbooks'] = None

        if course_current_release.course.history_object.essential_reference_materials:
            context['essential_reference_materials'] = str(course_current_release.course.history_object
                                                           .essential_reference_materials).splitlines()
        else:
            context['essential_reference_materials'] = None

        if course_current_release.course.history_object.recommended_textbooks_reference_materials:
            context['recommended_textbooks_reference_materials'] = course_current_release.course.history_object \
                .recommended_textbooks_reference_materials.splitlines()
        else:
            context['recommended_textbooks_reference_materials'] = None
        total_lecture_topic_contact_hours = course_current_release.course.history_object.total_lecture_topic_contact_hours()
        if total_lecture_topic_contact_hours:
            context['lecture_topics_lists'] = get_weekly_topics_list(
                total_lecture_topic_contact_hours, self.number_of_weeks,
                list(course_current_release.topics.filter(type=Topic.Types.LECTURE).order_by('id').all()))
        total_lab_topic_contact_hours = course_current_release.course.history_object.total_lab_topic_contact_hours()
        if total_lab_topic_contact_hours:
            context['lab_topics_lists'] = get_weekly_topics_list(total_lab_topic_contact_hours, self.number_of_weeks,
                                                                 list(course_current_release.topics.filter(
                                                                     type=Topic.Types.LAB).order_by('id').all()))
        return context

    def get_object(self, queryset=None):
        course = super().get_object(queryset)
        return course.current_release()


class GeneratePDFSyllabusView(GenerateSyllabusBaseView):

    def get(self, request, *args, **kwargs):
        course_current_release = self.get_object()
        if course_current_release and course_current_release.version != 0:
            super().get(request, *args, **kwargs)
            context = self.get_context_data()
            html_template = get_template('syllabus/syllabus_pdf.html').render(context)
            pdf_file = HTML(string=html_template, base_url=request.build_absolute_uri()).write_pdf()
            response = HttpResponse(pdf_file, content_type='application/pdf')
            file_name = course_current_release.course.history_object.program_code + " " + \
                        course_current_release.course.history_object.number + " Syllabus"
            response['Content-Disposition'] = 'filename="%s.pdf"' % file_name
            return response
        else:
            messages.error(message=_('This course has no approved release yet'), request=request)
            return HttpResponseRedirect(reverse('main_app:course_list'))


class GenerateWordSyllabusView(GenerateSyllabusBaseView):

    def get(self, request, *args, **kwargs):
        course_current_release = self.get_object()
        if course_current_release and course_current_release.version != 0:
            super().get(request, *args, **kwargs)
            context = self.get_context_data()
            result = finders.find('syllabus_template.docx')
            doc = DocxTemplate(result)
            doc.render(context)
            response = HttpResponse(
                content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            file_name = course_current_release.course.history_object.program_code + " " + \
                        course_current_release.course.history_object.number + " Syllabus"
            response['Content-Disposition'] = 'attachment; filename="%s.docx"' % file_name
            doc.save(response)
            return response
        else:
            messages.error(message=_('This course has no approved release yet'), request=request)
            return HttpResponseRedirect(reverse('main_app:course_list'))
