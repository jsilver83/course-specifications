from docxtpl import DocxTemplate
from weasyprint import HTML

from django.views.generic import DetailView
from django.contrib.staticfiles import finders
from django.http import HttpResponse
from django.template.loader import get_template

from course_specifications.utils import get_department_name
from main_app.models import Course, Topic
from syllabus.utils import get_weekly_topics_list, get_textbooks_list


class GenerateSyllabusBaseView(DetailView):
    model = Course

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        context['department_name'] = get_department_name(course.mother_department)
        context['lecture_assessment_tasks'] = course.assessment_tasks.filter(type='lecture')
        context['lab_assessment_tasks'] = course.assessment_tasks.filter(type='lab')
        context['prerequisite_courses'] = course.prerequisite_courses.all()
        context['corequisite_courses'] = course.corequisite_courses.all()
        context['learning_objectives'] = course.learning_objectives.all()
        context['learning_outcomes'] = course.learning_outcomes.all()
        if course.required_textbooks_from_sierra:
            context['required_textbooks'] = get_textbooks_list(course.required_textbooks_from_sierra)
        if course.other_required_textbooks:
            context['other_required_textbooks'] = str(course.other_required_textbooks).splitlines()
        else:
            context['other_required_textbooks'] = None
        if course.essential_reference_materials:
            context['essential_reference_materials'] = str(course.essential_reference_materials).splitlines()
        else:
            context['essential_reference_materials'] = None
        if course.recommended_textbooks_reference_materials:
            context['recommended_textbooks_reference_materials'] = course \
                .recommended_textbooks_reference_materials.splitlines()
        else:
            context['recommended_textbooks_reference_materials'] = None
        if course.total_lecture_topic_contact_hours():
            context['lecture_topics_lists'] = get_weekly_topics_list(
                course.total_lecture_topic_contact_hours(), 15,
                list(course.topics.filter(type=Topic.Types.LECTURE)))
        if course.total_lab_topic_contact_hours():
            context['lab_topics_lists'] = get_weekly_topics_list(course.total_lab_topic_contact_hours(), 15,
                                                                 list(course.topics.filter(
                                                                     type=Topic.Types.LAB)))
        return context


class GeneratePDFSyllabusView(GenerateSyllabusBaseView):

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        context = self.get_context_data()
        html_template = get_template('syllabus/syllabus_pdf.html').render(context)
        pdf_file = HTML(string=html_template, base_url=request.build_absolute_uri()).write_pdf()
        response = HttpResponse(pdf_file, content_type='application/pdf')
        file_name = context.get('course').program_code + " " + \
                    context.get('course').number + " Syllabus"
        response['Content-Disposition'] = 'filename="%s.pdf"' % file_name
        return response


class GenerateWordSyllabusView(GenerateSyllabusBaseView):

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        context = self.get_context_data()
        result = finders.find('syllabus_template.docx')
        doc = DocxTemplate(result)
        doc.render(self.get_context_data(**kwargs))
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        file_name = context.get('course').program_code + " " + \
                    context.get('course').number + " Syllabus"
        response['Content-Disposition'] = 'attachment; filename="%s.docx"' % file_name
        doc.save(response)
        return response
