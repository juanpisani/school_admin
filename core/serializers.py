# core/serializers.py
from django.db.models import Q
from rest_framework import serializers
from rest_framework.validators import ValidationError
from .models import Institution, Teacher, Student, Course, Classroom, Enrollment, Schedule


class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = ['id', 'name', 'address']


class TeacherSerializer(serializers.ModelSerializer):
    institution = InstitutionSerializer(read_only=True)
    institution_id = serializers.IntegerField(write_only=True)

    def validate_institution_id(self, value):
        try:
            Institution.objects.get(pk=value)
        except Institution.DoesNotExist:
            raise ValidationError("Institution with this ID does not exist.")
        return value

    class Meta:
        model = Teacher
        fields = ['id', 'first_name', 'last_name', 'email', 'institution', 'institution_id', 'phone_number']


class StudentSerializer(serializers.ModelSerializer):
    institution = InstitutionSerializer(read_only=True)
    institution_id = serializers.IntegerField(write_only=True)

    def validate_institution_id(self, value):
        try:
            Institution.objects.get(pk=value)
        except Institution.DoesNotExist:
            raise ValidationError("Institution with this ID does not exist.")
        return value

    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'date_of_birth', 'email', 'institution', 'institution_id']


class ClassroomSerializer(serializers.ModelSerializer):
    institution = InstitutionSerializer(read_only=True)
    institution_id = serializers.IntegerField(write_only=True)

    def validate_institution_id(self, value):
        try:
            Institution.objects.get(pk=value)
        except Institution.DoesNotExist:
            raise ValidationError("Institution with this ID does not exist.")
        return value

    class Meta:
        model = Classroom
        fields = ['id', 'name', 'capacity', 'institution', 'institution_id']


class CourseSerializer(serializers.ModelSerializer):
    institution = InstitutionSerializer(read_only=True)
    institution_id = serializers.IntegerField(write_only=True)
    primary_teacher = TeacherSerializer(read_only=True)
    primary_teacher_id = serializers.IntegerField(write_only=True, allow_null=True)

    def validate_institution_id(self, value):
        try:
            Institution.objects.get(pk=value)
        except Institution.DoesNotExist:
            raise ValidationError("Institution with this ID does not exist.")
        return value

    def validate_primary_teacher_id(self, value):
        if value is None:
            return value
        try:
            Teacher.objects.get(pk=value)
        except Teacher.DoesNotExist:
            raise ValidationError("Teacher with this ID does not exist.")
        return value

    class Meta:
        model = Course
        fields = ['id', 'name', 'institution', 'institution_id', 'primary_teacher', 'primary_teacher_id', 'description']


class EnrollmentSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    student_id = serializers.IntegerField(write_only=True)
    course = CourseSerializer(read_only=True)
    course_id = serializers.IntegerField(write_only=True)

    def validate(self, data):
        """
        Check for an existing enrollment with the same student and course.
        """
        student_id = data.get('student_id')
        course_id = data.get('course_id')
        if student_id and course_id:
            if Enrollment.objects.filter(student_id=student_id, course_id=course_id).exists():
                raise ValidationError("An enrollment with this student and course already exists.")
        return data

    def validate_student_id(self, value):
        try:
            Student.objects.get(pk=value)
        except Student.DoesNotExist:
            raise ValidationError("Student with this ID does not exist.")
        return value

    def validate_course_id(self, value):
        try:
            Course.objects.get(pk=value)
        except Course.DoesNotExist:
            raise ValidationError("Course with this ID does not exist.")
        return value

    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'student_id', 'course', 'course_id', 'enrollment_date']


class ScheduleSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    course_id = serializers.IntegerField(write_only=True)
    day_of_week = serializers.ChoiceField(choices=Schedule.DAY_OF_WEEK_CHOICES)
    classroom = ClassroomSerializer(read_only=True, allow_null=True)
    classroom_id = serializers.IntegerField(write_only=True, allow_null=True)

    def validate(self, data):
        """
        Check for classroom availability
        """
        classroom_id = data.get('classroom_id')
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        day_of_week = data.get('day_of_week')

        if (classroom_id is not None) and (start_time is not None) and (end_time is not None) and (
                day_of_week is not None):
            # Check for any overlapping schedules
            overlapping_schedules = Schedule.objects.filter(
                Q(start_time__lt=end_time) | Q(end_time__gt=start_time),
                classroom_id=classroom_id,
                day_of_week=day_of_week,
            )
            if overlapping_schedules.exists():
                raise ValidationError("This classroom is not available during the specified time.")
        return data

    def validate_course_id(self, value):
        try:
            Course.objects.get(pk=value)
        except Course.DoesNotExist:
            raise ValidationError("Course with this ID does not exist.")
        return value

    def validate_classroom_id(self, value):
        if value is None:
            return value
        try:
            Classroom.objects.get(pk=value)
        except Classroom.DoesNotExist:
            raise ValidationError("Classroom with this ID does not exist.")
        return value

    class Meta:
        model = Schedule
        fields = ['id', 'course', 'course_id', 'day_of_week', 'start_time', 'end_time', 'classroom', 'classroom_id']
