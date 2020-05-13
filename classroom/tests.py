from classroom.models import Student, Classroom
from mixer.backend.django import mixer
import pytest
from hypothesis import given, strategies as st
from hypothesis.extra.django import TestCase


class TestStudentModel(TestCase):
    def test_student_can_be_created(self):
        s1 = mixer.blend(Student)
        last_student = Student.objects.last()
        assert last_student == s1

    def test_str_representation(self):
        mixer.blend(Student, first_name="John", last_name="Smith")
        last_student = Student.objects.last()
        assert str(last_student) == "John Smith"

    # @given(st.characters())
    # def test_student_slug(self, first_name):
    #     mixer.blend(Student, first_name=first_name)
    #     print(first_name)
    #     assert len(Student.objects.last().username) == len(first_name)

    @given(st.floats(min_value=0.0, max_value=40.0))
    def test_grade_fail(self, average_score):
        print(average_score)
        mixer.blend(Student, average_score=average_score)
        last_student = Student.objects.last()
        assert last_student.get_grade() == "Fail"

    @given(st.floats(min_value=40.0, max_value=70.0))
    def test_grade_good(self, average_score):
        mixer.blend(Student, average_score=average_score)
        last_student = Student.objects.last()
        assert last_student.get_grade() == "Pass"

    @given(st.floats(min_value=70.0, max_value=100.0))
    def test_grade_excellent(self, average_score):
        mixer.blend(Student, average_score=average_score)
        last_student = Student.objects.last()
        assert last_student.get_grade() == "Excellent"

    @given(st.floats(min_value=100.0, exclude_min=True))
    def test_grade_error(self, average_score):
        mixer.blend(Student, average_score=average_score)
        last_student = Student.objects.last()
        assert last_student.get_grade() == "Error"


@pytest.mark.django_db
class TestClassroomModel:
    def test_classroom_string(self):
        mixer.blend(Classroom, name="test_classroom")
        assert str(Classroom.objects.last()) == "test_classroom"
