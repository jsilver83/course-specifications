from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render_to_response, render, get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views import View
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, FormView

from .forms import *
from .models import *


class CoursesList(ListView):
    model = Course
    template_name = 'main_app/courses_list.html'
    context_object_name = 'courses'


class NewCourse(SuccessMessageMixin, CreateView):
    form_class = CourseIdentificationForm
    template_name = 'main_app/course-identification.html'
    success_message = _('Course created successfully')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['step1_state'] = 'active'
        return context

    def form_valid(self, form):
        new_course = form.save()
        messages.success(self.request, self.success_message)
        return redirect(reverse_lazy('main_app:course_description', args=(new_course.pk, )))


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
        return redirect('main_app:course_list')


def course_description(request, pk):
    course = get_object_or_404(Course, pk=pk)

    form = CourseDescriptionForm(request.POST or None, instance=course)

    formset = LearningObjectiveFormSet(request.POST or None, queryset=course.learning_objectives.all(),
                                       prefix='objectives')

    formset2 = CourseLearningOutcomeFormSet(request.POST or None, queryset=course.learning_outcomes.all(),
                                            prefix='outcomes')

    if request.method == 'POST':
        if form.is_valid():
            saved_course = form.save()

            if formset.is_valid():
                for form1 in formset.forms:
                    if form1.is_valid():
                        obj = form1.save(commit=False)
                        obj.course = course
                formset.save()

            if formset2.is_valid():
                for form2 in formset2.forms:
                    if form2.is_valid():
                        obj2 = form2.save(commit=False)
                        obj2.course = course
                formset2.save()

            if formset.is_valid() and formset2.is_valid():
                messages.success(request, _('Course updated successfully'))
                return redirect(reverse_lazy('main_app:course_list'))

    return render(request, 'main_app/course-description.html', {
        'form': form, 'formset': formset, 'formset2': formset2,
        'step1_state': 'completed', 'step2_state': 'active',
    })


class CourseContents(SuccessMessageMixin, FormView):
    pass