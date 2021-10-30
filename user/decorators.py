from django.shortcuts import redirect


def user_only(view_fun):
    def wrapper(request, *args, **kwargs):
        if not request.session.has_key('user'):
            return redirect('accounts:login')
        return view_fun(request, *args, **kwargs)
    return wrapper
