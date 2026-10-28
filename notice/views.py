from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Notice
from accounts.decorators import admin_required, student_required


# ==================== ADMIN VIEWS ====================

@admin_required
def notice_list(request):
    notices = Notice.objects.all()
    return render(request, 'notice/notice_list.html', {'notices': notices})


@admin_required
def notice_add(request):
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
            return render(request, 'notice/notice_add.html', {
                'errors': errors,
                'form_data': request.POST
            })

        notice = Notice(
            title=title,
            description=description
        )
        notice.save()
        messages.success(request, 'Notice added successfully.')
        return redirect('notice:notice_list')

    return render(request, 'notice/notice_add.html')


@admin_required
def notice_view(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    return render(request, 'notice/notice_view.html', {'notice': notice})


@admin_required
def notice_delete(request, pk):
    if request.method == 'POST':
        notice = get_object_or_404(Notice, pk=pk)
        notice.delete()
        messages.success(request, 'Notice deleted successfully.')
    return redirect('notice:notice_list')


# ==================== STUDENT VIEWS ====================

@student_required
def student_notice_list(request):
    notices = Notice.objects.all()
    return render(request, 'notice/student_notice_list.html', {'notices': notices})


@student_required
def student_notice_view(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    return render(request, 'notice/student_notice_view.html', {'notice': notice})
