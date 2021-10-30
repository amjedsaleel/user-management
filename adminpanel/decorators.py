from django.http import Http404
from django.shortcuts import redirect


def admin_only(view_fun):
    def wrapper(request, *args, **kwargs):
        if not request.session.has_key('admin'):
            return redirect('admin-panel:admin-login')
        return view_fun(request, *args, **kwargs)
    return wrapper
