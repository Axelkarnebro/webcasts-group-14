from django.shortcuts import render

from .models import Course
from django.views.generic import CreateView
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User

# Create your views here.

def index(request):
    courses = Course.objects.all()
    context = {
        'title': 'List of Courses',
        'courses': courses
    }

    return render(request, 'pages/course_list.html', context)


class CreateCourse(CreateView):
    model = Course
    template_name = 'pages/course_create.html'
    fields = ['title','price','short_desc','desc','status']

    #@permission_required('course.add_course', raise_exception=True)
    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.title)
        response = super(CreateCourse, self).form_valid(form)
        return response

    def get_success_url(self):
        return reverse('course:course_list')

def course_detail(request, slug):
    course = Course.objects.get(slug__exact=slug)

    context = {
        'course': course
    }

    return render(request, 'pages/course_detail.html', context)

