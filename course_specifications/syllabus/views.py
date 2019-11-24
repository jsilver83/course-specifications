from weasyprint import HTML
from docxtpl import DocxTemplate

from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView
from django.contrib.staticfiles import finders
from django.http import HttpResponse
from django.template.loader import get_template

from course_specifications.utils import get_department_name
from main_app.models import Course
from syllabus.utils import get_weekly_topics_list, get_textbooks_list


class GenerateSyllabusBaseView(DetailView):
    model = Course

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['department_name'] = get_department_name(self.get_object().course.history_object.mother_department)
        context['lecture_assessment_tasks'] = self.get_object().assessment_tasks.order_by('pk').filter(type='lecture')
        context['lab_assessment_tasks'] = self.get_object().assessment_tasks.order_by('pk').filter(type='lab')
        context['prerequisite_courses'] = self.get_object().prerequisite_courses.order_by('pk').all()
        context['corequisite_courses'] = self.get_object().corequisite_courses.order_by('pk').all()
        context['learning_objectives'] = self.get_object().learning_objectives.order_by('pk').all()
        context['learning_outcomes'] = self.get_object().learning_outcomes.order_by('pk').all()
        if self.get_object().course.history_object.required_textbooks_from_sierra:
            context['required_textbooks'] = get_textbooks_list(
                self.get_object().course.history_object.required_textbooks_from_sierra)
        if self.get_object().course.history_object.other_required_textbooks:
            context['other_required_textbooks'] = str(self.get_object().course.history_object
                                                      .other_required_textbooks).splitlines()
        else:
            context['other_required_textbooks'] = None
        if self.get_object().course.history_object.essential_reference_materials:
            context['essential_reference_materials'] = str(self.get_object().course.history_object
                                                           .essential_reference_materials).splitlines()
        else:
            context['essential_reference_materials'] = None
        if self.get_object().course.history_object.recommended_textbooks_reference_materials:
            context['recommended_textbooks_reference_materials'] = self.get_object().course.history_object\
                .recommended_textbooks_reference_materials.splitlines()
        else:
            context['recommended_textbooks_reference_materials'] = None
        if self.get_object().course.history_object.lecture_credit_hours:
            context['lecture_topics_lists'] = get_weekly_topics_list(
                self.get_object().course.history_object.lecture_credit_hours, 15,
                list(self.get_object().topics.order_by('pk').filter(type='lecture')))
        if self.get_object().course.history_object.lab_contact_hours:
            context['lab_topics_lists'] = get_weekly_topics_list(
                self.get_object().course.history_object.lab_contact_hours, 15,
                list(self.get_object().topics.order_by('pk').filter(type='lab')))
        return context

    def get_object(self, queryset=None):
        course =  super().get_object(queryset)
        return course.current_release()


class GeneratePDFSyllabusView(GenerateSyllabusBaseView):

    def get(self, request, *args, **kwargs):
        course_current_release = self.get_object()
        if course_current_release and course_current_release.version != 0:
            super().get(request, *args, **kwargs)
            context = self.get_context_data()
            html_template = get_template('syllabus/syllabus_pdf.html').render(context)
            pdf_file = HTML(string=html_template,base_url=request.build_absolute_uri()).write_pdf()
            response = HttpResponse(pdf_file, content_type='application/pdf')
            file_name = context.get('object').course.history_object.program_code + " " + \
                        context.get('object').course.history_object.number + " Syllabus"
            response['Content-Disposition'] = 'filename="%s.pdf"' % file_name
        else:
            response = HttpResponse(_('This course has no approved release yet'))
        return response


class GenerateWordSyllabusView(GenerateSyllabusBaseView):
    def get(self, request, *args, **kwargs):
        course_current_release = self.get_object()
        if course_current_release and course_current_release.version != 0:
            super().get(request, *args, **kwargs)
            result = finders.find('syllabus_template.docx')
            doc = DocxTemplate(result)
            doc.render(self.get_context_data(**kwargs))
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            file_name = self.get_context_data(**kwargs)['object'].course.history_object.program_code + " " + \
                        self.get_context_data(**kwargs)[
                            'object'].course.history_object.number + " Syllabus"
            response['Content-Disposition'] = 'attachment; filename="%s.docx"' % file_name
            doc.save(response)
        else:
            response = HttpResponse(_('This course has no approved release yet'))
        return response
