from django.contrib.auth import user_logged_in
from django.dispatch import receiver
from impersonate.signals import session_begin, session_end

from course_specifications.utils import UserType


@receiver(user_logged_in)
@receiver(session_end)
def define_session_variables(sender, request, **kwargs):
    UserType.set_user_type(request)


@receiver(session_begin)
def define_session_variables_for_impersonator(sender, request, impersonator, impersonating, **kwargs):
    UserType.set_user_type(request, impersonating)
