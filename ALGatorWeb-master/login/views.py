#views.py
from login.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.template.defaulttags import register
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from login.models import UserProfile, ProfileForm

@register.filter
def field_type(field):
    """
    Get the name of the form field class.
    """
    if hasattr(field, 'field'):
        field = field.field
    s = str(type(field.widget).__name__)
    s = s.rpartition('Input')[0]
    s = s.lower()
    return s

@csrf_protect
def register(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email']
            )
            group = Group.objects.get(name="users")
            group.user_set.add(user)


            return HttpResponseRedirect('/register/success/')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {
    'form': form
    })
 
    return render_to_response(
    'registration/register.html',
    variables,
    )

def register_success(request):
    return render_to_response(
    'registration/success.html',
    )

def guest(request):
    user = authenticate(username='guest',password='guest')
    if user is not None:
        login(request,user)
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')
 
@login_required
def home(request):
    return render_to_response(
        'home.html',
        {'user': request.user,
         }, context_instance=RequestContext(request)
    )

@login_required
def settings_page(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None

    form = ProfileForm(request.POST or None, instance=profile)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/settings/')
    return render_to_response(
        'profile.html',
        {'form': form,
         }, context_instance=RequestContext(request)
    )



