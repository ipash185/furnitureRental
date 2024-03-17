from django.shortcuts import redirect

from users.models import UserInformation


def user_information_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                user_information = UserInformation.objects.get(user=request.user)
            except UserInformation.DoesNotExist:
                return redirect('billing-address')
            else:
                return function(request, *args, **kwargs)
        else:
            return redirect('billing-address')

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
