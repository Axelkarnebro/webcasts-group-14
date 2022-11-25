from django.urls import path

from .views import index, course_detail, CreateCourse#, class_detail

app_name = 'course'

urlpatterns = [
    path('', index, name='course_list'),
    # path('class/<slug:slug>', class_detail, name='class_detail'),

    # Course
    path('', index, name='course_list'),
    path('create/', CreateCourse.as_view(), name='create_course'),
    path('<slug:slug>', course_detail, name='course_detail'),
]