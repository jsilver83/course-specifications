from django.urls import path

from .views import *

app_name = 'main_app'

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('new-course/', NewCourse.as_view(), name='new_course')
]
