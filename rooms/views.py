from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from accounts.decorators import admin_required, warden_required
from .models import Room


@admin_required
def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'rooms/room_list.html', {'rooms': rooms})


@admin_required
def room_add(request):
    if request.method == 'POST':
        room_number = request.POST.get('room_number', '').strip()
        room_type = request.POST.get('room_type', '').strip()
        floor = request.POST.get('floor', '').strip()
        total_beds = request.POST.get('total_beds', '').strip()
        rent = request.POST.get('rent', '').strip()
        room_image = request.FILES.get('room_image')

        errors = {}

        if not room_number:
            errors['room_number'] = 'Room number is required.'
        elif Room.objects.filter(room_number=room_number).exists():
            errors['room_number'] = 'Room number already exists.'

        if not room_type:
            errors['room_type'] = 'Room type is required.'

        if not floor:
            errors['floor'] = 'Floor is required.'
        else:
            try:
                floor = int(floor)
            except ValueError:
                errors['floor'] = 'Floor must be a valid number.'

        if not total_beds:
            errors['total_beds'] = 'Total beds is required.'
        else:
            try:
                total_beds = int(total_beds)
                if total_beds < 1:
                    errors['total_beds'] = 'Total beds must be at least 1.'
            except ValueError:
                errors['total_beds'] = 'Total beds must be a valid number.'

        if not rent:
            errors['rent'] = 'Monthly rent is required.'
        else:
            try:
                rent = float(rent)
                if rent < 0:
                    errors['rent'] = 'Rent cannot be negative.'
            except ValueError:
                errors['rent'] = 'Rent must be a valid number.'

        if room_image:
            allowed_types = ['image/jpeg', 'image/png', 'image/gif']
            if room_image.content_type not in allowed_types:
                errors['room_image'] = 'Only JPEG, PNG, and GIF images are allowed.'

        if errors:
            return render(request, 'rooms/room_add.html', {
                'errors': errors,
                'form_data': request.POST,
            })

        room = Room(
            room_number=room_number,
            room_type=room_type,
            floor=floor,
            total_beds=total_beds,
            available_beds=total_beds,
            rent=rent,
            room_image=room_image,
        )
        room.save()
        messages.success(request, 'Room added successfully.')
        return redirect('rooms:room_list')

    return render(request, 'rooms/room_add.html')


@admin_required
def room_view(request, pk):
    room = get_object_or_404(Room, pk=pk)
    students = room.students.all()
    return render(request, 'rooms/room_view.html', {'room': room, 'students': students})


@admin_required
def room_delete(request, pk):
    if request.method == 'POST':
        room = get_object_or_404(Room, pk=pk)
        if room.students.exists():
            messages.error(request, 'Cannot delete room because students are assigned to it.')
        else:
            room.delete()
            messages.success(request, 'Room deleted successfully.')
    return redirect('rooms:room_list')


@warden_required
def warden_room_list(request):
    rooms = Room.objects.all()
    return render(request, 'rooms/warden_room_list.html', {'rooms': rooms})


@warden_required
def warden_room_view(request, pk):
    room = get_object_or_404(Room, pk=pk)
    students = room.students.all()
    return render(request, 'rooms/warden_room_view.html', {'room': room, 'students': students})
