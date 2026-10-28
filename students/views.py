from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from .models import Student
from rooms.models import Room
from accounts.decorators import admin_required, warden_required


# ==================== ADMIN VIEWS ====================

@admin_required
def student_list(request):
    students = Student.objects.select_related('room').all()
    return render(request, 'students/student_list.html', {'students': students})


@admin_required
def student_add(request):
    rooms = Room.objects.filter(available_beds__gt=0)

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()
        college = request.POST.get('college', '').strip()
        course = request.POST.get('course', '').strip()
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        photo = request.FILES.get('photo')
        id_proof = request.FILES.get('id_proof')
        joining_date = request.POST.get('joining_date', '')
        room_id = request.POST.get('room', '')

        errors = {}

        if not name:
            errors['name'] = 'Name is required.'
        if not email:
            errors['email'] = 'Email is required.'
        else:
            try:
                validate_email(email)
            except ValidationError:
                errors['email'] = 'Enter a valid email address.'
        if not phone:
            errors['phone'] = 'Phone is required.'
        if not address:
            errors['address'] = 'Address is required.'
        if not college:
            errors['college'] = 'College is required.'
        if not course:
            errors['course'] = 'Course is required.'
        if not username:
            errors['username'] = 'Username is required.'
        elif Student.objects.filter(username=username).exists():
            errors['username'] = 'Username already exists.'
        if not password:
            errors['password'] = 'Password is required.'
        elif len(password) < 6:
            errors['password'] = 'Password must be at least 6 characters.'
        if not photo:
            errors['photo'] = 'Photo is required.'
        else:
            allowed_types = ['image/jpeg', 'image/png', 'image/gif']
            if photo.content_type not in allowed_types:
                errors['photo'] = 'Only JPEG, PNG, and GIF images are allowed.'
        if not id_proof:
            errors['id_proof'] = 'ID proof is required.'
        else:
            allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'application/pdf']
            if id_proof.content_type not in allowed_types:
                errors['id_proof'] = 'Only JPEG, PNG, GIF, and PDF files are allowed.'
        if not joining_date:
            errors['joining_date'] = 'Joining date is required.'

        room = None
        if room_id:
            try:
                room = Room.objects.get(pk=room_id)
                if room.available_beds <= 0:
                    errors['room'] = 'Selected room has no available beds.'
            except Room.DoesNotExist:
                errors['room'] = 'Selected room does not exist.'

        if errors:
            return render(request, 'students/student_add.html', {
                'errors': errors,
                'form_data': request.POST,
                'rooms': rooms
            })

        student = Student(
            name=name,
            email=email,
            phone=phone,
            address=address,
            college=college,
            course=course,
            username=username,
            password=make_password(password),
            photo=photo,
            id_proof=id_proof,
            joining_date=joining_date,
            room=room
        )
        student.save()
        messages.success(request, 'Student added successfully.')
        return redirect('students:student_list')

    return render(request, 'students/student_add.html', {'rooms': rooms})


@admin_required
def student_view(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'students/student_view.html', {'student': student})


@admin_required
def student_delete(request, pk):
    if request.method == 'POST':
        student = get_object_or_404(Student, pk=pk)
        student.delete()
        messages.success(request, 'Student deleted successfully.')
    return redirect('students:student_list')


@admin_required
def student_assign_room(request, pk):
    student = get_object_or_404(Student, pk=pk)
    rooms = Room.objects.filter(available_beds__gt=0)

    if student.room:
        messages.warning(request, 'Student already has a room assigned. Vacate first.')
        return redirect('students:student_view', pk=pk)

    if request.method == 'POST':
        room_id = request.POST.get('room', '')

        if not room_id:
            messages.error(request, 'Please select a room.')
            return render(request, 'students/student_assign_room.html', {
                'student': student,
                'rooms': rooms
            })

        try:
            room = Room.objects.get(pk=room_id)
            if room.available_beds <= 0:
                messages.error(request, 'Selected room has no available beds.')
                return render(request, 'students/student_assign_room.html', {
                    'student': student,
                    'rooms': rooms
                })

            student.room = room
            student.save()
            messages.success(request, f'Room {room.room_number} assigned to {student.name}.')
            return redirect('students:student_view', pk=pk)

        except Room.DoesNotExist:
            messages.error(request, 'Selected room does not exist.')

    return render(request, 'students/student_assign_room.html', {
        'student': student,
        'rooms': rooms
    })


@admin_required
def student_vacate_room(request, pk):
    if request.method == 'POST':
        student = get_object_or_404(Student, pk=pk)
        if student.room:
            room_number = student.room.room_number
            student.room = None
            student.save()
            messages.success(request, f'{student.name} vacated from Room {room_number}.')
        else:
            messages.warning(request, 'Student does not have a room assigned.')
    return redirect('students:student_view', pk=pk)


# ==================== WARDEN VIEWS ====================

@warden_required
def warden_student_list(request):
    filter_type = request.GET.get('filter', 'all')

    if filter_type == 'no_room':
        students = Student.objects.filter(room__isnull=True)
    elif filter_type == 'with_room':
        students = Student.objects.filter(room__isnull=False).select_related('room')
    else:
        students = Student.objects.select_related('room').all()

    return render(request, 'students/warden_student_list.html', {
        'students': students,
        'filter_type': filter_type
    })


@warden_required
def warden_student_view(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'students/warden_student_view.html', {'student': student})
