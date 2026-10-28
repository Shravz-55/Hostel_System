from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from .models import Warden
from .decorators import admin_required, warden_required
from students.models import Student
from rooms.models import Room
from fees.models import Fee
from complaints.models import Complaint


def home(request):
    return render(request, 'accounts/home.html')


# ==================== ADMIN AUTH ====================

def admin_login(request):
    if request.session.get('is_admin'):
        return redirect('accounts:admin_dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        errors = {}
        if not username:
            errors['username'] = 'Username is required.'
        if not password:
            errors['password'] = 'Password is required.'

        if errors:
            return render(request, 'accounts/admin_login.html', {'errors': errors})

        if username == settings.ADMIN_USERNAME and password == settings.ADMIN_PASSWORD:
            request.session['is_admin'] = True
            request.session['admin_username'] = username
            messages.success(request, 'Welcome Admin!')
            return redirect('accounts:admin_dashboard')
        else:
            errors['general'] = 'Invalid username or password.'
            return render(request, 'accounts/admin_login.html', {'errors': errors})

    return render(request, 'accounts/admin_login.html')


def admin_logout(request):
    if request.method == 'POST':
        request.session.flush()
        messages.success(request, 'Logged out successfully.')
    return redirect('accounts:admin_login')


@admin_required
def admin_dashboard(request):
    context = {
        'total_students': Student.objects.count(),
        'total_rooms': Room.objects.count(),
        'available_rooms': Room.objects.filter(available_beds__gt=0).count(),
        'pending_fees': Fee.objects.filter(status='Pending').count(),
        'pending_complaints': Complaint.objects.filter(status='Pending').count(),
        'total_wardens': Warden.objects.count(),
    }
    return render(request, 'accounts/admin_dashboard.html', context)


# ==================== WARDEN MANAGEMENT (Admin) ====================

@admin_required
def warden_list(request):
    wardens = Warden.objects.all()
    return render(request, 'accounts/warden_list.html', {'wardens': wardens})


@admin_required
def warden_add(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        photo = request.FILES.get('photo')

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
        if not username:
            errors['username'] = 'Username is required.'
        elif Warden.objects.filter(username=username).exists():
            errors['username'] = 'Username already exists.'
        if not password:
            errors['password'] = 'Password is required.'
        elif len(password) < 6:
            errors['password'] = 'Password must be at least 6 characters.'

        if photo:
            allowed_types = ['image/jpeg', 'image/png', 'image/gif']
            if photo.content_type not in allowed_types:
                errors['photo'] = 'Only JPEG, PNG, and GIF images are allowed.'

        if errors:
            return render(request, 'accounts/warden_add.html', {
                'errors': errors,
                'form_data': request.POST
            })

        warden = Warden(
            name=name,
            email=email,
            phone=phone,
            username=username,
            password=make_password(password),
            photo=photo
        )
        warden.save()
        messages.success(request, 'Warden added successfully.')
        return redirect('accounts:warden_list')

    return render(request, 'accounts/warden_add.html')


@admin_required
def warden_delete(request, pk):
    if request.method == 'POST':
        warden = get_object_or_404(Warden, pk=pk)
        warden.delete()
        messages.success(request, 'Warden deleted successfully.')
    return redirect('accounts:warden_list')


# ==================== WARDEN AUTH ====================

def warden_login(request):
    if request.session.get('is_warden'):
        return redirect('accounts:warden_dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        errors = {}
        if not username:
            errors['username'] = 'Username is required.'
        if not password:
            errors['password'] = 'Password is required.'

        if errors:
            return render(request, 'accounts/warden_login.html', {'errors': errors})

        try:
            warden = Warden.objects.get(username=username)
            if check_password(password, warden.password):
                request.session['is_warden'] = True
                request.session['warden_id'] = warden.id
                request.session['warden_name'] = warden.name
                messages.success(request, f'Welcome {warden.name}!')
                return redirect('accounts:warden_dashboard')
            else:
                errors['general'] = 'Invalid username or password.'
        except Warden.DoesNotExist:
            errors['general'] = 'Invalid username or password.'

        return render(request, 'accounts/warden_login.html', {'errors': errors})

    return render(request, 'accounts/warden_login.html')


def warden_logout(request):
    if request.method == 'POST':
        request.session.flush()
        messages.success(request, 'Logged out successfully.')
    return redirect('accounts:warden_login')


@warden_required
def warden_dashboard(request):
    context = {
        'total_students': Student.objects.count(),
        'students_without_room': Student.objects.filter(room__isnull=True).count(),
        'total_rooms': Room.objects.count(),
        'pending_fees': Fee.objects.filter(status='Pending').count(),
        'pending_complaints': Complaint.objects.filter(status='Pending').count(),
    }
    return render(request, 'accounts/warden_dashboard.html', context)


# ==================== STUDENT AUTH ====================

def student_login(request):
    if request.session.get('is_student'):
        return redirect('accounts:student_dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        errors = {}
        if not username:
            errors['username'] = 'Username is required.'
        if not password:
            errors['password'] = 'Password is required.'

        if errors:
            return render(request, 'accounts/student_login.html', {'errors': errors})

        try:
            student = Student.objects.get(username=username)
            if check_password(password, student.password):
                request.session['is_student'] = True
                request.session['student_id'] = student.id
                request.session['student_name'] = student.name
                messages.success(request, f'Welcome {student.name}!')
                return redirect('accounts:student_dashboard')
            else:
                errors['general'] = 'Invalid username or password.'
        except Student.DoesNotExist:
            errors['general'] = 'Invalid username or password.'

        return render(request, 'accounts/student_login.html', {'errors': errors})

    return render(request, 'accounts/student_login.html')


def student_register(request):
    if request.session.get('is_student'):
        return redirect('accounts:student_dashboard')

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()
        college = request.POST.get('college', '').strip()
        course = request.POST.get('course', '').strip()
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        photo = request.FILES.get('photo')
        id_proof = request.FILES.get('id_proof')
        joining_date = request.POST.get('joining_date', '')

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
        if password != confirm_password:
            errors['confirm_password'] = 'Passwords do not match.'
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

        if errors:
            return render(request, 'accounts/student_register.html', {
                'errors': errors,
                'form_data': request.POST
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
            joining_date=joining_date
        )
        student.save()
        messages.success(request, 'Registration successful. Please login.')
        return redirect('accounts:student_login')

    return render(request, 'accounts/student_register.html')


def student_logout(request):
    if request.method == 'POST':
        request.session.flush()
        messages.success(request, 'Logged out successfully.')
    return redirect('accounts:student_login')


@admin_required
def student_dashboard(request):
    pass


from .decorators import student_required

@student_required
def student_dashboard(request):
    student_id = request.session.get('student_id')
    student = get_object_or_404(Student, pk=student_id)

    roommates = []
    if student.room:
        roommates = Student.objects.filter(room=student.room).exclude(pk=student.pk)

    pending_fees = Fee.objects.filter(student=student, status='Pending')
    my_complaints = Complaint.objects.filter(student=student)[:5]

    context = {
        'student': student,
        'roommates': roommates,
        'pending_fees': pending_fees,
        'pending_fees_count': pending_fees.count(),
        'my_complaints': my_complaints,
    }
    return render(request, 'accounts/student_dashboard.html', context)
