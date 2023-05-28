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
    status = models.IntegerField(choices=STATUS_CHOICES)
    read_sequence = models.IntegerField(default=1)
    date_inserted = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """
        Overrides the save method to update the read_sequence field to 2 automatically
        when the status changes to 'Closed' (1).
        """
        if self.status == 1 and self.read_sequence == 1:
            self.read_sequence = 2
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Returns a string representation of the reading.
        """
        return f"Reading #{self.pk} - Reading: {self.meter_reading}, Date Read: {self.reading_date}, Status: {self.get_status_display()}, Sequence: {self.read_sequence}"


    class Meta:
        """
        Meta class for the Reading model.
        """
        ordering = ['-reading_date']



class Invoice(models.Model):
    STATUS_CHOICES = [
        (0, 'Outstanding'),
        (1, 'Settled'),
    ]

    member = models.ForeignKey('Member', on_delete=models.CASCADE)
    current_reading = models.ForeignKey('Reading', on_delete=models.CASCADE, related_name='current_invoices')
    previous_reading = models.ForeignKey('Reading', on_delete=models.CASCADE, related_name='previous_invoices')
    standing_charges = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.IntegerField(choices=STATUS_CHOICES)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        """
        Returns a string representation of the invoice.
        """
        return f"Invoice #{self.pk} - Member: {self.member}, Status: {self.get_status_display()}"

    def calculate_usage(self):
        """
        Calculates the usage based on the current and previous readings.
        """
        if self.current_reading and self.previous_reading:
            usage = self.current_reading.meter_reading - self.previous_reading.meter_reading
            return usage if usage >= 0 else 0
        return 0

    def calculate_total_amount(self):
        """
        Calculates the total amount for the invoice based on usage and standing charges.
        """
        usage = self.calculate_usage()
        total_amount = usage * self.member.meter.tariff_rate + self.standing_charges
        return total_amount
