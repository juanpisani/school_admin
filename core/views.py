# core/views.py
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from .models import Institution, Teacher, Student, Course, Classroom, Enrollment, Schedule
from .serializers import (
    InstitutionSerializer,
    TeacherSerializer,
    StudentSerializer,
    CourseSerializer,
    ClassroomSerializer,
    EnrollmentSerializer, ScheduleSerializer,
)
from .filters import (
    InstitutionFilter,
    TeacherFilter,
    StudentFilter,
    CourseFilter,
    ClassroomFilter,
    EnrollmentFilter, ScheduleFilter,
)

class InstitutionViewSet(viewsets.ModelViewSet):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = InstitutionFilter


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TeacherFilter


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = StudentFilter


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CourseFilter


class ClassroomViewSet(viewsets.ModelViewSet):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ClassroomFilter


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EnrollmentFilter


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ScheduleFilter
