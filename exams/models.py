from django.db import models
from accounts.models import StudentProfile, TeacherProfile
from academic.models import Course


class Exam(models.Model):
    EXAM_TYPE_CHOICES = [
        ('Midterm', 'Midterm'),
        ('Final', 'Final'),
        ('Quiz', 'Quiz'),
        ('Assignment', 'Assignment'),
        ('Project', 'Project'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    exam_name = models.CharField(max_length=100)
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPE_CHOICES)
    total_marks = models.IntegerField()
    passing_marks = models.IntegerField()
    exam_date = models.DateField()
    duration = models.IntegerField(null=True, blank=True, help_text='Duration in minutes')
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(TeacherProfile, on_delete=models.SET_NULL, null=True, blank=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.exam_name} - {self.course.course_code}'

    class Meta:
        ordering = ['-exam_date']


class ExamResult(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    grade = models.CharField(max_length=5, blank=True)
    remarks = models.TextField(blank=True)
    entered_by = models.ForeignKey(TeacherProfile, on_delete=models.SET_NULL, null=True, blank=True)
    is_absent = models.BooleanField(default=False)
    entered_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_grade(self):
        """Calculate letter grade based on percentage"""
        if self.is_absent:
            return 'Ab'

        percentage = (float(self.marks_obtained) / float(self.exam.total_marks)) * 100

        if percentage >= 95:
            return 'A+'
        elif percentage >= 90:
            return 'A'
        elif percentage >= 85:
            return 'A-'
        elif percentage >= 80:
            return 'B+'
        elif percentage >= 75:
            return 'B'
        elif percentage >= 70:
            return 'B-'
        elif percentage >= 65:
            return 'C+'
        elif percentage >= 60:
            return 'C'
        elif percentage >= 55:
            return 'C-'
        elif percentage >= 50:
            return 'D'
        else:
            return 'F'

    def is_pass(self):
        """Check if student passed the exam"""
        return float(self.marks_obtained) >= float(self.exam.passing_marks)

    def save(self, *args, **kwargs):
        # Auto-calculate grade
        self.grade = self.calculate_grade()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.student.student_id} - {self.exam.exam_name}'

    class Meta:
        unique_together = ['exam', 'student']
        ordering = ['-entered_at']
