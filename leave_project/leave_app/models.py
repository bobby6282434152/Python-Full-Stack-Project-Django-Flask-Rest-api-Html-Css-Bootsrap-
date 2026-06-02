from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Employee(models.Model):

    ROLE_CHOICES = (
        ('Employee', 'Employee'),
        ('Manager', 'Manager'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Employee')

    def __str__(self):
        return self.name


class Leave(models.Model):

    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    reason = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def clean(self):
        if self.end_date < self.start_date:
            raise ValidationError("End date cannot be before start date")

    def __str__(self):
        return f"{self.employee.name} ({self.start_date} to {self.end_date}) - {self.status}"


# Signals
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_employee(sender, instance, created, **kwargs):
    if created:
        role = getattr(instance, 'role', 'Employee')
        Employee.objects.create(
            user=instance,
            name=instance.username,
            role=role
        )