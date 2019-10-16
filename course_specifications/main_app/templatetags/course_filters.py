from django import template
from django.shortcuts import get_object_or_404
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from course_specifications.utils import get_short_full_name
from main_app.forms import CreateCommentForm
from main_app.models import CourseRelease, ApprovalComment
from main_app.utils import CourseRoles

register = template.Library()


@register.filter
def can_be_edited(course, user):
    return course.can_be_edited(user)


@register.inclusion_tag('main_app/view_course/_create_comment.html', takes_context=True)
def create_comment(context, course_release_pk, comment_section):
    course_release = get_object_or_404(CourseRelease, pk=course_release_pk)
    form = CreateCommentForm(comment_section, course_release, context.request.POST or None)
    comments = ApprovalComment.objects.filter(course_release=course_release, section=comment_section)
    return {
        'form': form,
        'course_release': course_release,
        'prefix': slugify(comment_section),
        'comments': comments,
        'user': context.request.user,
    }


@register.inclusion_tag('main_app/view_course/_review_checklist.html', takes_context=True)
def review_checklist(context, course_release_pk, active_step):
    course_release = get_object_or_404(CourseRelease, pk=course_release_pk)
    return {
        'object': course_release,
        'active_step': active_step,
    }


@register.simple_tag
def maintainer(course_code, caretakers):
    for caretaker in caretakers:
        if (course_code == caretaker.get('course_code')
                and caretaker.get('role').get('code_name') == CourseRoles.MAINTAINER):
            return mark_safe('<span class="badge badge-success text-badge">{}</span>'.format(
                get_short_full_name(caretaker.get('assignee')))
            )
    return mark_safe('<span class="badge badge-danger text-badge">{}</span>'.format(_('Not Assigned')))


@register.simple_tag
def reviewer(course_code, caretakers):
    for caretaker in caretakers:
        if (course_code == caretaker.get('course_code')
                and caretaker.get('role').get('code_name') == CourseRoles.REVIEWER):
            return mark_safe('<span class="badge badge-success text-badge">{}</span>'.format(
                get_short_full_name(caretaker.get('assignee')))
            )
    return mark_safe('<span class="badge badge-danger text-badge">{}</span>'.format(_('Not Assigned')))


@register.simple_tag
def short_full_name(username):
    return get_short_full_name(username)
