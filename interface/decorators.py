"""

"""
from django.shortcuts import redirect


def login_required(function):
    """
    :param function:
    :return:
    """
    def login_check(request, *args, **kwargs):

        if 'user' in request.session:
            return function(request, *args, **kwargs)
        else:
            return redirect('index')

    return login_check


def not_already_login(function):
    """
    :param function:
    :return:
    """
    def login_check_2(request, *args, **kwargs):

        if 'user' in request.session:
            return redirect('properties_list')
        else:
            return function(request, *args, **kwargs)

    return login_check_2
