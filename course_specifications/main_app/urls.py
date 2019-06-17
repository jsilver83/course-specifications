from django.urls import path

from .views import *

app_name = 'main_app'

urlpatterns = [
    path('', CoursesListView.as_view(), name='course_list'),
    path('new-course/', NewCourseView.as_view(), name='new_course'),
    path('update-course/<int:pk>/', UpdateCourseView.as_view(), name='update_course'),
    path('course-description/<int:pk>/', course_description, name='course_description'),
    path('course-contents/<int:pk>/', course_contents, name='course_contents'),
    path('assessment-tasks/<int:pk>/', assessment_tasks, name='assessment_tasks'),
    path('learning-resources/<int:pk>/', LearningResourcesView.as_view(), name='learning_resources'),
    path('evaluation/<int:pk>/', EvaluationView.as_view(), name='evaluation'),
    path('accreditation-requirements/<int:pk>/', accreditation_requirements, name='accreditation_requirements'),
]
