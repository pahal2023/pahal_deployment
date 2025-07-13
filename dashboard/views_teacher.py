from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import Student, Volunteer, Attendance, Task
from .forms import Admission, VolunteerEnrolment
from .decorators import allowed_users
from .utils import register

# Create your views here.

@login_required(login_url='/login/')
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

@login_required(login_url='/login/')
def timetable(request):
    return render(request, 'dashboard/timetable.html')

@login_required(login_url='/login/')
def tasks(request):
    task = Task.objects.filter(assignedTo=request.user)
    return render(request, 'dashboard/tasks.html', {'tasks':task})

@allowed_users(allowed_roles=['teacher','admin'])
def attendance(request):
    students = Student.objects.filter(active=1)

    if request.method == "POST":
        try:
            with transaction.atomic():
                for st in students:
                    status = request.POST.get("rollNo" + str(st.roll_no))
                    att = Attendance(student=st, status=status)
                    att.save()
            messages.success(request, "Attendance saved successfully.")
        except Exception as e:
            # Rollback transaction and display error message
            messages.error(request, "Unable to save attendance: " + str(e))

    return render(request, 'dashboard/attendance.html',{"students":students})

@allowed_users(allowed_roles=['teacher', 'admin'])
def student_info(request):
    students = Student.objects.filter()
    return render(request, 'dashboard/students_info.html', {'students':students})


@allowed_users(allowed_roles=['teacher', 'admin'])
def volunteer_info(request):
    volunteers = Volunteer.objects.filter(status='approved')  # filter only approved volunteers
    return render(request, 'dashboard/volunteer_info.html', {'volunteer': volunteers})


@allowed_users(allowed_roles=['teacher','admin'])
def admission(request):
    if request.method == 'POST':
        form = Admission(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/dashboard/student-info')
        else:
            messages.error(request, "Admission form is showing invalid.")
    return render(request, 'dashboard/admission.html')

# This fun saves all the date to volunteers db and creates registration for new volunteer.
@allowed_users(allowed_roles=['admin'])
def volunteer_enrolment(request):
    if request.method == 'POST':
        form = VolunteerEnrolment(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # register(form.instance.name, form.instance.email)  # register function is in utils.py
            return redirect('/dashboard/applicants')
        else:
            errors = []
            for field, error_list in form.errors.items():
                for error in error_list:
                    errors.append(f"{field}: {error}")
            error_message = " | ".join(errors)
            messages.error(request, f"Volunteer enrolment form errors: {error_message}")

    return render(request, 'dashboard/volunteer_enrolment.html')
