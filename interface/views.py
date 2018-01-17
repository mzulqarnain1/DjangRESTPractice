"""
This module handles all the views for our interface
for user registration/login and user's properties
add/edit.
"""
from django.http.response import HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect
from django.template import loader

from api.models import Property
from interface.forms import UserSignUpForm, AuthenticationForm, PropertyForm


def index(request):
    """
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
            form = UserSignUpForm()
            return HttpResponse(template.render(dict(form=form, loginform=auth_form,
                                                     message='Signed Up Successfully. Kindly'
                                                             ' Login'), request))
        else:
            return HttpResponse(template.render(dict(form=form, loginform=auth_form), request))
    else:
        return HttpResponse('Not Allowed')


def login(request):
    """
    """
    if 'user' in request:
        return redirect('properties_list')
    template = loader.get_template('interface/index.html')
    register_form = UserSignUpForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            request.session['user'] = form.get_user_id()
            return redirect('properties_list')
        else:
            return HttpResponse(template.render(dict(form=register_form, loginform=form), request))
    else:
        return HttpResponse(HttpResponseForbidden)


def logout(request):
    """
    """
    if 'user' not in request.session:
        return HttpResponse('Not Login')
    del request.session['user']

    return redirect('index')


def properties_list(request):
    """
    """
    props = Property.objects.all()
    template = loader.get_template('interface/list.html')

    return HttpResponse(template.render(dict(properties=props), request))


def property_edit(request, pk):
    """
    """
    prop = Property.objects.get(pk=pk)
    if request.session['user'] != prop.owner_id:
        return HttpResponseForbidden('This property does not belong to you.')
    template = loader.get_template('interface/property.html')
    form = PropertyForm(request.POST or None, instance=prop)
    if form.is_valid():
        form.save()
        props = Property.objects.all()
        template = loader.get_template('interface/list.html')

        return HttpResponse(template.render(dict(properties=props, message='Property Updated'), request))
    else:
        return HttpResponse(template.render(dict(form=form), request))


def property(request):
    """
    """
    if 'user' not in request.session:
        return redirect('index')
    template = loader.get_template('interface/property.html')
    form = PropertyForm(request.POST or None)
    if form.is_valid():
        prop = Property(**form.cleaned_data)
        prop.owner_id = request.session['user']
        prop.save()
        props = Property.objects.all()
        template = loader.get_template('interface/list.html')

        return HttpResponse(template.render(dict(properties=props, message='Property Saved'), request))
    else:
        return HttpResponse(template.render(dict(form=form), request))
