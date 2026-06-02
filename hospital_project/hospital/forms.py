
from django import forms
from .models import Doctor, Patient

# Doctor Registration Form
class DoctorRegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Doctor
        fields = ['username', 'password', 'image', 'specialization', 'phone']
        

class PatientRegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Patient
        fields = ['username', 'password', 'age', 'disease', 'phone']