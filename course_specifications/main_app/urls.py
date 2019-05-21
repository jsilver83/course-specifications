from django.urls import path

from .views import *

app_name = 'main_app'

urlpatterns = [
    path('', CoursesList.as_view(), name='index'),
    path('new-course/', NewCourse.as_view(), name='new_course'),
    path('update-course/<int:pk>/', UpdateCourse.as_view(), name='update_course'),
    path('course-description/<int:pk>/', CourseDescription.as_view(), name='course_description'),
]
