import hashlib
from django.db import models

class Meter(models.Model):
    meter_number = models.CharField(max_length=20, unique=True)

class Member(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15, blank=False)
    id_number = models.CharField(max_length=20)
    meter = models.ForeignKey(Meter, on_delete=models.SET_NULL, null=True, blank=False)
    active = models.BooleanField(default=True)
    date_registered = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

class User(models.Model):

    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('accountant', 'Accountant'),
        ('field_agent', 'Field Agent'),
    ]
    username = models.CharField(max_length=100)
    role = models.CharField(max_length=100, choices=ROLE_CHOICES)
    password = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=15)
    active_status = models.BooleanField(default=True)
    date_created = models.DateField(auto_now_add=True)

    def make_password(self, password):
        assert password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password

    def save(self, *args, **kwargs):
        # Hash the password before saving
        if self.password:
            self.password = self.make_password(self.password)
        super().save(*args, **kwargs)

    def verify_password(self, password):
        # Verify the provided password against the stored hashed password
        hashed_password = self.make_password(password)
        return self.password == hashed_password

    def __str__(self):
        return self.username
