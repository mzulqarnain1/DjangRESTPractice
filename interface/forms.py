
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user_model
from django.utils.text import capfirst

from api.models import Property


class UserSignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    password1 = forms.CharField(label="Password",
                                required=True,
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation",
                                required=True,
                                widget=forms.PasswordInput,
                                help_text="Enter the same password as above, for verification.")

    def clean_password2(self):
        """

        :return:
        """
        pass1 = self.cleaned_data['password1']
        pass2 = self.cleaned_data['password2']

        if pass1 and pass2 and pass1 != pass2:
            self.add_error('password2', 'Passwords do not match.')

    def save(self, commit=True):
        """

        :param commit:
        :return:
        """
        user = super(UserSignUpForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_staff = True
        user.is_active = True
        if commit:
            user.save()
        return user


class AuthenticationForm(forms.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """
    username = forms.CharField(max_length=254)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    error_messages = {
        'invalid_login': "Please enter a correct %(username)s and password. "
                         "Note that both fields may be case-sensitive.",
        'inactive': "This account is inactive.",
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super(AuthenticationForm, self).__init__(*args, **kwargs)

        # Set the label for the "username" field.
        UserModel = get_user_model()
        self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        if self.fields['username'].label is None:
            self.fields['username'].label = capfirst(self.username_field.verbose_name)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username,
                                           password=password)
            if self.user_cache is None:
                self.add_error('password', 'Username or Password Incorrect')
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        """
        Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active users, and reject login by inactive users.

        If the given user cannot log in, this method should raise a
        ``forms.ValidationError``.

        If the given user may log in, this method should return None.
        """
        if not user.is_active:
            self.add_error('password', 'Your account is deactivated')

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache


class PropertyForm(forms.ModelForm):
    """

    """
    class Meta:
        model = Property
        fields = ('address', 'type', 'status', 'parentProperty')
