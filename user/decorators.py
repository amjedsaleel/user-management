from django.shortcuts import redirect


def user_only(view_fun):
    def wrapper(request, *args, **kwargs):
        if request.user.is_superuser:
            return redirect('admin-panel:dashboard')
        return view_fun(request, *args, **kwargs)
    return wrapper
