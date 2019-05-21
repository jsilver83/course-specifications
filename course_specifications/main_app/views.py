from django.utils.translation import ugettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import redirect
from django.views.generic import TemplateView, CreateView, ListView, UpdateView

from .forms import *
from .models import *


class CoursesList(ListView):
    model = Course
    template_name = 'main_app/courses_list.html'
    context_object_name = 'courses'


class NewCourse(SuccessMessageMixin, CreateView):
    form_class = CourseIdentificationForm
    template_name = 'main_app/course-identification.html'
    success_url = reverse_lazy('main_app:index')
    success_message = _('Course created successfully')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['step1_state'] = 'active'
        return context


class UpdateCourse(SuccessMessageMixin, UpdateView):
    model = Course
    form_class = CourseIdentificationForm
    template_name = 'main_app/course-identification.html'
    success_message = _('Course updated successfully')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['step1_state'] = 'active'
        return context

    def get_success_url(self):
        return reverse_lazy('main_app:course_description', args=(self.object.pk, ))


class Release(View):
    def get(self, request, *args, **kwargs):
        course = Course.objects.get(id=kwargs['course_id'])
        course.release()
        return redirect('course_list')


class CourseDescription(SuccessMessageMixin, UpdateView):
    model = Course
    form_class = CourseDescriptionForm
    template_name = 'main_app/course-description.html'
    success_url = reverse_lazy('main_app:index')
    success_message = _('Course updated successfully')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['step1_state'] = 'completed'
        context['step2_state'] = 'active'
        return context
