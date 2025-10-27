from django.db import models
from django.contrib.auth.models import User
from accounts.models import StaffProfile


class Shift(models.Model):
    SHIFT_TYPE_CHOICES = [
        ('Day', 'Day'),
        ('Evening', 'Evening'),
        ('Night', 'Night'),
        ('Custom', 'Custom'),
    ]

    shift_name = models.CharField(max_length=100)
    shift_type = models.CharField(max_length=20, choices=SHIFT_TYPE_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.shift_name} ({self.start_time} - {self.end_time})'

    class Meta:
        ordering = ['start_time']


class ShiftAssignment(models.Model):
    STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Missed', 'Missed'),
        ('Swapped', 'Swapped'),
    ]

    staff = models.ForeignKey(StaffProfile, on_delete=models.CASCADE)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    date = models.DateField()
    assigned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Scheduled')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_upcoming(self):
        from datetime import date
        return self.date >= date.today()

    def is_completed(self):
        return self.status == 'Completed'

    def __str__(self):
        return f'{self.staff.staff_id} - {self.shift.shift_name} - {self.date}'

    class Meta:
        unique_together = ['staff', 'date']
        ordering = ['-date']


class ShiftSwapRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Cancelled', 'Cancelled'),
    ]

    requester = models.ForeignKey(
        StaffProfile,
        on_delete=models.CASCADE,
        related_name='swap_requests_made'
    )
    requester_assignment = models.ForeignKey(
        ShiftAssignment,
        on_delete=models.CASCADE,
        related_name='swap_as_requester'
    )
    target_staff = models.ForeignKey(
        StaffProfile,
        on_delete=models.CASCADE,
        related_name='swap_requests_received'
    )
    target_assignment = models.ForeignKey(
        ShiftAssignment,
        on_delete=models.CASCADE,
        related_name='swap_as_target',
        null=True,
        blank=True
    )
    reason = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Swap Request: {self.requester.staff_id} <-> {self.target_staff.staff_id}'

    class Meta:
        ordering = ['-created_at']


class LeaveRequest(models.Model):
    LEAVE_TYPE_CHOICES = [
        ('Sick Leave', 'Sick Leave'),
        ('Casual Leave', 'Casual Leave'),
        ('Vacation', 'Vacation'),
        ('Emergency', 'Emergency'),
        ('Unpaid', 'Unpaid'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    staff = models.ForeignKey(StaffProfile, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    approval_date = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.staff.staff_id} - {self.leave_type} ({self.start_date} to {self.end_date})'

    class Meta:
        ordering = ['-created_at']
