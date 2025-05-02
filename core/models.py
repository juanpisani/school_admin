# core/models.py
from django.db import models

class Institution(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    address = models.TextField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.name


class Teacher(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, db_index=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='teachers')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    email = models.EmailField(unique=True, db_index=True)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='students')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Course(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    description = models.TextField(blank=True, null=True)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='courses')
    primary_teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, related_name='courses', null=True)

    def __str__(self):
        return self.name


class Classroom(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    capacity = models.IntegerField(default=30)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='classrooms')

    def __str__(self):
        return self.name


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments', db_index=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments', db_index=True)
    enrollment_date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')  # Ensure a student can't enroll in the same course twice

    def __str__(self):
        return f"{self.student} enrolled in {self.course}"


class Schedule(models.Model):
    DAY_OF_WEEK_CHOICES = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    day_of_week = models.IntegerField(
        choices=DAY_OF_WEEK_CHOICES, null=True, blank=True, db_index=True
    )
    start_time = models.TimeField()
    end_time = models.TimeField()
    classroom = models.ForeignKey(Classroom, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.course.name} on {self.get_day_of_week_display()} from {self.start_time} to {self.end_time}"
