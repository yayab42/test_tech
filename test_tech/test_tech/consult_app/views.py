from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Patient, Consultation, Address, AppUser, Doctor
from django.http import *
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if is_doctor(request.user):
                return redirect('patient-list')
            else:
                return patient_profile(request, username)

        else:
            messages.error(request, 'Invalid username or password.')

    elif request.method == 'GET':
        if is_doctor(request.user):
            return redirect('patient-list')
        elif request.user.is_authenticated and request.user.appuser.user_type == 'patient':
            return patient_profile(request, request.user.username)

    return render(request, 'login.html')


@login_required(login_url='login')
def patient_profile(request, username):
    patient = get_object_or_404(Patient, app_user__user__username=username)

    if not is_doctor(request.user) and request.user != patient.app_user.user:
        return redirect('patient-list')

    consultations = Consultation.objects.filter(patient=patient)

    context = {
        'patient': patient,
        'consultations': consultations,
        'is_doctor_user': is_doctor(request.user),
        'consultation_type_choices': Consultation.TYPE_CHOICES,
    }

    return render(request, 'patient-profile.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')


# Check if user is doctor or not
def is_doctor(user):
    if user.is_authenticated and user.appuser.user_type == 'doctor':
        return True


# List all the patients
@login_required
def patient_list(request):
    if not is_doctor(request.user):
        return render(request, 'access_denied.html')

    all_patients = Patient.objects.all().order_by('name')
    paginator = Paginator(all_patients, 50)

    page = request.GET.get('page')
    try:
        patients = paginator.page(page)
    except PageNotAnInteger:
        patients = paginator.page(1)
    except EmptyPage:
        patients = paginator.page(paginator.num_pages)

    return render(request, 'patient_list.html', {'patients': patients})


# Create Patient
@login_required
def patient_create(request):
    if not is_doctor(request.user):
        return render(request, 'access_denied.html')

    if request.method == 'POST':
        name = request.POST['name']
        surname = request.POST['surname']
        email = request.POST['email']
        address_data = request.POST['address']
        postal_code = request.POST['postal_code']
        city = request.POST['city']

        new_user = User(username=surname, email=email, password="password")
        new_user.save()

        new_appuser = AppUser.objects.create(user=new_user, user_type="patient")
        new_appuser.save()
        existing_address, created = Address.objects.get_or_create(address=address_data, postal_code=postal_code,
                                                                  city=city)
        existing_address.save()

        new_patient = Patient.objects.create(app_user=new_appuser, name=name, surname=surname, email=email,
                                             address=existing_address)
        new_patient.save()

        return redirect('patient-list')


# Update patient
@login_required
def patient_update(request, username):
    if not is_doctor(request.user):
        return render(request, 'access_denied.html')

    patient = get_object_or_404(Patient, app_user__user__username=username)

    if request.method == 'POST':
        name = request.POST['name']
        surname = request.POST['surname']
        email = request.POST['email']

        address_data = request.POST['address']
        postal_code = request.POST['postal_code']
        city = request.POST['city']

        existing_address = Address.objects.filter(
            address=address_data,
            postal_code=postal_code,
            city=city
        ).first()

        if existing_address:
            address = existing_address
        else:
            address = Address.objects.create(
                address=address_data,
                postal_code=postal_code,
                city=city
            )

        patient.name = name
        patient.surname = surname
        patient.email = email
        patient.address = address

        patient.save()
        return redirect('patient-list')


# Delete Patient
@login_required
def patient_delete(request, username):
    if not is_doctor(request.user):
        return render(request, 'access_denied.html')
    else:
        patient = get_object_or_404(Patient, app_user__user__username=username)
        patient.delete()
        return redirect('patient-list')


##############################

@login_required
def consultation_create(request, username):
    if not is_doctor(request.user):
        return render(request, 'access_denied.html')

    patient = get_object_or_404(Patient, app_user__user__username=username)

    if request.method == 'POST':
        date = request.POST.get('date')
        description = request.POST.get('description')
        name = request.POST.get('name')
        type = request.POST.get('type')

        doctor = Doctor.objects.get(app_user__user=request.user)

        new_consultation = Consultation.objects.create(
            patient=patient,
            doctor=doctor,
            date=timezone.now() if not date else date,
            description=description,
            name=name,
            type=type
        )
        new_consultation.save()
        return redirect('patient-profile', username=username)


@login_required
def consultation_delete(request, consultation_id):
    if not is_doctor(request.user):
        return render(request, 'access_denied.html')

    consultation = get_object_or_404(Consultation, id=consultation_id)
    consultation.delete()
    return redirect('patient-profile', username=consultation.patient.app_user.user.username)


@login_required
def consultation_update(request, username, consultation_id):
    if not is_doctor(request.user):
        return render(request, 'access_denied.html')

    patient = get_object_or_404(Patient, app_user__user__username=username)
    consultation = get_object_or_404(Consultation, id=consultation_id)

    if request.method == 'POST':
        consultation.date = request.POST.get('date')
        consultation.description = request.POST.get('description')
        consultation.name = request.POST.get('name')
        consultation.type = request.POST.get('type')

        consultation.save()

        return redirect('patient-profile', username=username)
