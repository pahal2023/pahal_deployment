from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .utils import register, mail_credentials, mail_suspension, mail_removing_suspension
from .decorators import allowed_users
from django.db import transaction
from .models import Volunteer, Task
from .forms import AddTask
import json

@allowed_users(allowed_roles=['admin'])
def add_task(request):
    if request.method == 'POST':
        form = AddTask(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, f"Task has been successfully assigned.")
            return redirect('/dashboard/add-tasks')
        else:
            messages.error(request, "Unable to assign task due to internal service error.")
    else: form = AddTask()
    return render(request, 'dashboard/add_task.html', {'form':form})


@allowed_users(allowed_roles=['admin'])
def all_volunteers(request):
    volunteers = Volunteer.objects.filter(status__in=['approved', 'suspended'])
    return render(request, 'dashboard/volunteers.html', {'volunteers': volunteers})

@allowed_users(allowed_roles=['admin'])
def edit_volunteer(request, reg_no):
    volunteer = get_object_or_404(Volunteer, Reg_no=reg_no)
    user = User.objects.get(username=volunteer.user)
    user_group = str(user.groups.all()[0])

    if request.method == 'POST':
        try:
            with transaction.atomic():
                # updating to group - user is either teacher or admin
                group = Group.objects.get(name=request.POST.get("groups", ''))
                user.groups.clear()
                user.groups.add(group)

                # Check for duplicate email (excluding current volunteer)
                email = request.POST.get('email', '').strip()
                if Volunteer.objects.exclude(Reg_no=reg_no).filter(email=email).exists():
                    messages.error(request, "A volunteer with this email already exists.")
                    return render(request, 'dashboard/edit_volunteer.html', {'volunteer': volunteer})
                
                update_fields = []
                # Getting data from form and Update volunteer fields only if changed
                for field in ["name", "designation","email", "phone_no", "interest", "experience"]:
                    new_value = request.POST.get(field, '').strip()
                    if new_value != getattr(volunteer, field):
                        setattr(volunteer, field, new_value)  # Update the field not yet saved
                        update_fields.append(field)
                
                # Handle photo upload
                if 'photo' in request.FILES:
                    photo = request.FILES['photo']
                    # Validate file size (max 5MB)
                    if photo.size > 5 * 1024 * 1024:
                        messages.error(request, "Photo size should not exceed 5MB.")
                        return render(request, 'dashboard/edit_volunteer.html', {'volunteer': volunteer})
                    
                    # Validate file type
                    allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']
                    if photo.content_type not in allowed_types:
                        messages.error(request, "Only JPEG, PNG, and GIF images are allowed.")
                        return render(request, 'dashboard/edit_volunteer.html',
                                      {'volunteer': volunteer, 'user_group':user_group})

                    # adding photos in update_fields if photo is changed
                    if not volunteer.photo or volunteer.photo.name != photo.name:
                        volunteer.photo = photo
                        update_fields.append("photo")

                volunteer.save(update_fields=update_fields)
                messages.success(request, f"Volunteer {volunteer.name} updated successfully.")
                return redirect('all_volunteers')
                
        except ValidationError as e:
            messages.error(request, f"Validation error: {str(e)}")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
    
    return render(request, 'dashboard/edit_volunteer.html', {'volunteer': volunteer, 'user_group':user_group})

@allowed_users(allowed_roles=['admin'])
def delete_volunteer(request, reg_no):
    volunteer = get_object_or_404(Volunteer, Reg_no=reg_no)

    if request.method == 'POST':
        # Delete the linked user if it exists
        if volunteer.user:
            volunteer.user.delete()

        volunteer.delete()
        messages.success(request, "Volunteer and corresponding user deleted successfully.")
        return redirect('all_volunteers')

    return render(request, 'dashboard/confirm_delete.html', {'volunteer': volunteer})

@allowed_users(allowed_roles=["admin"])
def reactivate_volunteer(request, reg_no):
    volunteer = get_object_or_404(Volunteer, Reg_no=reg_no)
    volunteer.update(status = 'approved')

    user = User.objects.get(username=volunteer.user)
    user.update(is_active = True)

    mail_removing_suspension((user.first_name + " " + user.last_name), user.email)
    messages.success(request, f"User {user.username} activated successfully.")

    return redirect('all_volunteers')

@allowed_users(allowed_roles=["admin"])
def suspend_volunteer(request, reg_no):
    volunteer = get_object_or_404(Volunteer, Reg_no=reg_no)
    volunteer.update(status = 'suspended')

    user = User.objects.get(username=volunteer.user)
    user.update(is_active = False)

    mail_suspension((user.first_name + " " + user.last_name), user.email)
    messages.success(request, f"User {user.username} deactivated successfully.")

    return redirect('all_volunteers')


@allowed_users(allowed_roles=['admin'])
def applicant_list(request):
    applicants = Volunteer.objects.filter(status__in=['pending', 'rejected'])
    return render(request, 'dashboard/applicants.html', {'applicants': applicants})

@allowed_users(allowed_roles=['admin'])
def applicant_detail(request, reg_no):
    volunteer = get_object_or_404(Volunteer, Reg_no=reg_no)
    return render(request, 'dashboard/details.html', {'volunteer': volunteer})

@allowed_users(allowed_roles=['admin'])
def approve_applicant(request, reg_no):
    volunteer = get_object_or_404(Volunteer, Reg_no=reg_no)

    if not volunteer.user:
        user = register(volunteer.name, volunteer.email)
        if not user:
            messages.error(request, "User creation failed.")
            return redirect('applicant_list')
        volunteer.user = user

    volunteer.status = 'approved'
    volunteer.save(update_fields=['status', 'user'])
    return redirect('applicant_list')

@allowed_users(allowed_roles=['admin'])
def reject_applicant(request, reg_no):
    volunteer = get_object_or_404(Volunteer, Reg_no=reg_no)
    volunteer.update(status="rejected")
    return redirect('applicant_list')
