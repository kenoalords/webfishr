# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.shortcuts import render, reverse
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.core.serializers import serialize, deserialize

from fishr.models import Order

SITE = Site.objects.get_current()

@shared_task
def send_subscription_email(email, uuid):
    email_body = render_to_string('email/subscription_notification.html', context={ 'uuid': uuid, 'current_site': SITE })
    link = "{0}{1}".format(SITE.domain, reverse('email_verify', kwargs={ 'uuid': uuid }))
    site_name = "{0} Team".format(SITE.name)
    email_body_text = """
                    Hello,

                    Thank you for joining our awesome mailing list.
                    Please copy and paste the link below into your browser to activate your email.

                    {0}

                    BR.
                    {1}
                    """
    text = email_body_text.format(link, site_name)
    email = EmailMultiAlternatives(
                    to=[email,],
                    subject='🔔Activate your email!',
                    body= text
                )
    email.attach_alternative(email_body, 'text/html')
    email.send()


# Order notification
@shared_task
def send_order_notification(email, uuid):
    order = Order.objects.get(uuid=uuid)
    link = "{0}{1}".format(SITE.domain, reverse('order', kwargs={ 'uuid': uuid }))
    email_body = render_to_string('email/order_notification.html', context={ 'uuid': uuid, 'current_site': SITE, 'order': order, 'link': link })
    site_name = "{0} Team".format(SITE.name)
    email_body_text = """
                    Hello {},

                    Your order was successful.
                    You are just one step away from enjoying our professional online services.

                    Your order details are as follows;
                    Package: {} Package
                    Amount: N{}

                    Please copy and paste the link below into your browser to make payment using your preferred payment method.
                    {}

                    BR.
                    {}
                    """
    text = email_body_text.format(order.user.first_name, order.package.title, int(order.amount), link, site_name)
    email = EmailMultiAlternatives(
                    to=[email,],
                    subject='Your Order Details',
                    body= text
                )
    email.attach_alternative(email_body, 'text/html')
    email.send()

@shared_task
def send_allauth_email(msg):
    obj = deserialize(msg)
    obj.send()
