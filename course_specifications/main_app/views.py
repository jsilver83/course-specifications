from django.utils.translation import ugettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import redirect
from django.views.generic import TemplateView, CreateView, ListView, UpdateView

from .forms import CourseIdentificationForm
from .models import *


class CoursesList(ListView):
    model = Course
    template_name = 'main_app/courses_list.html'
    context_object_name = 'courses'


class NewCourse(SuccessMessageMixin, CreateView):
    form_class = CourseIdentificationForm
    template_name = 'main_app/course-identification-form.html'
    success_url = reverse_lazy('main_app:index')
    success_message = _('Course created successfully')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['step1_state'] = 'active'
        return context


class UpdateCourse(SuccessMessageMixin, UpdateView):
    model = Course
    form_class = CourseIdentificationForm
    template_name = 'main_app/course-identification-form.html'
    success_url = reverse_lazy('main_app:index')
    success_message = _('Course updated successfully')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['step1_state'] = 'active'
        return context


class Release(View):
    def get(self, request, *args, **kwargs):
        course = Course.objects.get(id=kwargs['course_id'])
        course.release()
        return redirect('course_list')
