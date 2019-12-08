from django.urls import path
from .views import GeneratePDFSyllabusView,GenerateWordSyllabusView

app_name = 'syllabus'

urlpatterns = [
    path('pdf/<int:pk>/', GeneratePDFSyllabusView.as_view(), name='generate_pdf_syllabus'),
    path('word/<int:pk>/', GenerateWordSyllabusView.as_view(), name='generate_word_syllabus'),
]