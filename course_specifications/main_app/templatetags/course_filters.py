from django import template


register = template.Library()


@register.filter
def can_be_edited(course, user):
    return course.can_be_edited(user)
