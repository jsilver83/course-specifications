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
    inlines = [LearningObjectiveInlineAdmin, CourseLearningOutcomeInlineAdmin, TopicInlineAdmin,
               AssessmentTaskInlineAdmin, FacilitiesRequiredInlineAdmin]


class LearningObjectiveAdmin(SimpleHistoryAdmin):
    list_display = ('course', 'learning_objective')


class CourseLearningOutcomeAdmin(SimpleHistoryAdmin):
    list_display = ('course', 'learning_outcome')


class NewUserAdmin(UserAdminImpersonateMixin, UserAdmin):
    open_new_window = True
    pass


# admin.site.register(LearningObjective, LearningObjectiveInlineAdmin)
admin.site.register(LearningObjective, LearningObjectiveAdmin)
admin.site.register(CourseLearningOutcome, CourseLearningOutcomeAdmin)
admin.site.register(Topic)
admin.site.register(CourseRelease)
admin.site.register(Course, CourseAdmin)
