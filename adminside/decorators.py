from functools import wraps
from django.shortcuts import redirect,render



def superuser_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_superuser:
            # Redirect to the user's home page or another appropriate view
            return render(request,'admintemplates/adminsignin.html')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
