from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from accounts.models import StaffProfile
from workforce.models import ShiftAssignment
import uuid
import qrcode
from io import BytesIO
from django.core.files import File


class CheckInLog(models.Model):
    CHECK_IN_METHOD_CHOICES = [
        ('QR+PIN', 'QR+PIN'),
        ('Manual Admin', 'Manual Admin'),
        ('Auto', 'Auto'),
    ]

    CHECK_OUT_METHOD_CHOICES = [
        ('QR+PIN', 'QR+PIN'),
        ('Manual Admin', 'Manual Admin'),
        ('Auto', 'Auto'),
    ]

    staff = models.ForeignKey(StaffProfile, on_delete=models.CASCADE)
    shift_assignment = models.ForeignKey(
        ShiftAssignment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    check_in_time = models.DateTimeField()
    check_out_time = models.DateTimeField(null=True, blank=True)
    check_in_method = models.CharField(max_length=20, choices=CHECK_IN_METHOD_CHOICES)
    check_out_method = models.CharField(max_length=20, choices=CHECK_OUT_METHOD_CHOICES, blank=True)
    location_verified = models.BooleanField(default=False)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_duration(self):
        """Calculate duration between check-in and check-out"""
        if self.check_out_time:
            return self.check_out_time - self.check_in_time
        return None

    def is_active(self):
        """Check if still checked in (no check-out time)"""
        return self.check_out_time is None

    def is_late(self):
        """Check if checked in late compared to shift start time"""
        if self.shift_assignment:
            from datetime import datetime, timedelta
            shift_start = datetime.combine(
                self.check_in_time.date(),
                self.shift_assignment.shift.start_time
            )
            # Consider late if check-in is more than 15 minutes after shift start
            return self.check_in_time > shift_start + timedelta(minutes=15)
        return False

    def __str__(self):
        return f'{self.staff.staff_id} - {self.check_in_time.date()}'

    class Meta:
        ordering = ['-check_in_time']
        indexes = [
            models.Index(fields=['staff', 'check_in_time']),
        ]


class QRCode(models.Model):
    location_name = models.CharField(max_length=100)
    qr_code_data = models.TextField(unique=True)
    qr_code_image = models.ImageField(upload_to='qr_codes/', blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_qr_code(self):
        """Generate QR code image from qr_code_data"""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=5,
        )
        qr.add_data(self.qr_code_data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # Save to BytesIO
        buffer = BytesIO()
        img.save(buffer, 'PNG')
        buffer.seek(0)

        # Save to model
        filename = f'qr_{self.location_name.replace(" ", "_")}.png'
        self.qr_code_image.save(filename, File(buffer), save=False)

    def save(self, *args, **kwargs):
        # Generate UUID if not exists
        if not self.qr_code_data:
            self.qr_code_data = str(uuid.uuid4())

        # Generate QR code image if not exists
        if not self.qr_code_image:
            self.generate_qr_code()

        super().save(*args, **kwargs)

    def __str__(self):
        return f'QR Code - {self.location_name}'

    class Meta:
        ordering = ['-created_at']


class StaffPIN(models.Model):
    staff = models.OneToOneField(StaffProfile, on_delete=models.CASCADE)
    pin_hash = models.CharField(max_length=256)
    last_changed = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def set_pin(self, pin):
        """Hash and set PIN"""
        self.pin_hash = make_password(pin)

    def __str__(self):
        return f'PIN for {self.staff.staff_id}'

    class Meta:
        verbose_name = 'Staff PIN'
        verbose_name_plural = 'Staff PINs'
