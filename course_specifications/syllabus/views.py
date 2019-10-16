from django.views.generic import DetailView
from docxtpl import DocxTemplate
from weasyprint import HTML

from django.contrib.staticfiles import finders
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django.views import View

from course_specifications.utils import get_department_name
from main_app.models import Course
from syllabus.utils import get_topics_list


class GenerateSyllabusBaseView(DetailView):
    model = Course
    # object = None

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['department_name'] = get_department_name(self.get_object().mother_department)
        context['lecture_assessment_tasks'] = self.get_object().assessment_tasks.filter(type='lecture')
        context['lab_assessment_tasks'] = self.get_object().assessment_tasks.filter(type='lab')
        context['prerequisite_courses'] = self.get_object().prerequisite_courses.all()
        context['corequisite_courses'] = self.get_object().corequisite_courses.all()
        context['learning_objectives'] = self.get_object().learning_objectives.all()
        context['learning_outcomes'] = self.get_object().learning_outcomes.all()
        if self.get_object().other_required_textbooks:
            context['other_required_textbooks'] = str(self.get_object().other_required_textbooks).splitlines()
        else:
            context['other_required_textbooks'] = None
        if self.get_object().essential_reference_materials:
            context['essential_reference_materials'] = str(self.get_object().essential_reference_materials).splitlines()
        else:
            context['essential_reference_materials'] = None
        if self.get_object().recommended_textbooks_reference_materials:
            context['recommended_textbooks_reference_materials'] = self.get_object()\
                .recommended_textbooks_reference_materials.splitlines()
        else:
            context['recommended_textbooks_reference_materials'] = None
        context['lecture_topics_lists'] = get_topics_list(self.get_object().lab_contact_hours, 15 ,list(self.get_object().topics.filter(type='lecture')))
        context['lab_topics_lists'] = get_topics_list(self.get_object().lab_contact_hours, 15, list(self.get_object().topics.filter(type='lab')))
        data = {}
        data['coll'] = 'Cool'
        print(data)
        print(type(context['department_name']))
        print(context['department_name'])
        print(self.get_object().mother_department)
        return context


class GeneratePDFSyllabusView(GenerateSyllabusBaseView):


    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        print(self.get_context_data())
        html_template = get_template('syllabus/syllabus_pdf.html').render(self.get_context_data())
        pdf_file = HTML(string=html_template,base_url=request.build_absolute_uri()).write_pdf()
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = 'filename="home_page.pdf"'
        # response = HttpResponse(html_template)
        return response


class GenerateWordSyllabusView(GenerateSyllabusBaseView):
    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        result = finders.find('syllabus_template.docx')
        doc = DocxTemplate(result)
        doc.render(self.get_context_data(**kwargs))
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        file_name = self.get_context_data(**kwargs)['course'].program_code + " " + \
                    self.get_context_data(**kwargs)[
                        'course'].number + " Syllabus"
        response['Content-Disposition'] = 'attachment; filename="%s.docx"' % file_name
        doc.save(response)
        return response
