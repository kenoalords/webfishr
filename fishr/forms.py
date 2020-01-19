from django.contrib.auth.models import User
from django import forms
from django.contrib.humanize.templatetags.humanize import intcomma
from fishr.models import Order, Package, Theme, EmailSubscription, Blog
from django.utils.safestring import mark_safe
from django.core.validators import ValidationError
from django.utils.translation import gettext_lazy as _

class PackageModelChoiceField(forms.ModelChoiceField):
	def label_from_instance(self, obj):
		return mark_safe( '<div><h4 class="title is-3 is-size-4-mobile has-text-weight-bold is-marginless">%s</h4><div><span class="cost has-text-weight-bold has-text-success">₦%s</span> <del class="has-text-light">N%s</del></div></div>' % (obj.title, intcomma(obj.sale_price), obj.regular_price) )

class ThemeModelChoiceField(forms.ModelChoiceField):
	def label_from_instance(self, obj):
		return mark_safe( '<figure class="image"><img src="%s" alt="%s"><figcaption class="">%s</figcaption></figure>' % (obj.image.url, obj.title, obj.title) )

class PackageForm(forms.ModelForm):
    package = PackageModelChoiceField(label="", queryset=Package.objects.filter(category__title="Web Design"), widget=forms.RadioSelect(attrs={'class': 'radio-select'}), empty_label=None)

    class Meta:
        fields = ['package']
        model = Order

class ThemeForm(forms.ModelForm):
    theme = ThemeModelChoiceField(label="", queryset=Theme.objects.all(), widget=forms.RadioSelect(attrs={'class': 'radio-select'}), empty_label=None)

    class Meta:
        fields = ['theme']
        model = Order

def validate_user_email(value):
	check = User.objects.filter(email=value)
	if check:
		raise ValidationError( _('%(value)s is already registered. Please login to continue with your order'), params={ 'value': value } )

class DomainForm(forms.Form):
	domain_name = forms.CharField(label="Enter your domain name", widget=forms.TextInput(attrs={ 'class': 'input', 'placeholder': 'www.mycompanyname.com' }))
	is_domain_owner = forms.BooleanField(label='Check this box if you currently own this domain', widget=forms.CheckboxInput())
	tos = forms.BooleanField(label="I agree to your terms and condition", widget=forms.CheckboxInput(), error_messages={ 'required': 'Please agree to our terms and condition' })
	error_css_class = 'is-danger'

PAYMENT_CHOICES = (
	('online', 'Pay online using your debit card via PayStack'),
	('transfer', 'Pay by Bank Transfer'),
)
class PaymentForm(forms.Form):
	type = forms.ChoiceField( choices=PAYMENT_CHOICES, widget=forms.RadioSelect())

class EmailSubscriptionForm(forms.ModelForm):
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={ 'class': 'input is-rounded', 'placeholder': 'Email address' }))

	class Meta:
		model = EmailSubscription
		fields = ['email']


# Blog form
class BlogForm(forms.ModelForm):
	title = forms.CharField(label='', widget=forms.TextInput(attrs={ 'class': 'input', 'placeholder': 'Enter blog title' }))
	content = forms.CharField(label='', widget=forms.Textarea(attrs={ 'class': 'textarea', 'placeholder': 'Enter blog content' }))
	slug = forms.CharField(label='', widget=forms.TextInput(attrs={ 'class': 'input', 'placeholder': 'Provide slug' }))
	excerpt = forms.CharField(label='', widget=forms.Textarea(attrs={ 'class': 'textarea', 'placeholder': 'Enter blog title', 'rows': 2 }))
	is_public = forms.CharField(required=False, widget=forms.CheckboxInput())
	image = forms.ImageField(required=False)
	class Meta:
		model = Blog
		fields = ['title', 'content', 'slug', 'excerpt', 'image', 'is_public']
