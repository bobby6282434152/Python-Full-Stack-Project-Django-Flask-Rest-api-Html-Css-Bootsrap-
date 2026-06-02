from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from .forms import DoctorRegisterForm, PatientRegisterForm
from .models import Doctor, Patient

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')


# Doctor Register
def doctor_register(request):
    if request.method == 'POST':
        form = DoctorRegisterForm(request.POST, request.FILES)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
                return render(request, 'doctor_register.html', {'form': form})

            user = User.objects.create_user(username=username, password=password)

            doctor = form.save(commit=False)
            doctor.user = user
            doctor.save()

            messages.success(request, "Registration successful")
            return redirect('doctor_login')

    else:
        form = DoctorRegisterForm()

    return render(request, 'doctor_register.html', {'form': form})


# Doctor Login
def doctor_login(request):
    if request.method == 'POST':
        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            login(request, user)
            return redirect('home')

    return render(request, 'doctor_login.html')


# Patient Register

def patient_register(request):
    if request.method == 'POST':
        form = PatientRegisterForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')


            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
                return render(request, 'patient_register.html', {'form': form})

            user = User.objects.create_user(username=username, password=password)

            patient = form.save(commit=False)
            patient.user = user
            patient.save()

            messages.success(request, "Registration successful")
            return redirect('patient_login')

        else:
            messages.error(request, "Form is invalid")

    else:
        form = PatientRegisterForm()

    return render(request, 'patient_register.html', {'form': form})


# Patient Login

def patient_login(request):
    if request.method == 'POST':
        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )

        if user:
            login(request, user)
            return redirect('view_doctors')

    return render(request, 'patient_login.html')

def view_doctors(request):
    doctors = Doctor.objects.all()
    return render(request, 'view_doctors.html', {'doctors': doctors})

def view_patients(request):
    patients = Patient.objects.all()
    return render(request, 'view_patients.html', {'patients': patients})