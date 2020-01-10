from allauth.account.forms import LoginForm, ResetPasswordForm, SignupForm, SetPasswordForm
from django import forms
from django.template.defaultfilters import slugify
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3
# from allauth.compat import ugettext, ugettext_lazy as _

# from .models import Profile

class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget = forms.TextInput(attrs={'class': 'input', 'placeholder': 'Username or Email Address'})
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Password'})
        self.fields['captcha'] = ReCaptchaField(widget=ReCaptchaV3)
        self.fields['password'].label = ''
        self.fields['login'].label = ''


class CustomResetPasswordForm(ResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(CustomResetPasswordForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget = forms.TextInput(attrs={'class': 'input', 'placeholder': 'Email Address'})
        self.fields['email'].label = ''

class CustomSignupForm(SignupForm):
    error_css_class = 'is-danger'
    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        self.fields['first_name'] = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'First name'}))
        self.fields['last_name'] = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Last name'}))
        self.fields['captcha'] = ReCaptchaField(widget=ReCaptchaV3)
        self.fields['email'].widget = forms.TextInput(attrs={'class': 'input', 'placeholder': 'Email Address'})
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Password'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Confirm password'})

        self.fields['password1'].label = ''
        self.fields['password2'].label = ''
        self.fields['email'].label = ''

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        # Custom processing here
        first_name = request.POST.get('first_name', False)
        last_name = request.POST.get('last_name', False)
        if first_name and last_name:
            user.first_name = first_name
            user.last_name = last_name
            user.username = slugify( request.POST.get('email') )
            user.save()
        return user



class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.TextInput(attrs={'class': 'input', 'placeholder': 'Password'})
        self.fields['password2'].widget = forms.TextInput(attrs={'class': 'input', 'placeholder': 'Confirm password'})

        self.fields['password1'].label = ''
        self.fields['password2'].label = ''
