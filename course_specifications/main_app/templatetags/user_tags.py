from django import template
from django.utils.html import format_html

from course_specifications.utils import UserType, get_full_name

register = template.Library()


@register.simple_tag(takes_context=True)
def show_user_and_type(context):
    request = context['request']
    return format_html('<span class="user_name">{user_name}</span>&nbsp;&nbsp;'
                       '(<span class="user_type">{user_type}</span>)&nbsp;&nbsp;',
                       user_name=get_full_name(request.user),
                       user_type=UserType.get_user_type(request),
                       )
