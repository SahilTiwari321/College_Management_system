from django.db import models
from accounts.models import TeacherProfile, StudentProfile


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    head_of_department = models.ForeignKey(
        TeacherProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='department_head'
    )
    established_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.code} - {self.name}'

    def save(self, *args, **kwargs):
        # Convert code to uppercase
        self.code = self.code.upper()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['name']


class Course(models.Model):
    SEMESTER_CHOICES = [(i, f'Semester {i}') for i in range(1, 9)]

    course_code = models.CharField(max_length=20, unique=True)
    course_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    teacher = models.ForeignKey(
        TeacherProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='teaching_courses'
    )
    credits = models.IntegerField()
    semester = models.IntegerField(choices=SEMESTER_CHOICES)
    academic_year = models.CharField(max_length=20)
    max_students = models.IntegerField(default=60)
    schedule = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.course_code} - {self.course_name}'

    def save(self, *args, **kwargs):
        # Convert course_code to uppercase
        self.course_code = self.course_code.upper()
        super().save(*args, **kwargs)

    def enrolled_count(self):
        return self.courseenrollment_set.filter(status='Enrolled').count()

    def is_full(self):
        return self.enrolled_count() >= self.max_students

    class Meta:
        ordering = ['course_code']


class CourseEnrollment(models.Model):
    STATUS_CHOICES = [
        ('Enrolled', 'Enrolled'),
        ('Dropped', 'Dropped'),
        ('Completed', 'Completed'),
    ]

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Enrolled')
    grade = models.CharField(max_length=5, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.student.student_id} - {self.course.course_code}'

    class Meta:
        unique_together = ['student', 'course']
        ordering = ['-enrollment_date']
