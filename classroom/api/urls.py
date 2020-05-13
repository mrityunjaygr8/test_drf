from django.urls import path
from classroom.api.views import (
    StudentListView,
    StudentCreateView,
    StudentDestroyView,
    StudentRetrieveView,
    ClassroomNumberAPIView
)


urlpatterns = [
    path(
        'students/list/',
        StudentListView.as_view(),
        name='student_list_api'
    ),
    path(
        'students/create/',
        StudentCreateView.as_view(),
        name='student_create_api'
    ),
    path(
        'students/<int:pk>/',
        StudentRetrieveView.as_view(),
        name='student_retrieve_api'
    ),
    path(
        'students/<int:pk>/delete',
        StudentDestroyView.as_view(),
        name='student_destroy_api'
    ),
    path(
        'class/<int:capacity>/',
        ClassroomNumberAPIView.as_view(),
        name='class_qs_api'
    ),
]