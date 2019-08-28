from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render_to_response, render, get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views import View
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, FormView

from course_specifications.utils import UserType
from .forms import *
from .models import *


class AllowedUserTypesMixin(LoginRequiredMixin, UserPassesTestMixin):
    allowed_user_types = []

    def test_func(self):
        if self.allowed_user_types == '__all__':
            return True
        else:
            return UserType.get_user_type(self.request) in self.allowed_user_types


class CoursesListView(AllowedUserTypesMixin, ListView):
    model = Course
    template_name = 'main_app/courses_list.html'
    context_object_name = 'courses'
    allowed_user_types = '__all__'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['can_create_course'] = bool(UserType.get_user_type(self.request) in (UserType.CHAIRMAN, UserType.ADMIN))
        return context

    def get_queryset(self):
        if UserType.get_user_type(self.request) in (UserType.CHAIRMAN, UserType.FACULTY):
            return self.model.objects.filter(mother_department=UserType.get_department_id(self.request))
        elif UserType.get_user_type(self.request) == UserType.ADMIN:
            return self.model.objects.all()
        else:
            return self.model.objects.none()


class NewCourseView(AllowedUserTypesMixin, SuccessMessageMixin, CreateView):
    form_class = NewCourseForm
    template_name = 'main_app/new_course.html'
    success_message = _('Course created successfully')
    success_url = reverse_lazy('main_app:course_list')
    allowed_user_types = [UserType.CHAIRMAN, UserType.ADMIN]

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        new_course = form.save(commit=False)
        new_course.mother_department = UserType.get_department_id(self.request)
        new_course.save()
        # TODO: use API to assign maintainer and reviewer
        return super().form_valid(form)


class UpdateCourseView(SuccessMessageMixin, UpdateView):
    model = Course
    form_class = CourseIdentificationForm
    template_name = 'main_app/course_identification.html'
    success_message = _('Course updated successfully')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_step'] = '1'
        return context

    def get_success_url(self):
        return reverse_lazy('main_app:course_description', args=(self.object.pk, ))


class ReleaseCourseView(View):
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
        if form.is_valid() and formset.is_valid() and formset2.is_valid():
            saved_course = form.save()

            for form1 in formset.forms:
                if form1.is_valid():
                    obj = form1.save(commit=False)
                    obj.course = course
            formset.save()

            for form2 in formset2.forms:
                if form2.is_valid():
                    obj2 = form2.save(commit=False)
                    obj2.course = course
            formset2.save()

            messages.success(request, _('Course updated successfully'))
            return redirect(reverse_lazy('main_app:course_contents', args=(saved_course.pk, )))

    return render(request, 'main_app/course_description.html', {
        'course': course, 'form': form, 'formset': formset, 'formset2': formset2,
        'active_step': '2',
    })


def course_contents(request, pk):
    course = get_object_or_404(Course, pk=pk)

    total_self_study_hours = course.get_total_self_study_hours()

    form = CourseContentForm(request.POST or None, instance=course)

    formset = LectureTopicFormSet(request.POST or None, queryset=course.topics.filter(type=Topic.Types.LECTURE),
                                  prefix='lec_topics', form_kwargs={'course': course, 'topic_type': 'lec'})

    formset2 = None
    if course.get_min_lab_contact_hours_for_topics():  # only include lab topics if there is a lab in the course
        formset2 = LabTopicFormSet(request.POST or None, queryset=course.topics.filter(type=Topic.Types.LAB),
                                   prefix='lab_topics', form_kwargs={'course': course, 'topic_type': 'lab'})

    if request.method == 'POST':
        if form.is_valid() and formset.is_valid() and (formset2.is_valid() if formset2 else True):
            saved_course = form.save()

            for form1 in formset.forms:
                if form1.is_valid():
                    obj = form1.save(commit=False)
                    obj.type = Topic.Types.LECTURE
                    obj.course = course
            formset.save()

            if formset2:
                for form2 in formset2.forms:
                    if form2.is_valid():
                        obj = form2.save(commit=False)
                        obj.type = Topic.Types.LAB
                        obj.course = course
                formset2.save()

            messages.success(request, _('Course updated successfully'))
            return redirect(reverse_lazy('main_app:assessment_tasks', args=(saved_course.pk, )))

    return render(request, 'main_app/course_contents.html', {
        'course': course, 'form': form, 'formset': formset, 'formset2': formset2,
        'active_step': '3',
        'total_self_study_hours': total_self_study_hours,
    })


def assessment_tasks(request, pk):
    course = get_object_or_404(Course, pk=pk)

    formset = AssessmentTaskFormSet(request.POST or None,
                                    queryset=course.assessment_tasks.filter(type=AssessmentTask.Types.LECTURE),
                                    prefix='lecture', form_kwargs={'task_type': AssessmentTask.Types.LECTURE})

    formset2 = AssessmentTaskFormSet(request.POST or None,
                                     queryset=course.assessment_tasks.filter(type=AssessmentTask.Types.LAB),
                                     prefix='lab', form_kwargs={'task_type': AssessmentTask.Types.LAB})

    if request.method == 'POST':
        if formset.is_valid() and formset2.is_valid():
            for form1 in formset.forms:
                if form1.is_valid():
                    obj = form1.save(commit=False)
                    obj.course = course
            formset.save()

            for form2 in formset2.forms:
                if form2.is_valid():
                    obj2 = form2.save(commit=False)
                    obj2.course = course
            formset2.save()

            messages.success(request, _('Course updated successfully'))
            return redirect(reverse_lazy('main_app:learning_resources', args=(course.pk, )))

    return render(request, 'main_app/assessment_tasks.html', {
        'course': course, 'formset': formset, 'formset2': formset2,
        'active_step': '4',
    })


class LearningResourcesView(SuccessMessageMixin, UpdateView):
    model = Course
    form_class = LearningResourcesForm
    template_name = 'main_app/learning-resources.html'
    success_message = _('Course updated successfully')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_step'] = '5'
        return context

    def get_success_url(self):
        return reverse_lazy('main_app:evaluation', args=(self.object.pk, ))


class EvaluationView(SuccessMessageMixin, UpdateView):
    model = Course
    form_class = EvaluationForm
    template_name = 'main_app/evaluation.html'
    success_message = _('Course updated successfully')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_step'] = '6'
        return context

    def get_success_url(self):
        return reverse_lazy('main_app:accreditation_requirements', args=(self.object.pk, ))


def accreditation_requirements(request, pk):
    course = get_object_or_404(Course, pk=pk)

    form = AccreditationRequirementsForm(request.POST or None, instance=course)

    formset = FacilitiesRequiredFormSet(request.POST or None, queryset=course.facilities_required.all())

    if request.method == 'POST':
        if form.is_valid() and formset.is_valid():
            saved_course = form.save()

            for form1 in formset.forms:
                if form1.is_valid():
                    obj = form1.save(commit=False)
                    obj.course = course
            formset.save()

            messages.success(request, _('Course updated successfully'))
            return redirect(reverse_lazy('main_app:course_list'))

    return render(request, 'main_app/accreditation_requirements.html', {
        'course': course, 'form': form, 'formset': formset,
        'active_step': '7',
    })
