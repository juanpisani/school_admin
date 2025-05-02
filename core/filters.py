# core/filters.py
import django_filters
from django_filters import rest_framework as filters
from .models import Institution, Teacher, Student, Course, Classroom, Enrollment, Schedule


class InstitutionFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    address = filters.CharFilter(field_name='address', lookup_expr='icontains')

    class Meta:
        model = Institution
        fields = ['name', 'address']


class TeacherFilter(filters.FilterSet):
    first_name = filters.CharFilter(field_name='first_name', lookup_expr='icontains')
    last_name = filters.CharFilter(field_name='last_name', lookup_expr='icontains')
    email = filters.CharFilter(field_name='email', lookup_expr='icontains')
    institution = filters.NumberFilter(field_name='institution')
    courses = filters.NumberFilter(field_name='courses')

    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'email', 'institution', 'courses']


class StudentFilter(filters.FilterSet):
    first_name = filters.CharFilter(field_name='first_name', lookup_expr='icontains')
    last_name = filters.CharFilter(field_name='last_name', lookup_expr='icontains')
    email = filters.CharFilter(field_name='email', lookup_expr='icontains')
    institution = filters.NumberFilter(field_name='institution')
    date_of_birth = django_filters.DateFilter(field_name='date_of_birth')
    date_of_birth__gt = django_filters.DateFilter(field_name='date_of_birth', lookup_expr='gt')
    date_of_birth__lt = django_filters.DateFilter(field_name='date_of_birth', lookup_expr='lt')
    course = filters.NumberFilter(field_name='enrollments__course')


    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'institution', 'date_of_birth', 'course']


class CourseFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    institution = filters.NumberFilter(field_name='institution')
    primary_teacher = filters.NumberFilter(field_name='primary_teacher')
    student = filters.NumberFilter(field_name='enrollments__student')

    class Meta:
        model = Course
        fields = ['name', 'institution', 'primary_teacher', 'student']


class ClassroomFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    institution = filters.NumberFilter(field_name='institution')
    course = filters.NumberFilter(field_name='course') # Added course

    class Meta:
        model = Classroom
        fields = ['name', 'institution', 'course']


class EnrollmentFilter(filters.FilterSet):
    student = filters.NumberFilter(field_name='student')
    course = filters.NumberFilter(field_name='course')
    enrollment_date = django_filters.DateFilter(field_name='enrollment_date')
    enrollment_date__gt = django_filters.DateFilter(field_name='enrollment_date', lookup_expr='gt')
    enrollment_date__lt = django_filters.DateFilter(field_name='enrollment_date', lookup_expr='lt')

    class Meta:
        model = Enrollment
        fields = ['student', 'course', 'enrollment_date']


class ScheduleFilter(filters.FilterSet):
    course = filters.NumberFilter(field_name='course')
    day_of_week = filters.NumberFilter(field_name='day_of_week')
    start_time = django_filters.TimeFilter(field_name='start_time')
    start_time__gt = django_filters.TimeFilter(field_name='start_time', lookup_expr='gt')
    start_time__lt = django_filters.TimeFilter(field_name='start_time', lookup_expr='lt')
    end_time = django_filters.TimeFilter(field_name='end_time')
    end_time__gt = django_filters.TimeFilter(field_name='end_time', lookup_expr='gt')
    end_time__lt = django_filters.TimeFilter(field_name='end_time', lookup_expr='lt')
    classroom = filters.NumberFilter(field_name='classroom')

    class Meta:
        model = Schedule
        fields = ['course', 'day_of_week', 'start_time', 'end_time', 'classroom']
