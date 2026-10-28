from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from decimal import Decimal, InvalidOperation

from .models import Fee
from students.models import Student
from accounts.decorators import admin_required, warden_required, student_required


# ==================== ADMIN VIEWS ====================

@admin_required
def fee_list(request):
    fees = Fee.objects.select_related('student').all()
    students = Student.objects.all()

    status_filter = request.GET.get('status', '')
    if status_filter in ['Pending', 'Paid']:
        fees = fees.filter(status=status_filter)

    return render(request, 'fees/fee_list.html', {
        'fees': fees,
        'students': students,
        'status_filter': status_filter
    })


@admin_required
def fee_add(request):
    students = Student.objects.all()

    if request.method == 'POST':
        student_id = request.POST.get('student', '')
        month = request.POST.get('month', '').strip()
        amount = request.POST.get('amount', '')

        errors = {}

        if not student_id:
            errors['student'] = 'Student is required.'
        else:
            try:
                student = Student.objects.get(pk=student_id)
            except Student.DoesNotExist:
                errors['student'] = 'Student does not exist.'

        if not month:
            errors['month'] = 'Month is required.'

        if not amount:
            errors['amount'] = 'Amount is required.'
        else:
            try:
                amount = Decimal(amount)
                if amount <= 0:
                    errors['amount'] = 'Amount must be greater than 0.'
            except InvalidOperation:
                errors['amount'] = 'Amount must be a valid number.'

        if errors:
            return render(request, 'fees/fee_add.html', {
                'errors': errors,
                'form_data': request.POST,
                'students': students
            })

        fee = Fee(
            student=student,
            month=month,
            amount=amount,
            status='Pending'
        )
        fee.save()
        messages.success(request, 'Fee added successfully.')
        return redirect('fees:fee_list')

    return render(request, 'fees/fee_add.html', {'students': students})


@admin_required
def fee_mark_paid(request, pk):
    if request.method == 'POST':
        fee = get_object_or_404(Fee, pk=pk)
        fee.status = 'Paid'
        fee.payment_date = timezone.now().date()
        fee.save()
        messages.success(request, 'Fee marked as paid.')
    return redirect('fees:fee_list')


@admin_required
def fee_delete(request, pk):
    if request.method == 'POST':
        fee = get_object_or_404(Fee, pk=pk)
        fee.delete()
        messages.success(request, 'Fee deleted successfully.')
    return redirect('fees:fee_list')


# ==================== WARDEN VIEWS ====================

@warden_required
def warden_fee_list(request):
    fees = Fee.objects.select_related('student').all()
    students = Student.objects.all()

    status_filter = request.GET.get('status', '')
    if status_filter in ['Pending', 'Paid']:
        fees = fees.filter(status=status_filter)

    return render(request, 'fees/warden_fee_list.html', {
        'fees': fees,
        'students': students,
        'status_filter': status_filter
    })


@warden_required
def warden_fee_add(request):
    students = Student.objects.all()

    if request.method == 'POST':
        student_id = request.POST.get('student', '')
        month = request.POST.get('month', '').strip()
        amount = request.POST.get('amount', '')

        errors = {}

        if not student_id:
            errors['student'] = 'Student is required.'
        else:
            try:
                student = Student.objects.get(pk=student_id)
            except Student.DoesNotExist:
                errors['student'] = 'Student does not exist.'

        if not month:
            errors['month'] = 'Month is required.'

        if not amount:
            errors['amount'] = 'Amount is required.'
        else:
            try:
                amount = Decimal(amount)
                if amount <= 0:
                    errors['amount'] = 'Amount must be greater than 0.'
            except InvalidOperation:
                errors['amount'] = 'Amount must be a valid number.'

        if errors:
            return render(request, 'fees/warden_fee_add.html', {
                'errors': errors,
                'form_data': request.POST,
                'students': students
            })

        fee = Fee(
            student=student,
            month=month,
            amount=amount,
            status='Pending'
        )
        fee.save()
        messages.success(request, 'Fee added successfully.')
        return redirect('fees:warden_fee_list')

    return render(request, 'fees/warden_fee_add.html', {'students': students})


@warden_required
def warden_fee_mark_paid(request, pk):
    if request.method == 'POST':
        fee = get_object_or_404(Fee, pk=pk)
        fee.status = 'Paid'
        fee.payment_date = timezone.now().date()
        fee.save()
        messages.success(request, 'Fee marked as paid.')
    return redirect('fees:warden_fee_list')


# ==================== STUDENT VIEWS ====================

@student_required
def student_fee_list(request):
    student_id = request.session.get('student_id')
    student = get_object_or_404(Student, pk=student_id)
    fees = Fee.objects.filter(student=student)

    pending_total = fees.filter(status='Pending').aggregate(
        total=models.Sum('amount')
    )['total'] or 0

    return render(request, 'fees/student_fee_list.html', {
        'fees': fees,
        'pending_total': pending_total
    })


@student_required
def student_pay_fee(request, pk):
    if request.method == 'POST':
        student_id = request.session.get('student_id')
        fee = get_object_or_404(Fee, pk=pk, student_id=student_id)

        if fee.status == 'Pending':
            fee.status = 'Paid'
            fee.payment_date = timezone.now().date()
            fee.save()
            messages.success(request, f'Payment of ₹{fee.amount} for {fee.month} successful.')
        else:
            messages.warning(request, 'This fee has already been paid.')

    return redirect('fees:student_fee_list')


from django.db import models
