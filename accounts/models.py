from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from datetime import datetime


class StudentProfile(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    SECURITY_QUESTIONS = [
        ("What is your mother's maiden name?", "What is your mother's maiden name?"),
        ("What city were you born in?", "What city were you born in?"),
        ("What was your first pet's name?", "What was your first pet's name?"),
        ("What is your favorite book?", "What is your favorite book?"),
    ]

    SEMESTER_CHOICES = [(i, f'Semester {i}') for i in range(1, 9)]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='studentprofile')
    student_id = models.CharField(max_length=20, unique=True, editable=False)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    department = models.ForeignKey('academic.Department', on_delete=models.SET_NULL, null=True, blank=True)
    enrollment_date = models.DateField(auto_now_add=True)
    semester = models.IntegerField(choices=SEMESTER_CHOICES, default=1)
    profile_picture = models.ImageField(upload_to='students/', blank=True, null=True)
    security_question = models.CharField(max_length=200, choices=SECURITY_QUESTIONS)
    security_answer = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.student_id:
            year = datetime.now().year
            count = StudentProfile.objects.filter(student_id__startswith=f'STU-{year}').count() + 1
            self.student_id = f'STU-{year}-{count:04d}'

        # Hash security answer if not already hashed
        if self.security_answer and not self.security_answer.startswith('pbkdf2_'):
            self.security_answer = make_password(self.security_answer)

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.student_id} - {self.user.get_full_name()}'

    class Meta:
        ordering = ['-created_at']


class TeacherProfile(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    SECURITY_QUESTIONS = [
        ("What is your mother's maiden name?", "What is your mother's maiden name?"),
        ("What city were you born in?", "What city were you born in?"),
        ("What was your first pet's name?", "What was your first pet's name?"),
        ("What is your favorite book?", "What is your favorite book?"),
    ]

    QUALIFICATION_CHOICES = [
        ('PhD', 'PhD'),
        ('Masters', 'Masters'),
        ('Bachelors', 'Bachelors'),
        ('Diploma', 'Diploma'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacherprofile')
    teacher_id = models.CharField(max_length=20, unique=True, editable=False)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    department = models.ForeignKey('academic.Department', on_delete=models.SET_NULL, null=True, blank=True)
    specialization = models.CharField(max_length=100)
    qualification = models.CharField(max_length=20, choices=QUALIFICATION_CHOICES)
    date_of_joining = models.DateField()
    profile_picture = models.ImageField(upload_to='teachers/', blank=True, null=True)
    security_question = models.CharField(max_length=200, choices=SECURITY_QUESTIONS)
    security_answer = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.teacher_id:
            year = datetime.now().year
            count = TeacherProfile.objects.filter(teacher_id__startswith=f'TCH-{year}').count() + 1
            self.teacher_id = f'TCH-{year}-{count:04d}'

        # Hash security answer if not already hashed
        if self.security_answer and not self.security_answer.startswith('pbkdf2_'):
            self.security_answer = make_password(self.security_answer)

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.teacher_id} - {self.user.get_full_name()}'

    class Meta:
        ordering = ['-created_at']


class StaffProfile(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    SECURITY_QUESTIONS = [
        ("What is your mother's maiden name?", "What is your mother's maiden name?"),
        ("What city were you born in?", "What city were you born in?"),
        ("What was your first pet's name?", "What was your first pet's name?"),
        ("What is your favorite book?", "What is your favorite book?"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staffprofile')
    staff_id = models.CharField(max_length=20, unique=True, editable=False)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    position = models.CharField(max_length=100)
    date_of_joining = models.DateField()
    profile_picture = models.ImageField(upload_to='staff/', blank=True, null=True)
    security_question = models.CharField(max_length=200, choices=SECURITY_QUESTIONS)
    security_answer = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.staff_id:
            year = datetime.now().year
            count = StaffProfile.objects.filter(staff_id__startswith=f'STF-{year}').count() + 1
            self.staff_id = f'STF-{year}-{count:04d}'

        # Hash security answer if not already hashed
        if self.security_answer and not self.security_answer.startswith('pbkdf2_'):
            self.security_answer = make_password(self.security_answer)

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.staff_id} - {self.user.get_full_name()}'

    class Meta:
        ordering = ['-created_at']
