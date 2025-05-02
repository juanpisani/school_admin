# core/tests/test_integration.py
import json
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from ..models import Institution, Teacher, Student, Course, Classroom, Enrollment, Schedule
from ..serializers import CourseSerializer

class IntegrationTests(TestCase):
    def setUp(self):
        # Create an institution
        self.institution1 = Institution.objects.create(name="Test University", address="123 Main St")
        self.institution2 = Institution.objects.create(name="Test College", address="456 Oak Ave")

        # Create teachers
        self.teacher1 = Teacher.objects.create(
            first_name="Alice", last_name="Smith", email="alice@example.com", institution=self.institution1
        )
        self.teacher2 = Teacher.objects.create(
            first_name="Bob", last_name="Smith", email="bob@example.com", institution=self.institution2
        )

        # Create students
        self.student1 = Student.objects.create(
            first_name="Bob", last_name="Johnson", date_of_birth="2002-03-15", email="bob@example.com", institution=self.institution1
        )
        self.student2 = Student.objects.create(
            first_name="Alice", last_name="Johnson", date_of_birth="2003-04-20", email="alice2@example.com", institution=self.institution1
        )
        self.student3 = Student.objects.create(
            first_name="Charlie", last_name="Brown", date_of_birth="2004-05-25", email="charlie@example.com", institution=self.institution2
        )

        # Create courses
        self.course1 = Course.objects.create(name="Introduction to Python", institution=self.institution1, primary_teacher=self.teacher1)
        self.course2 = Course.objects.create(name="Advanced Python", institution=self.institution1, primary_teacher=self.teacher1)
        self.course3 = Course.objects.create(name="Data Structures", institution=self.institution2, primary_teacher=self.teacher2)

        # Create classrooms
        self.classroom1 = Classroom.objects.create(name="Room A101", capacity=30, institution=self.institution1)
        self.classroom2 = Classroom.objects.create(name="Room B202", capacity=25, institution=self.institution2)
        self.course1.classroom = self.classroom1
        self.course1.save()
        self.course2.classroom = self.classroom1
        self.course2.save()

        #enroll students
        self.enrollment1 = Enrollment.objects.create(student=self.student1, course=self.course1)
        self.enrollment2 = Enrollment.objects.create(student=self.student1, course=self.course2)
        self.enrollment3 = Enrollment.objects.create(student=self.student2, course=self.course1)
        self.enrollment4 = Enrollment.objects.create(student=self.student3, course=self.course3)

        # Create a schedule that occupies classroom1 on Monday from 9:00 to 11:00
        self.schedule1_data = {
            "course_id": self.course1.pk,
            "day_of_week": 0,  # Monday
            "start_time": "09:00:00",
            "end_time": "11:00:00",
            "classroom_id": self.classroom1.pk,
        }
        self.schedule1 = Schedule.objects.create(**self.schedule1_data)
        # Create another schedule for the same day
        self.schedule2_data = {
            "course_id": self.course2.pk,
            "day_of_week": 0,  # Monday
            "start_time": "13:00:00",
            "end_time": "15:00:00",
            "classroom_id": self.classroom1.pk,
        }
        self.schedule2 = Schedule.objects.create(**self.schedule2_data)

    def test_enroll_student_in_course(self):
        """
        Test case: Enroll a student in a course.
        """
        enrollment_data = {
            'student_id': self.student2.pk,
            'course_id': self.course2.pk,
        }
        enrollment_url = reverse('enrollment-list')
        response = self.client.post(enrollment_url, data=json.dumps(enrollment_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Enrollment.objects.count(), 5)
        enrollment = Enrollment.objects.get(student=self.student2, course=self.course2)
        self.assertEqual(enrollment.student, self.student2)
        self.assertEqual(enrollment.course, self.course2)

    def test_assign_course_to_teacher(self):
        """
        Test case: Assign a course to a teacher.
        """
        course_url = reverse('course-detail', args=[self.course3.pk])
        updated_course_data = {
            'name': self.course3.name,
            'institution_id': self.institution2.pk,
            'primary_teacher_id': self.teacher1.pk,
        }
        response = self.client.put(course_url, data=json.dumps(updated_course_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.course3.refresh_from_db()
        self.assertEqual(self.course3.primary_teacher, self.teacher1)

    def test_get_courses_for_student(self):
        """
        Test case: Get all courses a student is enrolled in.
        """
        student_courses_url = reverse('course-list') + f'?student={self.student1.pk}'
        response = self.client.get(student_courses_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        courses = json.loads(response.content)
        self.assertEqual(len(courses), 2)
        self.assertEqual(courses[0]['id'], self.course1.pk)
        self.assertEqual(courses[1]['id'], self.course2.pk)

    def test_get_primary_teacher_for_course(self):
        """
        Test case: Get all teachers assigned to a course
        """
        course_teachers_url = reverse('teacher-list') + f'?courses={self.course1.pk}'
        response = self.client.get(course_teachers_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        teachers = json.loads(response.content)
        self.assertEqual(len(teachers), 1)
        self.assertEqual(teachers[0]['id'], self.teacher1.pk)

    def test_get_students_from_course(self):
        """
        Test case: Get all students in a classroom.
        """
        course_students_url = reverse('student-list') + f'?course={self.course1.pk}'
        response = self.client.get(course_students_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        students = json.loads(response.content)
        self.assertEqual(len(students), 2)
        self.assertEqual(students[0]['id'], self.student1.pk)
        self.assertEqual(students[1]['id'], self.student2.pk)

    def test_remove_student_from_course(self):
        """
        Test case: Remove a student from a course (delete an enrollment).
        """
        enrollment_url = reverse('enrollment-detail', args=[self.enrollment1.pk])
        response = self.client.delete(enrollment_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Enrollment.objects.count(), 3)
        student_enrollments_url = reverse('enrollment-list') + f'?student={self.student1.pk}'
        response2 = self.client.get(student_enrollments_url)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        enrollments = json.loads(response2.content)
        self.assertEqual(len(enrollments), 1)

    def test_get_courses_by_teacher(self):
        """
        Test case: Get all courses taught by a teacher.
        """
        teacher_courses_url = reverse('course-list') + f'?primary_teacher={self.teacher1.pk}'
        response = self.client.get(teacher_courses_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        courses = json.loads(response.content)
        self.assertEqual(len(courses), 2)
        self.assertEqual(courses[0]['id'], self.course1.pk)
        self.assertEqual(courses[1]['id'], self.course2.pk)

    def test_remove_teacher_from_course(self):
        """
        Test case: Remove a teacher from a course.
        """
        course_url = reverse('course-detail', args=[self.course1.pk])
        updated_course_data = {
            'name': self.course1.name,
            'institution_id': self.institution1.pk,
            'primary_teacher_id': None,
        }
        response = self.client.put(course_url, data=json.dumps(updated_course_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.course1.refresh_from_db()
        self.assertIsNone(self.course1.primary_teacher)

    def test_get_all_students_for_course(self):
        """
        Test case: Get all students for a course.
        """
        url = reverse('student-list') + f'?course={self.course1.pk}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        students = json.loads(response.content)
        self.assertEqual(len(students), 2)
        self.assertEqual(students[0]['id'], self.student1.pk)
        self.assertEqual(students[1]['id'], self.student2.pk)

    def test_classroom_is_not_available(self):
        """
        Test case: Ensure that a classroom is not available when there is an overlapping schedule
        """
        # Attempt to create a schedule that overlaps with schedule1
        new_schedule_data = {
            "course_id": self.course2.pk,  # Different course, same classroom
            "day_of_week": 0,
            "start_time": "10:00:00",  # Overlaps with schedule1 (9:00-11:00)
            "end_time": "12:00:00",
            "classroom_id": self.classroom1.pk,
        }
        url = reverse('schedule-list')
        response = self.client.post(url, data=json.dumps(new_schedule_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Schedule.objects.count(), 2) # Ensure that the schedule was not created
        self.assertIn("This classroom is not available during the specified time", str(response.data))

    def test_get_list_of_schedules_for_a_day(self):
        """
        Test case: Get all schedules for a specific day.
        """
        url = reverse('schedule-list') + '?day_of_week=0'  # 0 for Monday
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        schedules = json.loads(response.content)
        self.assertEqual(len(schedules), 2)
        self.assertEqual(schedules[0]['course']['id'], self.course1.pk)
        self.assertEqual(schedules[1]['course']['id'], self.course2.pk)

    def test_get_schedules_for_course(self):
        """
        Test case: Get all schedules for a course
        """
        url = reverse('schedule-list') + f'?course={self.course1.pk}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        schedules = json.loads(response.content)
        self.assertEqual(len(schedules), 1)
        self.assertEqual(schedules[0]['course']['id'], self.course1.pk)
