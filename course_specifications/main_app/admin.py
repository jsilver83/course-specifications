from django.contrib import admin

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


# admin.site.register(LearningObjective, LearningObjectiveInlineAdmin)
admin.site.register(LearningObjective, LearningObjectiveAdmin)
admin.site.register(CourseLearningOutcome, CourseLearningOutcomeAdmin)
admin.site.register(Topic)
admin.site.register(CourseRelease)
admin.site.register(Course, CourseAdmin)
