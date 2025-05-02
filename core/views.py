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


# class InstitutionView(APIView):
#     """
#     View to handle CRUD operations for the Institution model.
#     """
#     filter_backends = [django_filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
#     filterset_class = InstitutionFilter
#     search_fields = ['name', 'address']
#     ordering_fields = ['name', 'address']
#
#     def get(self, request, pk=None):
#         """
#         Retrieves a list of all institutions or a specific institution by ID.
#
#         Args:
#             request (HttpRequest): The incoming HTTP request.
#             pk (int, optional): The primary key of the institution to retrieve. Defaults to None.
#
#         Returns:
#             Response: A Response object containing the serialized institution data or a list of institution data.
#                       Returns a 404 Not Found if the institution with the given ID does not exist.
#         """
#         if pk:
#             institution = get_object_or_404(Institution, pk=pk)
#             serializer = InstitutionSerializer(institution)
#             return Response(serializer.data)
#         else:
#             institutions = Institution.objects.all()
#             queryset = self.filter_queryset(institutions) # Apply the filters
#             serializer = InstitutionSerializer(queryset, many=True)
#             return Response(serializer.data)
#
#     def post(self, request):
#         """
#         Creates a new institution.
#
#         Args:
#             request (HttpRequest): The incoming HTTP request containing the institution data.
#
#         Returns:
#             Response: A Response object containing the serialized data of the newly created institution
#                       with a 201 Created status upon success. Returns a 400 Bad Request if the
#                       provided data is invalid or violates data integrity constraints.
#         """
#         serializer = InstitutionSerializer(data=request.data)
#         if serializer.is_valid():
#             try:
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             except IntegrityError as e:
#                 return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def put(self, request, pk):
#         """
#         Updates an existing institution.
#
#         Args:
#             request (HttpRequest): The incoming HTTP request containing the updated institution data.
#             pk (int): The primary key of the institution to update.
#
#         Returns:
#             Response: A Response object containing the serialized data of the updated institution upon success.
#                       Returns a 400 Bad Request if the provided data is invalid or violates data
#                       integrity constraints. Returns a 404 Not Found if the institution with the given
#                       ID does not exist.
#         """
#         institution = get_object_or_404(Institution, pk=pk)
#         serializer = InstitutionSerializer(institution, data=request.data)
#         if serializer.is_valid():
#             try:
#                 serializer.save()
#                 return Response(serializer.data)
#             except IntegrityError as e:
#                 return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk):
#         """
#         Deletes an existing institution.
#
#         Args:
#             request (HttpRequest): The incoming HTTP request.
#             pk (int): The primary key of the institution to delete.
#
#         Returns:
#             Response: A Response object with a 204 No Content status upon successful deletion.
#                       Returns a 404 Not Found if the institution with the given ID does not exist.
#                       Returns a 500 Internal Server Error if deletion fails due to other reasons.
#         """
#         institution = get_object_or_404(Institution, pk=pk)
#         try:
#             institution.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         except Exception as e: # Consider more specific exceptions like ProtectedError
#             return Response({'error': f'Could not delete institution: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#
#     def filter_queryset(self, queryset):
#         """
#         Apply filters to the queryset.
#         """
#         for backend in list(self.filter_backends):
#             queryset = backend().filter_queryset(self.request, queryset, view=self)
#         return queryset
#
#
# class TeacherView(APIView):
#     """
#     View to handle CRUD operations for the Teacher model.
#     """
#     filter_backends = [django_filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
#     filterset_class = TeacherFilter
#     search_fields = ['first_name', 'last_name', 'email']
#     ordering_fields = ['first_name', 'last_name', 'email']
#
#     def get(self, request, pk=None):
#         """
#         Retrieves a list of all teachers or a specific teacher by ID.
#         """
#         if pk:
#             teacher = get_object_or_404(Teacher, pk=pk)
#             serializer = TeacherSerializer(teacher)
#             return Response(serializer.data)
#         else:
#             teachers = Teacher.objects.all()
#             queryset = self.filter_queryset(teachers)
#             serializer = TeacherSerializer(queryset, many=True)
#             return Response(serializer.data)
#
#     def post(self, request):
#         """
#         Creates a new teacher.
#         """
#         serializer = TeacherSerializer(data=request.data)
#         if serializer.is_valid():
#             try:
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             except IntegrityError as e:
#                 return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def put(self, request, pk):
#         """
#         Updates an existing teacher.
#         """
#         teacher = get_object_or_404(Teacher, pk=pk)
#         serializer = TeacherSerializer(teacher, data=request.data)
#         if serializer.is_valid():
#             try:
#                 serializer.save()
#                 return Response(serializer.data)
#             except IntegrityError as e:
#                 return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
#             except ValidationError as e:
#                 return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk):
#         """
#         Deletes an existing teacher.
#         """
#         teacher = get_object_or_404(Teacher, pk=pk)
#         try:
#             teacher.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         except Exception as e:
#             return Response({'error': f'Could not delete teacher: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#
#     def filter_queryset(self, queryset):
#         """
#         Apply filters to the queryset.
#         """
#         for backend in list(self.filter_backends):
#             queryset = backend().filter_queryset(self.request, queryset, view=self)
#         return queryset
#
#
#
# class StudentView(APIView):
#     """
#     View to handle CRUD operations for the Student model.
#     """
#     filter_backends = [django_filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
#     filterset_class = StudentFilter
#     search_fields = ['first_name', 'last_name', 'email']
#     ordering_fields = ['first_name', 'last_name', 'date_of_birth', 'email']
#
#     def get(self, request, pk=None):
#         """
#         Retrieves a list of all students or a specific student by ID.
#         """
#         if pk:
#             student = get_object_or_404(Student, pk=pk)
#             serializer = StudentSerializer(student)
#             return Response(serializer.data)
#         else:
#             students = Student.objects.all()
#             queryset = self.filter_queryset(students)
#             serializer = StudentSerializer(queryset, many=True)
#             return Response(serializer.data)
#
#     def post(self, request):
#         """
#         Creates a new student.
#         """
#         serializer = StudentSerializer(data=request.data)
#         if serializer.is_valid():
#             try:
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             except IntegrityError as e:
#                 return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def put(self, request, pk):
#         """
#         Updates an existing student.
#         """
#         student = get_object_or_404(Student, pk=pk)
#         serializer = StudentSerializer(student, data=request.data)
#         if serializer.is_valid():
#             try:
#                 serializer.save()
#                 return Response(serializer.data)
#             except IntegrityError as e:
#                 return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk):
#         """
#         Deletes an existing student.
#         """
#         student = get_object_or_404(Student, pk=pk)
#         try:
#             student.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         except Exception as e:
#             return Response({'error': f'Could not delete student: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#
#     def filter_queryset(self, queryset):
#         """
#         Apply filters to the queryset.
#         """
#         for backend in list(self.filter_backends):
#             queryset = backend().filter_queryset(self.request, queryset, view=self)
#         return queryset
#
#
#
# class CourseView(APIView):
#     """
#     View to handle CRUD operations for the Course model.
#     """
#     filter_backends = [django_filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
#     filterset_class = CourseFilter
#     search_fields = ['name', 'description']
#     ordering_fields = ['name']
#
#     def get(self, request, pk=None):
#         """
#         Retrieves a list of all courses or a specific course by ID.
#         """
#         if pk:
#             course = get_object_or_404(Course, pk=pk)
#             serializer = CourseSerializer(course)
#             return Response(serializer.data)
#         else:
#             courses = Course.objects.all()
#             queryset = self.filter_queryset(courses)
#             serializer = CourseSerializer(queryset, many=True)
#             return Response(serializer.data)
#
#     def post(self, request):
#         """
#         Creates a new course.
#         """
#         serializer = CourseSerializer(data=request.data)
#         if serializer.is_valid():
#             try:
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             except IntegrityError as e:
#                 return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def put(self, request, pk):
#         """
#         Updates an existing course.
#         """
#         course = get_object_or_404(Course, pk=pk)
#         serializer = CourseSerializer(course, data=request.data)
#         if serializer.is_valid():
#             try:
#                 serializer.save()
#                 return Response(serializer.data)
#             except IntegrityError as e:
#                 return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk):
#         """
#         Deletes an existing course.
#         """
#         course = get_object_or_404(Course, pk=pk)
#         try:
#             course.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         except Exception as e:
#             return Response({'error': f'Could not delete course: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#
#     def filter_queryset(self, queryset):
#         """
#         Apply filters to the queryset.
#         """
#         for backend in list(self.filter_backends):
#             queryset = backend().filter_queryset(self.request, queryset, view=self)
#         return queryset
#
#
#
# class ClassroomView(APIView):
#     """
#     View to handle CRUD operations for the Classroom model.
#     """
#     filter_backends = [django_filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
#     filterset_class = ClassroomFilter
#     search_fields = ['name']
#     ordering_fields = ['name', 'capacity']
#
#     def get(self, request, pk=None):
#         """
#         Retrieves a list of all classrooms or a specific classroom by ID.
#         """
#         if pk:
#             classroom = get_object_or_404(Classroom, pk=pk)
#             serializer = ClassroomSerializer(classroom)
#             return Response(serializer.data)
#         else:
#             classrooms = Classroom.objects.all()
#             queryset = self.filter_queryset(classrooms)
#             serializer = ClassroomSerializer(queryset, many=True)
#             return Response(serializer.data)
#
#     def post(self, request):
#         """
#         Creates a new classroom.
#         """
#         serializer = ClassroomSerializer(data=request.data)
#         if serializer.is_valid():
#             try:
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             except IntegrityError as e:
#                 return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def put(self, request, pk):
#         """
#         Updates an existing classroom.
#         """
#         classroom = get_object_or_404(Classroom, pk=pk)
#         serializer = ClassroomSerializer(classroom, data=request.data)
#         if serializer.is_valid():
#             try:
#                 serializer.save()
#                 return Response(serializer.data)
#             except IntegrityError as e:
#                 return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk):
#         """
#         Deletes an existing classroom.
#         """
#         classroom = get_object_or_404(Classroom, pk=pk)
#         try:
#             classroom.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         except Exception as e:
#             return Response({'error': f'Could not delete classroom: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#
#     def filter_queryset(self, queryset):
#         """
#         Apply filters to the queryset.
#         """
#         for backend in list(self.filter_backends):
#             queryset = backend().filter_queryset(self.request, queryset, view=self)
#         return queryset
#
#
# class EnrollmentView(APIView):
#     """
#     View to handle CRUD operations for the Enrollment model.
#     """
#     filter_backends = [django_filters.DjangoFilterBackend, filters.OrderingFilter]
#     filterset_class = EnrollmentFilter
#     ordering_fields = ['enrollment_date']
#
#     def get(self, request, pk=None):
#         """
#         Retrieves a list of all enrollments or a specific enrollment by ID.
#         """
#         if pk:
#             enrollment = get_object_or_404(Enrollment, pk=pk)
#             serializer = EnrollmentSerializer(enrollment)
#             return Response(serializer.data)
#         else:
#             enrollments = Enrollment.objects.all()
#             queryset = self.filter_queryset(enrollments)
#             serializer = EnrollmentSerializer(queryset, many=True)
#             return Response(serializer.data)
#
#     def post(self, request):
#         """
#         Creates a new enrollment.
#         """
#         serializer = EnrollmentSerializer(data=request.data)
#         if serializer.is_valid():
#             try:
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             except IntegrityError as e:
#                 return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def put(self, request, pk):
#         """
#         Updates an existing enrollment.
#         """
#         enrollment = get_object_or_404(Enrollment, pk=pk)
#         serializer = EnrollmentSerializer(enrollment, data=request.data)
#         if serializer.is_valid():
#             try:
#                 serializer.save()
#                 return Response(serializer.data)
#             except IntegrityError as e:
#                 return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk):
#         """
#         Deletes an existing enrollment.
#         """
#         enrollment = get_object_or_404(Enrollment, pk=pk)
#         try:
#             enrollment.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         except Exception as e:
#             return Response({'error': f'Could not delete enrollment: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#
#     def filter_queryset(self, queryset):
#         """
#         Apply filters to the queryset.
#         """
#         for backend in list(self.filter_backends):
#             queryset = backend().filter_queryset(self.request, queryset, view=self)
#         return queryset
#
#
# class ScheduleView(APIView):
#     """
#     View to handle CRUD operations for the Schedule model.
#     """
#     filter_backends = [django_filters.DjangoFilterBackend, filters.OrderingFilter]
#     filterset_class = EnrollmentFilter
#     ordering_fields = ['enrollment_date']
#
#     def get(self, request, pk=None):
#         """
#         Retrieves a list of all enrollments or a specific enrollment by ID.
#         """
#         if pk:
#             enrollment = get_object_or_404(Enrollment, pk=pk)
#             serializer = EnrollmentSerializer(enrollment)
#             return Response(serializer.data)
#         else:
#             enrollments = Enrollment.objects.all()
#             queryset = self.filter_queryset(enrollments)
#             serializer = EnrollmentSerializer(queryset, many=True)
#             return Response(serializer.data)
#
#     def post(self, request):
#         """
#         Creates a new enrollment.
#         """
#         serializer = EnrollmentSerializer(data=request.data)
#         if serializer.is_valid():
#             try:
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             except IntegrityError as e:
#                 return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def put(self, request, pk):
#         """
#         Updates an existing enrollment.
#         """
#         enrollment = get_object_or_404(Enrollment, pk=pk)
#         serializer = EnrollmentSerializer(enrollment, data=request.data)
#         if serializer.is_valid():
#             try:
#                 serializer.save()
#                 return Response(serializer.data)
#             except IntegrityError as e:
#                 return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk):
#         """
#         Deletes an existing enrollment.
#         """
#         enrollment = get_object_or_404(Enrollment, pk=pk)
#         try:
#             enrollment.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         except Exception as e:
#             return Response({'error': f'Could not delete enrollment: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#
#     def filter_queryset(self, queryset):
#         """
#         Apply filters to the queryset.
#         """
#         for backend in list(self.filter_backends):
#             queryset = backend().filter_queryset(self.request, queryset, view=self)
#         return queryset


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
