from django.contrib.auth import user_logged_in
from django.dispatch import receiver

from course_specifications.utils import UserType


@receiver(user_logged_in)
def define_session_variables(sender, request, user, **kwargs):
    UserType.set_user_type(request)
