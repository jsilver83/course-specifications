from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from impersonate.admin import UserAdminImpersonateMixin

from .models import *
from simple_history.admin import SimpleHistoryAdmin


class LearningObjectiveInlineAdmin(admin.TabularInline):
    model = LearningObjective


class CourseLearningOutcomeInlineAdmin(admin.TabularInline):
    model = CourseLearningOutcome


class TopicInlineAdmin(admin.TabularInline):
    model = Topic


class AssessmentTaskInlineAdmin(admin.TabularInline):
    model = AssessmentTask


class FacilitiesRequiredInlineAdmin(admin.TabularInline):
    model = FacilitiesRequired


class CourseAdmin(SimpleHistoryAdmin):
    list_display = ('get_department_name', 'program_code', 'number', 'title', 'lecture_credit_hours',
                    'lab_contact_hours', 'total_credit_hours', )
    search_fields = ('program_code', 'number', 'title', )
    inlines = [LearningObjectiveInlineAdmin, CourseLearningOutcomeInlineAdmin, TopicInlineAdmin,
               AssessmentTaskInlineAdmin, FacilitiesRequiredInlineAdmin]


class CourseReleaseAdmin(admin.ModelAdmin):
    list_display = ('version', 'course', )
    search_fields = ('course__program_code', 'course__number', 'course__title', )
    readonly_fields = ('course', 'prerequisite_courses', 'corequisite_courses', 'not_to_be_taken_with_courses',
                       'learning_objectives',
                       'learning_outcomes', 'topics', 'assessment_tasks', 'facilities_required', )


class LearningObjectiveAdmin(SimpleHistoryAdmin):
    list_display = ('course', 'learning_objective')


class CourseLearningOutcomeAdmin(SimpleHistoryAdmin):
    list_display = ('course', 'learning_outcome')


class NewUserAdmin(UserAdminImpersonateMixin, UserAdmin):
    open_new_window = True
    pass


class ApprovalCommentsAdmin(admin.ModelAdmin):
    list_display = ('course_release', 'section', 'comment', 'commented_by', 'comment_date', )
    autocomplete_fields = ('course_release', )


# admin.site.register(LearningObjective, LearningObjectiveInlineAdmin)
admin.site.register(LearningObjective, LearningObjectiveAdmin)
admin.site.register(CourseLearningOutcome, CourseLearningOutcomeAdmin)
admin.site.register(Topic)
admin.site.register(CourseRelease, CourseReleaseAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(ApprovalComment, ApprovalCommentsAdmin)
