from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView, FormView, DetailView

from course_specifications.mixins import AjaxableResponseMixin
from course_specifications.utils import UserType
from .forms import *
from .models import *
from .utils import *


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
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['can_create_course'] = bool(UserType.get_user_type(self.request) == UserType.CHAIRMAN)

        queryset = self.get_queryset()
        context['caretakers'] = get_courses_caretakers(queryset)

        if UserType.get_user_type(self.request) in (UserType.CHAIRMAN, UserType.FACULTY):
            context['department_name'] = get_department_name(UserType.get_department_id(self.request))
            college_id = get_college_id(UserType.get_department_id(self.request))
            context['college_name'] = get_college_name(college_id)

        context['can_assign_caretakers'] = context['can_create_course']
        return context

    def get_queryset(self):
        if UserType.get_user_type(self.request) in (UserType.CHAIRMAN, UserType.FACULTY):
            return self.model.objects.filter(mother_department=UserType.get_department_id(self.request))
        elif UserType.get_user_type(self.request) == UserType.NONE:
            return self.model.objects.none()
        else:
            return self.model.objects.all()


class NewCourseView(AllowedUserTypesMixin, SuccessMessageMixin, CreateView):
    form_class = NewCourseForm
    template_name = 'main_app/new_course.html'
    success_message = _('Course created successfully')
    allowed_user_types = [UserType.CHAIRMAN]

    def form_valid(self, form):
        new_course = form.save(commit=False)
        new_course.mother_department = UserType.get_department_id(self.request)
        new_course.save()
        return redirect(reverse_lazy('main_app:assign_caretakers', args=(new_course.pk, )))


class AssignCaretakersView(AllowedUserTypesMixin, SuccessMessageMixin, FormView):
    form_class = AssignCaretakersForm
    template_name = 'main_app/plain_form.html'
    success_message = _('Roles assigned successfully')
    success_url = reverse_lazy('main_app:course_list')
    allowed_user_types = [UserType.CHAIRMAN]

    course = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Assign Caretakers for Course {course}').format(course=str(self.course))
        context['sub_title'] = _('Assign Course Maintainer and Reviewer')
        return context

    def dispatch(self, request, *args, **kwargs):
        if UserType.get_user_type(request) == UserType.CHAIRMAN:
            self.course = get_object_or_404(
                Course,
                pk=kwargs.get('pk', 0),
                mother_department=UserType.get_department_id(request),
            )
        else:
            self.course = get_object_or_404(
                Course,
                pk=kwargs.get('pk', 0),
            )

        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        assign_new_maintainer(
            course=str(self.course),
            assigner=str(self.request.user),
            assignee=form.cleaned_data.get('maintainer'),
            department=self.course.mother_department,
        )
        assign_new_reviewer(
            course=str(self.course),
            assigner=str(self.request.user),
            assignee=form.cleaned_data.get('reviewer'),
            department=self.course.mother_department,
        )
        return super().form_valid(form)


class BaseUpdateCourseView(UserPassesTestMixin, SuccessMessageMixin, UpdateView):

    def test_func(self):
        return True

    @staticmethod
    def update_all_related_objects(course):
        latest_release = course.latest_release()
        if latest_release:
            latest_release.update_all_related_objects()

    def form_valid(self, form):
        super_return = super().form_valid(form)
        self.update_all_related_objects(self.object)
        return super_return


class UpdateCourseView(BaseUpdateCourseView):
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

            BaseUpdateCourseView.update_all_related_objects(saved_course)

            messages.success(request, _('Course updated successfully'))
            return redirect(reverse_lazy('main_app:course_contents', args=(saved_course.pk, )))

    return render(request, 'main_app/course_description.html', {
        'course': course, 'form': form, 'formset': formset, 'formset2': formset2,
        'active_step': '2',
    })


def course_contents(request, pk):
    course = get_object_or_404(Course, pk=pk)

    total_self_study_hours = course.get_total_self_learning_hours()

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

            BaseUpdateCourseView.update_all_related_objects(saved_course)

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

    formset2 = None
    if course.lab_contact_hours:
        formset2 = AssessmentTaskFormSet(request.POST or None,
                                         queryset=course.assessment_tasks.filter(type=AssessmentTask.Types.LAB),
                                         prefix='lab', form_kwargs={'task_type': AssessmentTask.Types.LAB})

    if request.method == 'POST':
        if formset.is_valid() and (formset2.is_valid() if formset2 else True):
            for form1 in formset.forms:
                if form1.is_valid():
                    obj = form1.save(commit=False)
                    obj.course = course
            formset.save()

            if formset2:
                for form2 in formset2.forms:
                    if form2.is_valid():
                        obj2 = form2.save(commit=False)
                        obj2.course = course
                formset2.save()

            BaseUpdateCourseView.update_all_related_objects(course)

            messages.success(request, _('Course updated successfully'))
            return redirect(reverse_lazy('main_app:learning_resources', args=(course.pk, )))

    return render(request, 'main_app/assessment_tasks.html', {
        'course': course, 'formset': formset, 'formset2': formset2,
        'active_step': '4',
    })


class LearningResourcesView(BaseUpdateCourseView):
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


class EvaluationView(BaseUpdateCourseView):
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

    latest_release = course.latest_release()
    if not latest_release or latest_release.approved is False or latest_release.approved is None:
        new_release = True
        confirm_message = _('Are you sure you want to submit this release for approval? You may NOT be able to modify '
                            'this release afterwards')
    else:
        new_release = False
        confirm_message = _('Are you sure you want to submit?')

    if request.method == 'POST':
        if form.is_valid() and formset.is_valid():
            saved_course = form.save()

            for form1 in formset.forms:
                if form1.is_valid():
                    obj = form1.save(commit=False)
                    obj.course = course
            formset.save()

            BaseUpdateCourseView.update_all_related_objects(saved_course)

            # start camunda process only if latest release is a new
            latest_release = saved_course.latest_release()
            if latest_release and latest_release.is_new():
                process_started = latest_release.start_camunda_process()

                if process_started:
                    messages.success(request, _('Course updated successfully and a new version has been added and it '
                                                'is pending approval'))
                    return redirect(reverse_lazy('main_app:course_list'))
                else:
                    messages.error(request, _('There was an issue starting the approval process. Kindly retry later or '
                                              'contact system admins to resolve this issue'))
            else:
                messages.success(request, _('Course updated successfully'))
                return redirect(reverse_lazy('main_app:course_list'))

    return render(request, 'main_app/accreditation_requirements.html', {
        'course': course, 'form': form, 'formset': formset,
        'active_step': '7', 'confirm_message': confirm_message,
    })


class BaseReviewCourseView(AllowedUserTypesMixin, DetailView):
    template_name = ''
    model = CourseRelease
    allowed_user_types = '__all__'
    title = ''
    active_step = ''
    next_url_handler = ''
    comments_sections = []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = self.object.course
        context['title'] = self.title
        context['active_step'] = self.active_step
        if self.next_url_handler:
            context['next_url'] = reverse_lazy('main_app:{}'.format(self.next_url_handler), kwargs={'pk': self.object.pk})

        context['can_comment'] = True  # TODO: use camunda to decide on this
        for counter, comments_section in enumerate(self.comments_sections):
            context['comments_section_{}'.format(counter+1)] = comments_section

        return context


class ReviewCourseView(BaseReviewCourseView):
    template_name = 'main_app/view_course/review_course.html'
    title = _('Course identification and general information')
    active_step = '1'
    next_url_handler = 'review_course_release_step2'
    comments_sections = [ApprovalComment.Sections.COURSE_IDENTIFICATION, ApprovalComment.Sections.REQUISITES,
                         ApprovalComment.Sections.MODE_OF_INSTRUCTION, ApprovalComment.Sections.OFFICE_HOURS]


class ReviewCourseStep2View(BaseReviewCourseView):
    template_name = 'main_app/view_course/review_course_step2.html'
    title = _('Course Description, Objectives & Learning Outcomes')
    active_step = '2'
    next_url_handler = 'review_course_release_step3'
    comments_sections = [ApprovalComment.Sections.DESCRIPTION, ApprovalComment.Sections.OBJECTIVES,
                         ApprovalComment.Sections.CLO]


class ReviewCourseStep3View(BaseReviewCourseView):
    template_name = 'main_app/view_course/review_course_step3.html'
    title = _('Course Contents')
    active_step = '3'
    next_url_handler = 'review_course_release_step4'
    comments_sections = [ApprovalComment.Sections.TOPICS, ApprovalComment.Sections.SELF_LEARNING,
                         ApprovalComment.Sections.SUBJECT_AREA_HRS]


class ReviewCourseStep4View(BaseReviewCourseView):
    template_name = 'main_app/view_course/review_course_step4.html'
    title = _('Assessment Tasks')
    active_step = '4'
    next_url_handler = 'review_course_release_step5'
    comments_sections = [ApprovalComment.Sections.ASSESSMENT_TASKS, ]


class ReviewCourseStep5View(BaseReviewCourseView):
    template_name = 'main_app/view_course/review_course_step5.html'
    title = _('Assessment Tasks')
    active_step = '5'
    next_url_handler = 'review_course_release_step6'
    comments_sections = [ApprovalComment.Sections.LEARNING_RESOURCES, ]


class ReviewCourseStep6View(BaseReviewCourseView):
    template_name = 'main_app/view_course/review_course_step6.html'
    title = _('Course Evaluation')
    active_step = '6'
    next_url_handler = 'review_course_release_step7'
    comments_sections = [ApprovalComment.Sections.COURSE_EVALUATION, ]


class ReviewCourseStep7View(BaseReviewCourseView):
    template_name = 'main_app/view_course/review_course_step7.html'
    title = _('Accreditation Requirements')
    active_step = '7'
    next_url_handler = 'review_checklist_form'
    comments_sections = [ApprovalComment.Sections.ACCREDITATION_REQUIREMENTS, ]


class CreateCommentView(AjaxableResponseMixin, CreateView):
    template_name = 'main_app/view_course/review_course.html'
    form_class = CreateCommentForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['section'] = ''  # we are passing null values here that will be overridden by POST data
        kwargs['course_release'] = ''  # same a s above
        return kwargs

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.commented_by = self.request.user
        return super().form_valid(form)


class ReviewChecklistFormView(BaseReviewCourseView, FormView):
    template_name = 'main_app/view_course/review_course_checklist.html'
    form_class = ReviewChecklistForm
    title = _('Actions Page')
    active_step = 'finish'
    comments_sections = [ApprovalComment.Sections.GENERAL, ]

    def test_func(self):
        return True
        course_release_id = self.kwargs['pk']
        course_release = CourseRelease.objects.filter(id=course_release_id).first()
        camunda_api = CamundaAPI(course_release.workflow_instance_id)
        task = camunda_api.get_active_task()

        return task and task['assignee'] == self.request.user.username

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        course_release_id = self.kwargs['pk']
        course_release = CourseRelease.objects.filter(id=course_release_id).first()

        if course_release.is_completed:
            messages.warning(self.request, _('Thi Approval request was completed'))
            return context

        options = []

        task_options = course_release.camunda_task_options
        for key in task_options:
            color, margin, order = self.get_css_values(key)
            options.append({
                'key': key,
                'value': task_options[key],
                'color': color,
                'margin': margin,
                'order': order
            })

        if not options:
            # add Submit button if these is no task options
            options.append({
                'key': 'submit',
                'value': _('Submit'),  # TODO: come up with aq more meaningfule genric name
                'color': 'primary',
                'margin': 'ml-4',
                'order': 1
            })

        context['task_options'] = sorted(options, key=lambda option: option['order'])

        return context

    def get_css_values(self, button_key):
        if button_key.lower().startswith('submit'):
            return 'warning', 'ml-4', 3
        elif button_key.lower().startswith('approve'):
            return 'primary', 'ml-4', 4
        elif button_key.lower().startswith('reject'):
            return 'danger', 'ml-4', 2
        else:
            return 'secondary', 'mr-auto ml-4', 1

    def form_valid(self, form):
        course_release_id = self.kwargs['pk']
        course_release = CourseRelease.objects.filter(id=course_release_id).first()

        camunda_api = CamundaAPI(course_release.workflow_instance_id)
        active_task = camunda_api.get_active_task()
        options = camunda_api.get_task_options()

        if 'submit' in self.request.POST:
            response = camunda_api.complete_current_task()
            if response.status_code == 204:
                messages.success(self.request, _('Your Decision has been submitted successfully'))
                return redirect(reverse_lazy('main_app:course_list'))
        else:
            for key in options:
                if key in self.request.POST:
                    response = camunda_api.complete_current_task(key)
                    if response.status_code == 204:
                        messages.success(self.request, _('Your Decision has been submitted successfully'))
                        return redirect(reverse_lazy('main_app:course_list'))

        messages.warning(self.request, _('Oops something wrong happened, your Decision has not been submitted'))
        return redirect(
            reverse_lazy('main_app:review_checklist_form', kwargs={"pk": course_release_id})
        )
