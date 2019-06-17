from django.urls import path

from .views import *

app_name = 'main_app'

urlpatterns = [
    path('', CoursesList.as_view(), name='course_list'),
    path('new-course/', NewCourse.as_view(), name='new_course'),
    path('update-course/<int:pk>/', UpdateCourse.as_view(), name='update_course'),
    path('course-description/<int:pk>/', course_description, name='course_description'),
    path('course-contents/<int:pk>/', course_contents, name='course_contents'),
    path('assessment-tasks/<int:pk>/', assessment_tasks, name='assessment_tasks'),
]
