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


# class LearningObjectiveAdmin(SimpleHistoryAdmin):
#     pass


class CourseAdmin(SimpleHistoryAdmin):
    inlines = [LearningObjectiveInlineAdmin, CourseLearningOutcomeInlineAdmin, TopicInlineAdmin,
               AssessmentTaskInlineAdmin, FacilitiesRequiredInlineAdmin]


#admin.site.register(LearningObjective, LearningObjectiveInlineAdmin)
# admin.site.register(LearningObjective, LearningObjectiveAdmin)
admin.site.register(CourseRelease)
admin.site.register(Course, CourseAdmin)
