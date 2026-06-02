from django.db import models
from django.contrib.auth.models import User


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='doctor_images/')
    specialization = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.user.username

# models.py

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    disease = models.CharField(max_length=200)
    phone = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.user.username