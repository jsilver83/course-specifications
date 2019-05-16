from django.shortcuts import render
from django.views import View, generic
from django.shortcuts import redirect

from . import models


class CourseList(generic.ListView):
    model = models.Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'


class Release(View):
    def get(self, request, *args, **kwargs):
        course = models.Course.objects.get(id=kwargs['course_id'])
        course.release()
        return redirect('course_list')
