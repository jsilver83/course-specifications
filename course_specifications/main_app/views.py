from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import redirect
from django.views.generic import TemplateView, CreateView, ListView

from .forms import CourseIdentificationForm
from .models import *


class Index(ListView):
    model = Course
    template_name = 'main_app/course-identification-form.html'


class NewCourse(SuccessMessageMixin, CreateView):
    form_class = CourseIdentificationForm
    template_name = 'main_app/course-identification-form.html'
    success_url = reverse_lazy('main_app:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['step1_state'] = 'active'
        return context


class Release(View):
    def get(self, request, *args, **kwargs):
        course = Course.objects.get(id=kwargs['course_id'])
        course.release()
        return redirect('course_list')
