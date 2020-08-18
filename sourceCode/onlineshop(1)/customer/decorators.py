from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            group = None
            group = request.user.groups.all()[0].name
            if group == 'admin':
                return redirect('/dashboard/')
            if group == 'customer':
                return redirect('/')

        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func

def allowed_users(allowed_rule=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            #print(allowed_rule)

            group = None
            if request.user.groups.exists():

                group = request.user.groups.all()[0].name
            
            if group in allowed_rule:
                return view_func(request, *args, **kwargs)
            
            else:
                return HttpResponse("You are not allowed to view this page")
        return wrapper_func
    return decorator

def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
            
            if group == 'customer':
                return redirect('/user/')
            
            if group == 'admin':
                return view_func(request, *args, **kwargs)
        else:
            return HttpResponse(request,"No group exists!!???")

    return wrapper_func
