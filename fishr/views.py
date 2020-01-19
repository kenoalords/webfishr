from django.shortcuts import render, reverse, render_to_response
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.views.generic import TemplateView, DetailView, View, ListView
from django.db import IntegrityError
from meta.views import Meta
from formtools.wizard.views import SessionWizardView, NamedUrlSessionWizardView
from django.template.defaultfilters import slugify
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.conf import settings
from django.template import RequestContext
import requests, json

# App Imports
from fishr.forms import PackageForm, ThemeForm, DomainForm, PaymentForm, EmailSubscriptionForm, BlogForm
from fishr.models import Theme, Package, Order, Faq, EmailSubscription, Blog
from .tasks import send_subscription_email, send_order_notification, send_order_payment_notification
from .mixins import SuperUserMixin, BlogPublicMixin


from django.contrib import admin
from django.contrib.auth.decorators import login_required

admin.site.login = login_required(admin.site.login)

SITE_META = 'WebFishr | Web Design Service in Nigeria'

meta = Meta(
    title = "Affordable Website Design - %s" % SITE_META,
    description = "Our website design service gives you the perfect online presence with a global reach. Get a budget friendly website design today",
    keywords = ['web design', 'affordable website design', 'website design and development', 'corporate website design', 'ecommerce website design', 'sme website design', 'cheap website design']
)

# Create your views here.
class IndexView(TemplateView):
    template_name = 'app/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meta'] = meta
        return context

class CareerTemplateView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meta'] = Meta(
            title='Careers - %s' % SITE_META,
            description='Start a career as web designer, graphics designer, digital marketer and content management. Contact us today for availability'
        )
        return context

class ContactTemplateView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meta'] = Meta(
            title='Contact Us - %s' % SITE_META,
            description='Want to find out more about our website design and management services? Send us an email today.'
        )
        return context

class AboutTemplateView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meta'] = Meta(
            title='About Us - %s' % SITE_META,
            description='We are a team of highly skilled website designers and managers helping you build the perfect online presence for your business'
        )
        return context

class PolicyTemplateView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meta'] = Meta(
            title='Privacy Policy - %s' % SITE_META,
            description='Read our privacy policy to find out how we use your private information on our website.'
        )
        return context

class HowItWorksTemplateView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meta'] = Meta(
            title='How It Works - %s' % SITE_META,
            description='See how our website design and management services helps you get your online presence up and running quickly.'
        )
        return context

class WebsiteThemeView(TemplateView):
    template_name = 'app/themes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meta'] = Meta(
            title='Find your website design - %s' % SITE_META,
            description='Choose a website theme for your business from our collection of beautiful and professional website designs.'
        )
        return context

class PricingView(TemplateView):
    template_name = 'app/pricing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meta'] = Meta(
            title='Website design packages - %s' % SITE_META,
            description='Choose a website design package that is perfect for your business and budget.'
        )
        return context

class WebsiteDesignPreviewView(DetailView):
    template_name = 'app/design_preview.html'
    model = Theme

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meta'] = Meta(
            title='Website Theme - %s' % SITE_META,
            description='Choose the right website theme for your business from our collection of beautiful and professional website design templates.'
        )
        return context

class FaqTemplateView(TemplateView):
    template_name = 'app/faq.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['faqs'] = Faq.objects.all()
        context['meta'] = Meta(
            title='Frequently asked questions - %s' % SITE_META,
            description='Signing up for a new website on WebFishr? Here are some of the commonly asked questions about our website design and management service.'
        )
        return context

FORMS = [
    ('theme', ThemeForm),
    ('package', PackageForm),
    ('domain', DomainForm),
    ('payment', PaymentForm),
]

FORM_TEMPLATES = {
    'package': 'app/order_package.html',
    'theme': 'app/order_theme.html',
    'domain': 'app/order_domain.html',
    'payment': 'app/order_payment.html',
}

def is_user_loggedin(wizard):
    print(wizard.request.user)
    return True

class OrderWizardView(LoginRequiredMixin, SessionWizardView):
    form_list = FORMS

    def get_template_names(self):
        return [FORM_TEMPLATES[self.steps.current]]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meta'] = Meta(
            title='Order a website design - %s' % SITE_META,
            description='Order your website design service and get a professional website in 48 hours.'
        )
        return context

    def get_form_initial(self, step):
        if step == 'theme' and self.request.GET.get('theme', False):
            return self.initial_dict.get(step, {'theme': self.request.GET.get('theme')})
        if step == 'package' and self.request.GET.get('package', False):
            return self.initial_dict.get(step, {'package': self.request.GET.get('package')})
        return self.initial_dict.get(step, {})


    def done(self, form_list, form_dict, **kwargs):

        theme = form_dict['theme'].cleaned_data['theme']
        package = form_dict['package'].cleaned_data['package']
        domain_name = form_dict['domain'].cleaned_data['domain_name']
        payment_type = form_dict['payment'].cleaned_data['type']
        is_domain_owner = form_dict['domain'].cleaned_data['is_domain_owner']

        # Add order
        # amount = Package.objects.get(pk=)
        order = Order(
            user=self.request.user,
            package= package,
            theme= theme,
            domain_name=domain_name,
            is_domain_owner=is_domain_owner,
            payment_type=payment_type,
            amount=package.sale_price
        )
        order.save()
        # Redirect to respective pages
        send_order_notification.delay(order.user.email, order.uuid)
        return HttpResponseRedirect(order.get_absolute_url())


class OrderCompleteView(TemplateView):
    template_name = 'app/order_complete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = Order.objects.get(uuid=kwargs['uuid'])
        context['meta'] = Meta(
            title='Order Complete',
            description='Please review your website design order below and choose your preferred payment option.'
        )
        return context

    def post(self, request, *args, **kwargs):
        try:
            order = Order.objects.get(uuid=kwargs['uuid'])
            if order.is_paid == True:
                messages.warning(request, 'This order has been paid for, please contact us if you have any issues')
                return HttpResponseRedirect(reverse('dashboard'))
            else:
                postdata = {
                    'amount': order.amount * 100,
                    'email': order.user.email,
                    'reference': order.uuid,
                }
                headers = {
                    'authorization': 'Bearer %s' % settings.PAYSTACK_SECRET,
                    'accept': 'application/json',
                    'cache-control': 'no-cache'
                }
                req = requests.post('https://api.paystack.co/transaction/initialize', data=postdata, headers=headers)
                if req.status_code == 200:
                    res = req.json()
                    print(res)
                    if res['status'] == True:
                        return HttpResponseRedirect(res['data']['authorization_url'])
                    else:
                        messages.error(request, 'We couldn\'t process your request at the moment. Please try again')
                        return HttpResponseRedirect(order.get_absolute_url())
                else:
                    messages.error(request, 'There seem to be a problem with Paystack at the momemt. This is entirely not your fault. Please wait a few minutes and try the transaction again')
                    return HttpResponseRedirect(order.get_absolute_url())
        except Order.DoesNotExist:
            messages.error(request, 'This order %s does not exist or has been deleted by admin.' % kwargs['uuid'])
            return HttpResponseRedirect(reverse('dashboard'))

class SubscribeEmail(View):
    def post(self, request, **kwargs):
        form = EmailSubscriptionForm(request.POST)
        if form.is_valid():
            try:
                sub = form.save()
                send_subscription_email.delay(sub.email, sub.uuid)
                if request.is_ajax():
                    return JsonResponse({ 'saved': True, 'redirect': reverse('email_sub_successful', kwargs={'uuid': sub.uuid}) })
                else:
                    return HttpResponseRedirect(reverse('email_sub_successful'))
            except IntegrityError as e:
                if request.is_ajax():
                    return JsonResponse({ 'saved': 'duplicate' })
            except Exception as e:
                if request.is_ajax():
                    error = e.message
                    return JsonResponse({ 'saved': False, 'error': error })
                else:
                    return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            if request.is_ajax():
                return JsonResponse({ 'saved': 'duplicate' })

class SubscriptionSuccessful(TemplateView):
    template_name = 'app/subscription.html'

class SubscriptionVerify(DetailView):
    model = EmailSubscription
    template_name = 'app/subscription_verify.html'

    def get(self, request, **kwargs):
        try:
            sub = EmailSubscription.objects.get(uuid=kwargs['uuid'])
            sub.is_verified = True
            sub.save()
            return render(request, self.template_name, context={ 'sub': sub })
        except sub.DoesNotExist as e:
            return HttpResponseRedirect(reverse('index'))
# Dashboard Views
class DashboardTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['orders'] = Order.objects.filter(user=self.request.user)
        context['meta'] = Meta(
            title='My Account - %s' % SITE_META,
        )
        return context

class PaystackCallback(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        ref = request.GET.get('trxref', False)
        if ref:
            url = 'https://api.paystack.co/transaction/verify/%s' % ref
            headers = { 'accept': 'application/json', 'authorization': 'Bearer %s' % settings.PAYSTACK_SECRET, 'cache-control': 'no-cache' }
            req = requests.get(url, headers=headers)
            if req.status_code == 200:
                body = req.json()
                if body['status'] == True:
                    ref = body['data']['reference']
                    amount = body['data']['amount'] / 100
                    order = Order.objects.get(uuid=ref)
                    order.is_paid = True
                    order.transaction_ref = ref
                    order.amount_paid = amount
                    order.save()
                    send_order_payment_notification(order.uuid)
                    messages.success(request, 'Your payment was successful. We will start processing your order immediately')
                    return HttpResponseRedirect(reverse('dashboard'))
        else:
            messages.error(request, 'There seem to be a problem with Paystack at the momemt. This is entirely not your fault. Please wait a few minutes and try the transaction again')
            return HttpResponseRedirect(reverse('index'))



# Blog views
class BlogListView(LoginRequiredMixin, SuperUserMixin, ListView):
    template_name = 'dashboard/blog.html'
    model = Blog
    context_object_name = 'blogs'

class BlogAddTemplateView(LoginRequiredMixin, SuperUserMixin, TemplateView):
    template_name = 'dashboard/blog_form.html'

    def get(self, request, *args, **kwargs):
        form = BlogForm()
        return render(request, self.template_name, context={ 'form': form })

    def post(self, request, *args, **kwargs):
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.user = request.user
            blog.save()
            messages.success(request, 'Blog post saved successfully')
            return HttpResponseRedirect(reverse('admin_blog'))
        else:
            return render(request, self.template_name, context={ 'form': form })


class BlogEditTemplateView(LoginRequiredMixin, SuperUserMixin, TemplateView):
    template_name = 'dashboard/blog_edit_form.html'

    def get(self, request, *args, **kwargs):
        blog = Blog.objects.get(pk=kwargs['pk'])
        form = BlogForm(instance=blog)
        return render(request, self.template_name, context={ 'form': form, 'blog': blog })

    def post(self, request, *args, **kwargs):
        blog = Blog.objects.get(pk=kwargs['pk'])
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog.title = form.cleaned_data['title']
            blog.slug = form.cleaned_data['slug']
            blog.content = form.cleaned_data['content']
            blog.excerpt = form.cleaned_data['excerpt']
            blog.is_public = form.cleaned_data['is_public']
            if request.FILES.get('image', False):
                blog.image = form.cleaned_data['image']
            blog.save()
            messages.success(request, 'Blog post updated successfully')
            return HttpResponseRedirect(reverse('admin_blog'))
        else:
            return render(request, self.template_name, context={ 'form': form, 'blog': blog })


# Blog view template
class BlogDetailView(BlogPublicMixin, DetailView):
    model = Blog
    template_name = 'app/blog_single.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['blogs'] = Blog.public.exclude(pk=self.object.pk)
        context['meta'] = Meta(title=self.object.title, description=self.object.excerpt)
        return context

class BlogPageListView(ListView):
    template_name = 'app/blogs.html'
    context_object_name = 'blogs'
    queryset = Blog.public.all()

def handle_403(request, exception):
    response = render_to_response('errors/403.html')
    response.status_code = 403
    return response

def handle_400(request, exception):
    response = render_to_response('errors/400.html')
    response.status_code = 400
    return response

def handle_500(request):
    response = render_to_response('errors/500.html')
    response.status_code = 500
    return response

def handle_404(request, exception):
    response = render_to_response('errors/404.html')
    response.status_code = 404
    return response










# END ---
