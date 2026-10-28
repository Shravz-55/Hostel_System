from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('is_admin'):
            messages.error(request, 'Please login as admin to access this page.')
            return redirect('accounts:admin_login')
        return view_func(request, *args, **kwargs)
    return wrapper


def warden_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('is_warden'):
            messages.error(request, 'Please login as warden to access this page.')
            return redirect('accounts:warden_login')
        return view_func(request, *args, **kwargs)
    return wrapper


def student_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('is_student'):
            messages.error(request, 'Please login as student to access this page.')
            return redirect('accounts:student_login')
        return view_func(request, *args, **kwargs)
    return wrapper
