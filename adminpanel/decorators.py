from django.http import Http404


def admin_only(view_fun):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_superuser:
            raise Http404
        return view_fun(request, *args, **kwargs)
    return wrapper
