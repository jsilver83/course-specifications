from django import template
from django.shortcuts import get_object_or_404
from django.utils.text import slugify

from main_app.forms import CreateCommentForm
from main_app.models import CourseRelease, ApprovalComments

register = template.Library()


@register.filter
def can_be_edited(course, user):
    return course.can_be_edited(user)


@register.inclusion_tag('main_app/view_course/_create_comment.html', takes_context=True)
def create_comment(context, course_release_pk, comment_section):
    course_release = get_object_or_404(CourseRelease, pk=course_release_pk)
    form = CreateCommentForm(comment_section, course_release, context.request.POST or None)
    comments = ApprovalComments.objects.filter(section=comment_section)
    return {
        'form': form,
        'course_release': course_release,
        'prefix': slugify(comment_section),
        'comments': comments,
        'user': context.request.user,
    }
