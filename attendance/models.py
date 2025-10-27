from django.db import models
from accounts.models import StudentProfile, TeacherProfile
from academic.models import Course


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Late', 'Late'),
        ('Excused', 'Excused'),
    ]

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    marked_by = models.ForeignKey(TeacherProfile, on_delete=models.SET_NULL, null=True, blank=True)
    remarks = models.TextField(blank=True)
    marked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.student.student_id} - {self.course.course_code} - {self.date}'

    class Meta:
        unique_together = ['student', 'course', 'date']
        ordering = ['-date']
        indexes = [
            models.Index(fields=['student', 'course']),
            models.Index(fields=['course', 'date']),
        ]
