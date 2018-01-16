"""

"""
from django.http.response import HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect
from django.template import loader

from api.models import Property
from interface.forms import UserSignUpForm, AuthenticationForm, PropertyForm


def index(request):
    """

    :return:
    """
    if 'user' in request.session:
        return redirect('properties_list')
    template = loader.get_template('interface/index.html')
    auth_form = AuthenticationForm()
    if request.method == 'GET':
        form = UserSignUpForm()
        return HttpResponse(template.render(dict(form=form, loginform=auth_form), request))
    elif request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('Saved')
        else:
            return HttpResponse(template.render(dict(form=form, loginform=auth_form), request))
    else:
        return HttpResponse('Not Allowed')


def login(request):
    """

    :param request:
    :return:
    """
    if 'user' in request:
        return redirect('properties_list')
    template = loader.get_template('interface/index.html')
    register_form = UserSignUpForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            request.session['user'] = form.get_user_id()
            return HttpResponse('Login')
        else:
            return HttpResponse(template.render(dict(form=register_form, loginform=form), request))
    else:
        return HttpResponse('Not Allowed')


def logout(request):
    """

    :param request:
    :return:
    """
    if 'user' not in request.session:
        return HttpResponse('Not Login')

    del request.session['user']
    return HttpResponse('Logged Out')


def properties_list(request):
    """

    :param request:
    :return:
    """
    props = Property.objects.all()

    return HttpResponse(props)


def property_edit(request, pk):
    """

    :param request:
    :return:
    """
    prop = Property.objects.get(pk=pk)
    if request.session['user'] != prop.owner_id:
        return HttpResponseForbidden('This property does not belong to you.')
    template = loader.get_template('interface/property.html')
    form = PropertyForm(request.POST or None, instance=prop)
    if form.is_valid():
        form.save()
        return HttpResponse('Saved')
    else:
        return HttpResponse(template.render(dict(form=form), request))


def property(request):
    """

    :param request:
    :return:
    """

    template = loader.get_template('interface/property.html')
    form = PropertyForm(request.POST or None)
    if form.is_valid():
        prop = Property(**form.cleaned_data)
        prop.owner_id = request.session['user']
        prop.save()
        return HttpResponse('Saved')
    else:
        return HttpResponse(template.render(dict(form=form), request))
