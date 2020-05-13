from rest_framework.serializers import ModelSerializer
from classroom.models import Student, Classroom


class StudentSerializer(ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Student


class ClassroomSerializer(ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Classroom
