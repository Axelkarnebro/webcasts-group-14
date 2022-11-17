from django.shortcuts import render

from .models import Course
# Create your views here.

def index(request):
    courses = Course.objects.all()
    context = {
        'title': 'List of Courses',
        'courses': courses
    }

    return render(request, 'pages/course_list.html', context)

def course_detail(request, slug):
    course = Course.objects.get(slug__exact=slug)

    context = {
        'course': course
    }

    return render(request, 'pages/course_detail.html', context)