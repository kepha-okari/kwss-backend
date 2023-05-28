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

    def save_password(self, *args, **kwargs):
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


class Reading(models.Model):
    """
    Represents a reading for a meter at a specific date.

    Key Fields:
    - meter: ForeignKey to the Meter model representing the meter associated with the reading.
    - reading_date: DateField representing the date of the reading.
    - meter_reading: DecimalField representing the meter reading value.
    - status: IntegerField representing the status of the reading (0 for 'Pending', 1 for 'Closed').
    - read_sequence: IntegerField representing the read sequence (1 for 'Pending', 2 for 'Closed' for automating and reconciling invoices).
    - date_inserted: DateTimeField representing the date when the record was inserted to the db.
    """

    STATUS_CHOICES = [
        (0, 'Pending'),
        (1, 'Closed'),
    ]

    meter = models.ForeignKey('Meter', on_delete=models.CASCADE)
    reading_date = models.DateField()
    meter_reading = models.DecimalField(max_digits=10, decimal_places=4)
    tariff_rate = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.IntegerField(choices=STATUS_CHOICES)
    read_sequence = models.IntegerField(default=1)
    date_inserted = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.status == 1 and self.read_sequence == 1:
            self.read_sequence = 2
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Reading #{self.pk} - Reading: {self.meter_reading}, Date Read: {self.reading_date}, Status: {self.get_status_display()}, Sequence: {self.read_sequence}"


    class Meta:
        ordering = ['-reading_date']



class Invoice(models.Model):
    STATUS_CHOICES = [
        (0, 'Outstanding'),
        (1, 'Settled'),
    ]

    member = models.ForeignKey('Member', on_delete=models.CASCADE)
    current_reading = models.ForeignKey('Reading', on_delete=models.CASCADE, related_name='current_invoices')
    previous_reading = models.ForeignKey('Reading', on_delete=models.CASCADE, related_name='previous_invoices', null=True, default=0)
    standing_charges = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.IntegerField(choices=STATUS_CHOICES)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Invoice #{self.pk} - Member: {self.member}, Status: {self.get_status_display()}"

    def save(self, *args, **kwargs):
        """
        Overrides the save method to set the current and previous readings automatically based on status.
        """
        if not self.pk:  # Only perform this logic when creating a new invoice
            try:
                self.current_reading = Reading.objects.filter(meter=self.member.meter, status=0).latest('reading_date')
                self.previous_reading = Reading.objects.filter(meter=self.member.meter, status=1).latest('reading_date')
            except Reading.DoesNotExist:
                self.previous_reading = 0  # Set previous_reading to 0 if no previous reading is found

        super().save(*args, **kwargs)

    def calculate_usage(self):
        if self.current_reading and self.previous_reading and self.previous_reading != 0:
            usage = self.current_reading.meter_reading - self.previous_reading.meter_reading
            return usage if usage >= 0 else 0
        return 0

    def calculate_total_amount(self):
        usage = self.calculate_usage()
        total_amount = usage * self.member.meter.tariff_rate + self.standing_charges
        return total_amount
