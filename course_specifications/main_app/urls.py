from django.urls import path

from .views import *

app_name = 'main_app'

urlpatterns = [
    path('', CoursesListView.as_view(), name='course_list'),
    path('new-course/', NewCourseView.as_view(), name='new_course'),
    path('assign-caretakers/<int:pk>/', AssignCaretakersView.as_view(), name='assign_caretakers'),
    path('update-course/<int:pk>/', UpdateCourseView.as_view(), name='update_course'),

    path('course-description/<int:pk>/', course_description, name='course_description'),
    path('course-contents/<int:pk>/', course_contents, name='course_contents'),
    path('assessment-tasks/<int:pk>/', assessment_tasks, name='assessment_tasks'),
    path('learning-resources/<int:pk>/', LearningResourcesView.as_view(), name='learning_resources'),
    path('evaluation/<int:pk>/', EvaluationView.as_view(), name='evaluation'),
    path('accreditation-requirements/<int:pk>/', accreditation_requirements, name='accreditation_requirements'),
    path('review-checklist/<int:pk>/', ReviewChecklistFormView.as_view(), name='review_checklist_form'),

    path('view-course-release/<int:pk>/', ReviewCourseView.as_view(), name='view_course_release'),

    path('review/<int:pk>/', ReviewCourseView.as_view(), name='review_course_release_step1'),
    path('review/step2/<int:pk>/', ReviewCourseStep2View.as_view(), name='review_course_release_step2'),
    path('review/step3/<int:pk>/', ReviewCourseStep3View.as_view(), name='review_course_release_step3'),
    path('review/step4/<int:pk>/', ReviewCourseView.as_view(), name='review_course_release_step4'),
    path('review/step5/<int:pk>/', ReviewCourseView.as_view(), name='review_course_release_step5'),
    path('review/step6/<int:pk>/', ReviewCourseView.as_view(), name='review_course_release_step6'),
    path('review/step7/<int:pk>/', ReviewCourseView.as_view(), name='review_course_release_step7'),

    path('new-comment/', CreateCommentView.as_view(), name='create_comment'),
]
