import pytest
from mixer.backend.django import mixer
from classroom.models import Student, Classroom
from rest_framework.test import APIClient
from django.test import TestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model


class TestStudentAPIViews(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(username="test", password="password")
        url = "/api-token-auth/"
        res = self.client.post(
            url,
            {
                "username": "test",
                "password": "password"
            },
            headers={
                "Content-Type": "application/json"
            }
        )
        token = res.json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

    def test_student_list_works(self):
        mixer.blend(Student, first_name="Adam")
        mixer.blend(Student, first_name="Adam")
        response = self.client.get(reverse("student_list_api"))
        assert len(response.json()) == 2
        assert response.status_code == 200

    def test_student_create(self):
        input_data = {
            "first_name": "auto",
            "last_name": "ing",
            "admission_number": 122,
            "average_score": 69.69
        }
        response = self.client.post(
            reverse("student_create_api"),
            data=input_data
        )
        assert response.json() is not None
        assert response.status_code == 201
        assert Student.objects.count() == 1

    def test_student_retrieve(self):
        mixer.blend(Student, first_name="Adam")
        response = self.client.get(
            reverse(
                "student_retrieve_api",
                kwargs={"pk": 1}
            )
        )
        assert response.json() is not None
        assert response.status_code == 200
        assert response.json()["first_name"] == "Adam"

    def test_student_delete(self):
        mixer.blend(Student, first_name="Adam")
        assert Student.objects.count() == 1
        response = self.client.delete(
            reverse(
                "student_destroy_api",
                kwargs={"pk": 1}
            )
        )

        assert response.status_code == 204
        assert Student.objects.count() == 0


@pytest.mark.django_db
class TestClassroom(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = mixer.blend(get_user_model())
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_classroom_student_capacity_filter(self):
        mixer.blend(Classroom, student_capacity=2)
        response = self.client.get(
            reverse(
                'class_qs_api',
                kwargs={"capacity": 4}
            )
        )
        assert response.json() is not None
        assert response.status_code == 200
        assert len(response.json()["classes"]) == 1

    def test_classroom_student_capacity_filter_more(self):
        mixer.blend(Classroom, student_capacity=20)
        response = self.client.get(
            reverse(
                'class_qs_api',
                kwargs={"capacity": 4}
            )
        )
        assert response.json() is not None
        assert response.status_code == 200
        assert len(response.json()["classes"]) == 0
