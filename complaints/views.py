from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Complaint
from students.models import Student
from accounts.decorators import admin_required, warden_required, student_required


# ==================== ADMIN VIEWS ====================

@admin_required
def complaint_list(request):
    complaints = Complaint.objects.select_related('student').all()

    status_filter = request.GET.get('status', '')
    if status_filter in ['Pending', 'Resolved']:
        complaints = complaints.filter(status=status_filter)

    return render(request, 'complaints/complaint_list.html', {
        'complaints': complaints,
        'status_filter': status_filter
    })


@admin_required
def complaint_view(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    return render(request, 'complaints/complaint_view.html', {'complaint': complaint})


@admin_required
def complaint_resolve(request, pk):
    if request.method == 'POST':
        complaint = get_object_or_404(Complaint, pk=pk)
        complaint.status = 'Resolved'
        complaint.save()
        messages.success(request, 'Complaint marked as resolved.')
    return redirect('complaints:complaint_list')


# ==================== WARDEN VIEWS ====================

@warden_required
def warden_complaint_list(request):
    complaints = Complaint.objects.select_related('student').all()

    status_filter = request.GET.get('status', '')
    if status_filter in ['Pending', 'Resolved']:
        complaints = complaints.filter(status=status_filter)

    return render(request, 'complaints/warden_complaint_list.html', {
        'complaints': complaints,
        'status_filter': status_filter
    })


@warden_required
def warden_complaint_view(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    return render(request, 'complaints/warden_complaint_view.html', {'complaint': complaint})


@warden_required
def warden_complaint_resolve(request, pk):
    if request.method == 'POST':
        complaint = get_object_or_404(Complaint, pk=pk)
        complaint.status = 'Resolved'
        complaint.save()
        messages.success(request, 'Complaint marked as resolved.')
    return redirect('complaints:warden_complaint_list')


# ==================== STUDENT VIEWS ====================

@student_required
def student_complaint_list(request):
    student_id = request.session.get('student_id')
    student = get_object_or_404(Student, pk=student_id)
    complaints = Complaint.objects.filter(student=student)

    return render(request, 'complaints/student_complaint_list.html', {
        'complaints': complaints
    })


@student_required
def student_complaint_add(request):
    student_id = request.session.get('student_id')
    student = get_object_or_404(Student, pk=student_id)

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()

        errors = {}

        if not title:
            errors['title'] = 'Title is required.'
        elif len(title) > 200:
            errors['title'] = 'Title must be less than 200 characters.'

        if not description:
            errors['description'] = 'Description is required.'

        if errors:
            return render(request, 'complaints/student_complaint_add.html', {
                'errors': errors,
                'form_data': request.POST
            })

        complaint = Complaint(
            student=student,
            title=title,
            description=description,
            status='Pending'
        )
        complaint.save()
        messages.success(request, 'Complaint submitted successfully.')
        return redirect('complaints:student_complaint_list')

    return render(request, 'complaints/student_complaint_add.html')


@student_required
def student_complaint_view(request, pk):
    student_id = request.session.get('student_id')
    complaint = get_object_or_404(Complaint, pk=pk, student_id=student_id)
    return render(request, 'complaints/student_complaint_view.html', {'complaint': complaint})
