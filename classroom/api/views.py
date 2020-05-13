from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    DestroyAPIView,
)
from rest_framework.views import APIView
from classroom.api.serializers import StudentSerializer, ClassroomSerializer
from classroom.models import Student, Classroom
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class StudentListView(ListAPIView):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)


class StudentCreateView(CreateAPIView):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)


class StudentRetrieveView(RetrieveAPIView):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)


class StudentDestroyView(DestroyAPIView):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)


class ClassroomNumberAPIView(APIView):
    serializer_class = ClassroomSerializer
    lookup_field = "capacity"
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        return Classroom.objects.filter(
            student_capacity__lte=self.kwargs.get(self.lookup_field)
        )

    def get(self, request, *args, **kwargs):
        return Response(
            {
                "classes": self.serializer_class(
                    self.get_queryset(),
                    many=True
                ).data
            }
        )
