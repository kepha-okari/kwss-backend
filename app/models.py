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
